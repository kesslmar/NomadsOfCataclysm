#!/usr/bin/env python

# Author: Shao Zhang and Phil Saltzman
# Last Updated: 2015-03-13
#
# This tutorial will cover events and how they can be used in Panda
# Specifically, this lesson will use events to capture keyboard presses and
# mouse clicks to trigger actions in the world. It will also use events
# to count the number of orbits the Earth makes around the sun. This
# tutorial uses the same base code from the solar system tutorial.

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from panda3d.core import WindowProperties
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

import sys

base = ShowBase()
wp = WindowProperties()
wp.setSize(1080, 600)
base.win.requestProperties(wp)


class World(DirectObject):
    # Macro-like function used to reduce the amount to code needed to create the
    # on screen instructions

    def genLabelText(self, text, i):
        return OnscreenText(text=text, pos=(0.06, -.06 * (i + 0.5)), fg=(1, 1, 1, 1),
                            parent=base.a2dTopLeft,align=TextNode.ALeft, scale=.05)

    def __init__(self):

        # The standard camera position and background initialization
        base.setBackgroundColor(0, 0, 0)
        base.disableMouse()
        camera.setPos(0, -30, 30)
        camera.setHpr(0, -45, 0)
        

        # The global variables we used to control the speed and size of objects
        self.yearscale = 900
        self.dayscale = self.yearscale / 365.0 * 5
        self.yearCounter = 0
        self.dayCounter = 0
        self.orbitscale = 10
        self.sizescale = 0.6
        self.camSpeed = 10
        self.keyDict = {'left':False, 'right':False, 'up':False, 'down':False}
        self.followObject = None
        self.followObjectScale = 1
        self.followModeOn = False
        self.planetDB = {}

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.collQueue = CollisionHandlerQueue()
        base.cTrav = CollisionTraverser('myTraverser')
        base.cTrav.addCollider(self.pickerNP, self.collQueue)

        self.loadPlanets()  # Load, texture, and position the planets
        self.rotatePlanets()  # Set up the motion to start them moving

        taskMgr.add(self.setCam, "setcamTask")

        self.title = OnscreenText(
            text="Panda3D: Tutorial 3 - Events",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07)

        self.accept("escape", sys.exit)

        self.accept("arrow_up", self.pressKey, ["up"])
        self.accept("arrow_up-up", self.releaseKey, ["up"])
        self.accept("arrow_down", self.pressKey, ["down"])
        self.accept("arrow_down-up", self.releaseKey, ["down"])
        self.accept("arrow_left", self.pressKey, ["left"])
        self.accept("arrow_left-up", self.releaseKey, ["left"])
        self.accept("arrow_right", self.pressKey, ["right"])
        self.accept("arrow_right-up", self.releaseKey, ["right"])
        self.accept("mouse1", self.handleMouseClick)

    def pressKey(self, key): self.keyDict[key] = True
    def releaseKey(self, key): self.keyDict[key] = False
    def incYear(self): self.yearCounter += 1
    def incDay(self): self.dayCounter += 1

    def setCam(self, task):
        dt = globalClock.getDt()
        if self.keyDict['up']: camera.setPos(camera.getPos()[0],camera.getPos()[1] + self.camSpeed * dt, camera.getPos()[2])
        elif self.keyDict['down']: camera.setPos(camera.getPos()[0],camera.getPos()[1] - self.camSpeed * dt, camera.getPos()[2])
        if self.keyDict['left']: camera.setPos(camera.getPos()[0] - self.camSpeed * dt,camera.getPos()[1], camera.getPos()[2])
        elif self.keyDict['right']: camera.setPos(camera.getPos()[0] + self.camSpeed * dt,camera.getPos()[1], camera.getPos()[2])
        return task.cont
        

    def handleMouseClick(self):
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        base.cTrav.traverse(render)
        if self.collQueue.getNumEntries() > 0:
            self.collQueue.sortEntries()
            pickedObj = self.collQueue.getEntry(0).getIntoNodePath()
            pickedObj = pickedObj.findNetTag('clickable')
            if not pickedObj.isEmpty():
                self.toggleFollowCam(pickedObj)

    def toggleFollowCam(self, obj=None):
        if not self.followModeOn:
            self.followModeOn = True
            taskMgr.add(self.followCam, 'followcamTask')
            self.followObject = obj
            self.followObjectScale = self.planetDB[obj.getNetTag('clickable')]['scale']
        else:
            self.followModeOn = False
            taskMgr.remove('followcamTask')
            self.followObject = None
            self.followObjectScale = 1
            camera.setPos(camera.getPos()[0], camera.getPos()[1]-20, 30)
        print('Follow Mode is now: ' + str(self.followModeOn))

    def followCam(self, task):
        pos = self.followObject.getPos(base.render)
        camera.setPos(pos[0], pos[1]-self.followObjectScale * 7, self.followObjectScale * 7)
        return task.cont

    def loadPlanets(self):
        self.orbit_root_mercury = render.attachNewNode('orbit_root_mercury')
        self.orbit_root_venus = render.attachNewNode('orbit_root_venus')
        self.orbit_root_mars = render.attachNewNode('orbit_root_mars')
        self.orbit_root_earth = render.attachNewNode('orbit_root_earth')

        self.orbit_root_moon = (
            self.orbit_root_earth.attachNewNode('orbit_root_moon'))

        self.sky = loader.loadModel("models/solar_sky_sphere")

        self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render)
        self.sky.setScale(100)

        self.planetDB.update({'sun':{
            'scale':2, 'dist':0, 'type':'sun'}})
        self.sun = loader.loadModel("models/planet_sphere")
        self.sun_tex = loader.loadTexture("models/sun_1k_tex.jpg")
        self.sun.setTexture(self.sun_tex, 1)
        self.sun.reparentTo(render)
        self.sun.setScale(self.planetDB['sun']['scale'] * self.sizescale)
        self.sun.setTag('clickable', 'sun')

        self.planetDB.update({'mercury':{
            'scale':0.385, 'dist':0.38, 'type':'planet',
            'athm':False, 'wind':1, 'resc':{'coal':100, 'iron':50},
            'rescBlds':{}, 'prodBlds':{}, 'enrgBlds':{},
            'devBlds':{}, 'habBlds':{} }})
        self.mercury = loader.loadModel("models/planet_sphere")
        self.mercury_tex = loader.loadTexture("models/mercury_1k_tex.jpg")
        self.mercury.setTexture(self.mercury_tex, 1)
        self.mercury.reparentTo(self.orbit_root_mercury)
        self.mercury.setPos(self.planetDB['mercury']['dist'] * self.orbitscale, 0, 0)
        self.mercury.setScale(self.planetDB['mercury']['scale'] * self.sizescale)
        self.mercury.setTag('clickable', 'mercury')

        self.planetDB.update({'venus':{
            'scale':0.923, 'dist':0.72, 'type':'planet',
            'athm':False, 'wind':2, 'resc':{'coal':100, 'iron':50},
            'rescBlds':{}, 'prodBlds':{}, 'enrgBlds':{},
            'devBlds':{}, 'habBlds':{} }})
        self.venus = loader.loadModel("models/planet_sphere")
        self.venus_tex = loader.loadTexture("models/venus_1k_tex.jpg")
        self.venus.setTexture(self.venus_tex, 1)
        self.venus.reparentTo(self.orbit_root_venus)
        self.venus.setPos(self.planetDB['venus']['dist'] * self.orbitscale, 0, 0)
        self.venus.setScale(self.planetDB['venus']['scale'] * self.sizescale)
        self.venus.setTag('clickable', 'venus')

        self.planetDB.update({'mars':{
            'scale':0.512, 'dist':1.52, 'type':'planet',
            'athm':True, 'wind':1, 'resc':{'coal':100, 'iron':50},
            'rescBlds':{}, 'prodBlds':{}, 'enrgBlds':{},
            'devBlds':{}, 'habBlds':{} }})
        self.mars = loader.loadModel("models/planet_sphere")
        self.mars_tex = loader.loadTexture("models/mars_1k_tex.jpg")
        self.mars.setTexture(self.mars_tex, 1)
        self.mars.reparentTo(self.orbit_root_mars)
        self.mars.setPos(self.planetDB['mars']['dist'] * self.orbitscale, 0, 0)
        self.mars.setScale(self.planetDB['mars']['scale'] * self.sizescale)
        self.mars.setTag('clickable', 'mars')

        self.planetDB.update({'earth':{
            'scale':1, 'dist':1, 'type':'planet',
            'athm':False, 'wind':1, 'resc':{'coal':100, 'iron':50},
            'rescBlds':{}, 'prodBlds':{}, 'enrgBlds':{},
            'devBlds':{}, 'habBlds':{} }})
        self.earth = loader.loadModel("models/planet_sphere")
        self.earth_tex = loader.loadTexture("models/earth_1k_tex.jpg")
        self.earth.setTexture(self.earth_tex, 1)
        self.earth.reparentTo(self.orbit_root_earth)
        self.earth.setScale(self.planetDB['earth']['scale'] * self.sizescale)
        self.earth.setPos(self.planetDB['earth']['dist'] * self.orbitscale, 0, 0)
        self.earth.setTag('clickable', 'earth')

        self.orbit_root_moon.setPos(self.orbitscale, 0, 0)

        self.planetDB.update({'moon':{
            'scale':0.1, 'dist':0.1, 'type':'moon',
            'athm':False, 'wind':0, 'resc':{'coal':100, 'iron':50},
            'rescBlds':{}, 'prodBlds':{}, 'enrgBlds':{},
            'devBlds':{}, 'habBlds':{} }})
        self.moon = loader.loadModel("models/planet_sphere")
        self.moon_tex = loader.loadTexture("models/moon_1k_tex.jpg")
        self.moon.setTexture(self.moon_tex, 1)
        self.moon.reparentTo(self.orbit_root_moon)
        self.moon.setScale(0.1 * self.sizescale)
        self.moon.setPos(0.1 * self.orbitscale, 0, 0)
        self.moon.setTag('clickable', 'moon')

    def rotatePlanets(self):
        self.day_period_sun = self.sun.hprInterval(20, (360, 0, 0))

        self.orbit_period_mercury = self.orbit_root_mercury.hprInterval(
            (0.241 * self.yearscale), (360, 0, 0))
        self.day_period_mercury = self.mercury.hprInterval(
            (59 * self.dayscale), (360, 0, 0))

        self.orbit_period_venus = self.orbit_root_venus.hprInterval(
            (0.615 * self.yearscale), (360, 0, 0))
        self.day_period_venus = self.venus.hprInterval(
            (243 * self.dayscale), (360, 0, 0))

        self.orbit_period_earth = Sequence(
            self.orbit_root_earth.hprInterval(self.yearscale, (360, 0, 0))
            , Func(self.incYear))
        self.day_period_earth = Sequence(self.earth.hprInterval(
            self.dayscale, (360, 0, 0)), Func(self.incDay))

        self.orbit_period_moon = self.orbit_root_moon.hprInterval(
            (.0749 * self.yearscale), (360, 0, 0))
        self.day_period_moon = self.moon.hprInterval(
            (.0749 * self.yearscale), (360, 0, 0))

        self.orbit_period_mars = self.orbit_root_mars.hprInterval(
            (1.881 * self.yearscale), (360, 0, 0))
        self.day_period_mars = self.mars.hprInterval(
            (1.03 * self.dayscale), (360, 0, 0))

        self.day_period_sun.loop()
        self.orbit_period_mercury.loop()
        self.day_period_mercury.loop()
        self.orbit_period_venus.loop()
        self.day_period_venus.loop()
        self.orbit_period_earth.loop()
        self.day_period_earth.loop()
        self.orbit_period_moon.loop()
        self.day_period_moon.loop()
        self.orbit_period_mars.loop()
        self.day_period_mars.loop()

# end class world

w = World()
base.run()