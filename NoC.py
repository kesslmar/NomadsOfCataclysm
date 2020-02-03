#!/usr/bin/env python

# Author: Markus Kessler (Git: kesslmar)
# Last Updated: 2020-02-03
#
# The main goal of this smaller project is for me to dig deeper into software
# developement with python. Trying to build something like "Settlers of Catan,
# but in space" it forces me to get familiar with object oriented paradigms 
# and to use Github. Most of it is based on the "Solar System Tutorial"
# from the Panda 1.10 standard package

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

    def __init__(self):

        # The standard camera position and background initialization
        base.setBackgroundColor(0, 0, 0)
        base.disableMouse()
        camera.setPos(0, -30, 30)
        camera.setHpr(0, -45, 0)
        

        # The global variables we use to control the speed and size of objects
        self.yearscale = 900
        self.dayscale = self.yearscale / 365.0 * 5
        self.yearCounter = 0
        self.dayCounter = 0
        self.orbitscale = 10
        self.sizescale = 0.6
        self.camSpeed = 10
        self.zoomSpeed = 5
        self.keyDict = {'left':False, 'right':False, 'up':False, 'down':False}
        self.followObject = None
        self.followObjectScale = 1
        self.planetDB = {}

        self.PlanetInfoModeOn = False
        self.PlanetBuildModeOn = False
        self.PlanetBuildSection  = 'RESC' #Is either RESC, PROD, ENRG, DEV, HAB

        # Everything that's needed to detect selecting objects with mouse
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.collQueue = CollisionHandlerQueue()
        base.cTrav = CollisionTraverser('myTraverser')
        base.cTrav.addCollider(self.pickerNP, self.collQueue)

        # Set up the start screen
        self.setUpGui()
        self.loadPlanets()
        self.rotatePlanets()

        taskMgr.add(self.setCam, "setcamTask")

        # Open up all listeners for varous mouse and keyboard inputs
        self.accept("escape", sys.exit)
        self.accept("arrow_up", self.pressKey, ["up"])
        self.accept("arrow_up-up", self.releaseKey, ["up"])
        self.accept("w", self.pressKey, ["up"])
        self.accept("w-up", self.releaseKey, ["up"])
        self.accept("arrow_down", self.pressKey, ["down"])
        self.accept("arrow_down-up", self.releaseKey, ["down"])
        self.accept("s", self.pressKey, ["down"])
        self.accept("s-up", self.releaseKey, ["down"])
        self.accept("arrow_left", self.pressKey, ["left"])
        self.accept("arrow_left-up", self.releaseKey, ["left"])
        self.accept("a", self.pressKey, ["left"])
        self.accept("a-up", self.releaseKey, ["left"])
        self.accept("arrow_right", self.pressKey, ["right"])
        self.accept("arrow_right-up", self.releaseKey, ["right"])
        self.accept("d", self.pressKey, ["right"])
        self.accept("d-up", self.releaseKey, ["right"])
        self.accept("mouse1", self.handleMouseClick)
        self.accept("wheel_up", self.handleZoom, ['in'])
        self.accept("wheel_down", self.handleZoom, ['out'])
    
    # end of init function


    # Smaller single-line functions
    def pressKey(self, key): self.keyDict[key] = True
    def releaseKey(self, key): self.keyDict[key] = False
    def incYear(self): self.yearCounter += 1
    def incDay(self): self.dayCounter += 1

    #****************************************
    #            Main Functions             *
    #****************************************

    def setCam(self, task):
        dt = globalClock.getDt()
        if self.keyDict['up']: camera.setPos(camera.getPos()[0],camera.getPos()[1] + self.camSpeed * dt, camera.getPos()[2])
        elif self.keyDict['down']: camera.setPos(camera.getPos()[0],camera.getPos()[1] - self.camSpeed * dt, camera.getPos()[2])
        if self.keyDict['left']: camera.setPos(camera.getPos()[0] - self.camSpeed * dt,camera.getPos()[1], camera.getPos()[2])
        elif self.keyDict['right']: camera.setPos(camera.getPos()[0] + self.camSpeed * dt,camera.getPos()[1], camera.getPos()[2])
        return task.cont

    def handleZoom(self, direction):
        dt = globalClock.getDt()
        camPos = camera.getPos()
        if not self.PlanetInfoModeOn:    
            if direction == 'in' and camera.getPos()[2] > 5:
                zoomInterval = camera.posInterval(0.1, Point3(camPos[0],camPos[1]+self.zoomSpeed,camPos[2]-self.zoomSpeed,), camPos)
                zoomInterval.start()
            elif direction == 'out' and camera.getPos()[2] < 50:
                zoomInterval = camera.posInterval(0.1, Point3(camPos[0],camPos[1]-self.zoomSpeed,camPos[2]+self.zoomSpeed,), camPos)
                zoomInterval.start()

    def handleMouseClick(self):
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        base.cTrav.traverse(render)
        if self.collQueue.getNumEntries() > 0:
            self.collQueue.sortEntries()
            pickedObj = self.collQueue.getEntry(0).getIntoNodePath()
            pickedObj = pickedObj.findNetTag('clickable')
            if not pickedObj.isEmpty() and not self.PlanetInfoModeOn:
                self.togglePlanetInfoMode(True, pickedObj)

    def togglePlanetInfoMode(self, mode=False, obj=None):
        if mode:
            self.PlanetInfoModeOn = True
            taskMgr.add(self.followCam, 'followcamTask')
            self.followObject = obj
            self.followObjectScale = self.planetDB[obj.getNetTag('clickable')]['scale']
            pos = self.followObject.getPos(base.render)
            camPos = camera.getPos()
            zoomInterval = camera.posInterval(0.2, Point3(pos[0]-self.followObjectScale * 1.5,
                                                          pos[1]-self.followObjectScale * 4, 
                                                          self.followObjectScale * 4), camPos)
            zoomInterval.start()
            self.emptyPlanetInfo()
            self.fillPlanetInfo()
            self.PlanetInfoPanel.show()
        else:
            self.PlanetInfoModeOn = False
            taskMgr.remove('followcamTask')
            self.followObject = None
            self.followObjectScale = 1
            camPos = camera.getPos()
            zoomInterval = camera.posInterval(0.2, Point3(0, -30, 30), camPos)
            zoomInterval.start()
            self.PlanetInfoPanel.hide()
            self.emptyPlanetInfo()

    def togglePlanetBuildMode(self, mode=False):
        if mode==True:
            self.PlanetInfoPanel.hide()
            self.emptyPlanetInfo()
            self.PlanetBuildPanel.show()
        else:
            self.PlanetBuildPanel.hide()
            self.fillPlanetInfo()
            self.PlanetInfoPanel.show()


        return None

    def followCam(self, task):
        pos = self.followObject.getPos(base.render)
        camera.setPos(pos[0]-self.followObjectScale * 1.5, 
                      pos[1]-self.followObjectScale * 4, 
                      self.followObjectScale * 4)
        return task.cont

    def fillPlanetInfo(self):
        # Fills the content of the planet info gui every time a planet gets selected

        objID = self.followObject.getNetTag('clickable')
        
        PlanetInfoTitle = DirectLabel(text=self.planetDB[objID]['name'], 
            pos=(-0.85, 0, 0.5), text_fg=(1,1,1,1), frameColor=(0,0,0,0), 
            parent = self.PlanetInfoPanel, text_align=TextNode.ALeft, text_scale = 0.13
            )
        self.PlanetInfoPanelContent.append(PlanetInfoTitle)
    
        PlanetInfoAttributesText = (
            'Type:\t\t' + str(self.planetDB[objID]['type']) + '\n'
            'Diameter:\t\t' + str(self.planetDB[objID]['scale'] * 10**5) + '\n')
        if self.planetDB[objID]['type'] != "Star":
            PlanetInfoAttributesText += (
                'Distance to Sun:\t' + str(self.planetDB[objID]['dist'] * 10**7) + '\n'
                'Athmosphere:\t' + str(self.planetDB[objID]['athm']) + '\n'
                'Windstrength:\t' + str(self.planetDB[objID]['wind']) + '\n')

        PlanetInfoAttributesTable = DirectLabel(text=PlanetInfoAttributesText,
            pos=(-0.85, 0, 0.4), text_fg=(1,1,1,1), frameColor=(0,0,0,0), 
            parent = self.PlanetInfoPanel, text_align=TextNode.ALeft,
            scale=0.13, text_scale=0.5)
        self.PlanetInfoPanelContent.append(PlanetInfoAttributesTable)

        if self.planetDB[objID]['type'] != "Star":
            PlanetInfoRescourceText = 'Rescources:\n'
            for k,v in self.planetDB[objID]['resc'].items():
                PlanetInfoRescourceText += k + ':\t\t' + str(v) + '\n'

            PlanetInfoRescourceTable = DirectLabel(text=PlanetInfoRescourceText,
                pos=(-0.85, 0, 0), text_fg=(1,1,1,1), frameColor=(0,0,0,0), 
                parent = self.PlanetInfoPanel, text_align=TextNode.ALeft,
                scale=0.13, text_scale=0.5)
            self.PlanetInfoPanelContent.append(PlanetInfoRescourceTable)

    def emptyPlanetInfo(self):
        for element in self.PlanetInfoPanelContent:
            element.destroy()


    #****************************************
    #       Initialisation Functions        *
    #****************************************

    def setUpGui(self):
        # Constant visible gui elements
        #------------------------------
        self.Calendar = OnscreenText(text='Year '+str(self.yearCounter)+', Day '+str(self.dayCounter), 
            pos=(0.06, -.06), fg=(1, 1, 1, 1),
            parent=base.a2dTopLeft,align=TextNode.ALeft, scale=.05)

        # All static gui elements for the planet info screen
        #---------------------------------------------------
        self.PlanetInfoPanel = DirectFrame(
            frameColor=(0.15, 0.15, 0.15, 0.9),
            frameSize=(-0.9, 0.9, -0.65, 0.65),
            pos=(-0.8, 0, 0))
        self.PlanetInfoPanel.hide()

        self.PlanetInfoPanelContent = []

        self.PlanetInfoCloseButton = DirectButton(text='Close', 
            pos=(-0.745,0,0.7), pad=(0.05, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.togglePlanetInfoMode, extraArgs=[False])
        self.PlanetInfoCloseButton.reparentTo(self.PlanetInfoPanel)

        self.PlanetInfoBuildButton = DirectButton(text='Build', 
            pos=(1.8,0,-0.61), pad=(0.06, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.togglePlanetBuildMode, extraArgs=[True])
        self.PlanetInfoBuildButton.reparentTo(self.PlanetInfoPanel)


        # All static gui elements for the planet build screen
        #----------------------------------------------------
        self.PlanetBuildPanel = DirectFrame(
            frameColor=(0.15, 0.15, 0.15, 0.9),
            frameSize=(-0.4, 0.4, -0.65, 0.65),
            pos=(-1.3, 0, 0))
        self.PlanetBuildPanel.hide()

        self.PlanetBuildPanelContent = []

        self.PlanetBuildCloseButton = DirectButton(text='Back', 
            pos=(-0.26,0,0.7), pad=(0.05, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.togglePlanetBuildMode, extraArgs=[False])
        self.PlanetBuildCloseButton.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildSectionDropdown = DirectOptionMenu(text="options", 
            pos=(-0.1,0,0.68),pad=(1.7, 1), borderWidth=(0.06,0.06),
            scale=0.15, text_scale=0.5, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            items=["RESC", "PROD", "ENRG", "DEV", "HAB"], 
            initialitem=2, highlightColor=(0.65, 0.65, 0.65, 1))
        self.PlanetBuildSectionDropdown.reparentTo(self.PlanetBuildPanel)


        self.PlanetBuildSlotButton1 = DirectButton(text='R1', 
            pos=(1.7,0,0.2), hpr=(0,0,45), pad=(0.04, 0.04), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1), text_roll=45,
            command=self.togglePlanetBuildMode, extraArgs=[True])
        self.PlanetBuildSlotButton1.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildSlotButton2 = DirectButton(text='R2', 
            pos=(1.7,0,-0.2), hpr=(0,0,45), pad=(0.04, 0.04), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1), text_roll=45,
            command=self.togglePlanetBuildMode, extraArgs=[True])
        self.PlanetBuildSlotButton2.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildSlotButton3 = DirectButton(text='R3', 
            pos=(1.4,0,0.4), hpr=(0,0,45), pad=(0.04, 0.04), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(0.5,0.5,0.5,1), text_roll=45,
            command=self.togglePlanetBuildMode, extraArgs=[True], state='DISABLED')
        self.PlanetBuildSlotButton3.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildSlotButton4 = DirectButton(text='R4', 
            pos=(1.4,0,0), hpr=(0,0,45), pad=(0.04, 0.04), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(0.5,0.5,0.5,1), text_roll=45,
            command=self.togglePlanetBuildMode, extraArgs=[True], state='DISABLED')
        self.PlanetBuildSlotButton4.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildSlotButton5 = DirectButton(text='R5', 
            pos=(1.4,0,-0.4), hpr=(0,0,45), pad=(0.04, 0.04), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(0.5,0.5,0.5,1), text_roll=45,
            command=self.togglePlanetBuildMode, extraArgs=[True], state='DISABLED')
        self.PlanetBuildSlotButton5.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildWire1 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(0,1,0,1),
            pos=(1.7,-0.5,-0.035))
        self.PlanetBuildWire1.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildWire2 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(1,0,0,1),
            pos=(1.4,-0.5, 0.165))
        self.PlanetBuildWire2.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildWire3 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(1,0,0,1),
            pos=(1.4,-0.5,-0.235))
        self.PlanetBuildWire3.reparentTo(self.PlanetBuildPanel)


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
            'name':'Sun', 'scale':2, 'dist':0, 'type':'Star'}})
        self.sun = loader.loadModel("models/planet_sphere")
        self.sun_tex = loader.loadTexture("models/sun_1k_tex.jpg")
        self.sun.setTexture(self.sun_tex, 1)
        self.sun.reparentTo(render)
        self.sun.setScale(self.planetDB['sun']['scale'] * self.sizescale)
        self.sun.setTag('clickable', 'sun')

        self.planetDB.update({'mercury':{
            'name':'Mercury', 'scale':0.385, 'dist':0.38, 'type':'Planet',
            'athm':False, 'wind':1, 'resc':{'Coal':100, 'Iron':50},
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
            'name':'Venus', 'scale':0.923, 'dist':0.72, 'type':'Planet',
            'athm':False, 'wind':2, 'resc':{'Coal':100, 'Uranium':250},
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
            'name':'Mars', 'scale':0.512, 'dist':1.52, 'type':'Planet',
            'athm':True, 'wind':1, 'resc':{'Noblestone':100, 'Iron':50},
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
            'name':'Earth', 'scale':1, 'dist':1, 'type':'Planet',
            'athm':False, 'wind':1, 'resc':{'Iron':50},
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
            'name':'Moon', 'scale':0.1, 'dist':0.1, 'type':'Moon',
            'athm':False, 'wind':0, 'resc':{'Coal':300, 'Cheese':20},
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