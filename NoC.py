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
base = ShowBase()

from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
import sys

# We start this tutorial with the standard class. However, the class is a
# subclass of an object called DirectObject. This gives the class the ability
# to listen for and respond to events. From now on the main class in every
# tutorial will be a subclass of DirectObject


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
        camera.setPos(0, -13, 40)
        camera.setHpr(0, -70, 0)
        

        # The global variables we used to control the speed and size of objects
        self.yearscale = 900
        self.dayscale = self.yearscale / 365.0 * 5
        self.yearCounter = 0  # year counter for earth years
        self.orbitscale = 10
        self.sizescale = 0.6
        self.camSpeed = 10
        self.keyDict = {'left':False, 'right':False, 'up':False, 'down':False}

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



        # Events
        # Each self.accept statement creates an event handler object that will call
        # the specified function when that event occurs.
        # Certain events like "mouse1", "a", "b", "c" ... "z", "1", "2", "3"..."0"
        # are references to keyboard keys and mouse buttons. You can also define
        # your own events to be used within your program. In this tutorial, the
        # event "newYear" is not tied to a physical input device, but rather
        # is sent by the function that rotates the Earth whenever a revolution
        # completes to tell the counter to update
        # Exit the program when escape is pressed
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

    def setCam(self, task):
        dt = globalClock.getDt()
        if self.keyDict['up']: camera.setPos(camera.getPos()[0],camera.getPos()[1] + self.camSpeed * dt, camera.getPos()[2])
        elif self.keyDict['down']: camera.setPos(camera.getPos()[0],camera.getPos()[1] - self.camSpeed * dt, camera.getPos()[2])
        if self.keyDict['left']: camera.setPos(camera.getPos()[0] - self.camSpeed * dt,camera.getPos()[1], camera.getPos()[2])
        elif self.keyDict['right']: camera.setPos(camera.getPos()[0] + self.camSpeed * dt,camera.getPos()[1], camera.getPos()[2])
        return task.cont

    def handleMouseClick(self):
        mpos = base.mouseWatcherNode.getMouse()
        pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        myTraverser.traverse(render)
        # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
        if myHandler.getNumEntries() > 0:
            # This is so we get the closest object.
            myHandler.sortEntries()
            pickedObj = myHandler.getEntry(0).getIntoNodePath()
            pickedObj = pickedObj.findNetTag('myObjectTag')
            if not pickedObj.isEmpty():
                handlePickedObject(pickedObj)

    def toggleInterval(self, interval):
        if interval.isPlaying():
            interval.pause()
        else:
            interval.resume()
    # end toggleInterval

    # the function incYear increments the variable yearCounter and then updates
    # the OnscreenText 'yearCounterText' every time the message "newYear" is
    # sent
    def incYear(self):
        self.yearCounter += 1
    # end incYear


#########################################################################
# Except for the one commented line below, this is all as it was before #
# Scroll down to the next comment to see an example of sending messages #
#########################################################################

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
        self.sky.setScale(40)

        self.sun = loader.loadModel("models/planet_sphere")
        self.sun_tex = loader.loadTexture("models/sun_1k_tex.jpg")
        self.sun.setTexture(self.sun_tex, 1)
        self.sun.reparentTo(render)
        self.sun.setScale(2 * self.sizescale)

        self.mercury = loader.loadModel("models/planet_sphere")
        self.mercury_tex = loader.loadTexture("models/mercury_1k_tex.jpg")
        self.mercury.setTexture(self.mercury_tex, 1)
        self.mercury.reparentTo(self.orbit_root_mercury)
        self.mercury.setPos(0.38 * self.orbitscale, 0, 0)
        self.mercury.setScale(0.385 * self.sizescale)

        self.venus = loader.loadModel("models/planet_sphere")
        self.venus_tex = loader.loadTexture("models/venus_1k_tex.jpg")
        self.venus.setTexture(self.venus_tex, 1)
        self.venus.reparentTo(self.orbit_root_venus)
        self.venus.setPos(0.72 * self.orbitscale, 0, 0)
        self.venus.setScale(0.923 * self.sizescale)

        self.mars = loader.loadModel("models/planet_sphere")
        self.mars_tex = loader.loadTexture("models/mars_1k_tex.jpg")
        self.mars.setTexture(self.mars_tex, 1)
        self.mars.reparentTo(self.orbit_root_mars)
        self.mars.setPos(1.52 * self.orbitscale, 0, 0)
        self.mars.setScale(0.515 * self.sizescale)

        self.earth = loader.loadModel("models/planet_sphere")
        self.earth_tex = loader.loadTexture("models/earth_1k_tex.jpg")
        self.earth.setTexture(self.earth_tex, 1)
        self.earth.reparentTo(self.orbit_root_earth)
        self.earth.setScale(self.sizescale)
        self.earth.setPos(self.orbitscale, 0, 0)
        self.earth.setTag('clickable', '1')

        self.orbit_root_moon.setPos(self.orbitscale, 0, 0)

        self.moon = loader.loadModel("models/planet_sphere")
        self.moon_tex = loader.loadTexture("models/moon_1k_tex.jpg")
        self.moon.setTexture(self.moon_tex, 1)
        self.moon.reparentTo(self.orbit_root_moon)
        self.moon.setScale(0.1 * self.sizescale)
        self.moon.setPos(0.1 * self.orbitscale, 0, 0)

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
        self.day_period_earth = self.earth.hprInterval(
            self.dayscale, (360, 0, 0))

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
    # end RotatePlanets()

# end class world

w = World()
base.run()