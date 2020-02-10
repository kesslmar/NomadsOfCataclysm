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
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task

import sys
import random
import math

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
        self.dayscale = self.yearscale / 365.0*30
        self.yearCounter = 0
        self.dayCounter = 0
        self.money = 2000
        self.orbitscale = 10
        self.sizescale = 0.6
        self.camSpeed = 10
        self.zoomSpeed = 5
        self.keyDict = {'left':False, 'right':False, 'up':False, 'down':False}

        self.selectedObject = None
        self.selectedObjectName = None
        self.followObjectScale = 1
        self.PlanetInfoModeOn = False
        self.PlanetBuildModeOn = False
        self.ActiveBuildSection  = 'RESC' #Is either RESC, PROD, ENRG, DEV or HAB
        self.ActiveBuildSlot = None
        self.ActiveBlueprint = None
        self.PopulationTimeDelta = 2
        self.taxFactor = 0.1
        self.salvageFactor = 0.75

        self.planetDB = {} #All attributes and constructed buildings that a planet has
        self.buildingsDB = {} #Contains all buildable structures

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
        self.fillBuildingsDB()
        self.prepareSlotsInPlanetDB()

        # Add all constantly running checks to the taskmanager
        taskMgr.add(self.setCam, "setcamTask")
        taskMgr.add(self.redrawHeadGUI, "redrawHeadGUITask")
        taskMgr.doMethodLater(self.PopulationTimeDelta, self.populatePlanetTask, 'populatePlanetTask', extraArgs=['earth'], appendTask=True)
        taskMgr.doMethodLater(2, self.generateMoneyTask, 'generateMoneyTask')
        # Other tasks are created in: constructBuilding()

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

    def followCam(self, mode, task):
        pos = self.selectedObject.getPos(base.render)
        if mode=='info':
            camera.setPos(pos[0]-self.followObjectScale * 1.5, 
                         pos[1]-self.followObjectScale * 4, 
                         self.followObjectScale * 4)
        if mode=='build':
            camera.setPos(pos[0]-self.followObjectScale * 0.9, 
                         pos[1]-self.followObjectScale * 3.3, 
                         0)
        return task.cont

    def redrawHeadGUI(self, task):
        self.HeadGUI.text = 'Year '+str(self.yearCounter)+', Day '+str(self.dayCounter) + ', Money: ' +str(self.money)
        return task.cont

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
            self.selectedObject = obj
            self.selectedObjectName = obj.getNetTag('name')
            self.followObjectScale = self.planetDB[obj.getNetTag('name')]['scale']
            pos = self.selectedObject.getPos(base.render)
            camPos = camera.getPos()
            self.clearPlanetInfo()
            self.fillPlanetInfo()
            self.checkForBuildButton()
            zoomInterval = Sequence(camera.posInterval(0.3, Point3(pos[0]-self.followObjectScale * 1.5,
                                                          pos[1]-self.followObjectScale * 4, 
                                                          self.followObjectScale * 4), camPos), Func(self.PlanetInfoPanel.show))
            zoomInterval.start()
            taskMgr.add(self.followCam, 'infocamTask', extraArgs=['info'], appendTask=True)
            taskMgr.doMethodLater(1, self.updatePlanetInfoTask, 'updatePlanetInfoTask')
        else:
            self.PlanetInfoModeOn = False
            taskMgr.remove('infocamTask')
            camPos = camera.getPos()
            zoomInterval = camera.posInterval(0.3, Point3(0, -30, 30), camPos)
            zoomInterval.start()
            taskMgr.remove('updatePlanetInfoTask')
            self.PlanetInfoPanel.hide()
            self.clearPlanetInfo()
            self.selectedObject = None
            self.followObjectScale = 1

    def togglePlanetBuildMode(self, mode=False):
        pos = self.selectedObject.getPos(base.render)
        camPos = camera.getPos()
        scale = self.followObjectScale
        if mode:
            self.PlanetInfoPanel.hide()
            self.clearPlanetInfo()
            self.fillBuildPanel()
            self.checkForConstructButton()
            self.checkForSalvageButton()
            self.updateBuildingLables()
            taskMgr.remove('infoCamTask')
            zoomInterval = Sequence(camera.posHprInterval(0.3, Point3(pos[0]-scale * 0.9, pos[1]-scale * 3.3, 0), Vec3(0,0,0), camPos),
                                    Func(self.PlanetBuildPanel.show))
            zoomInterval.start()
            taskMgr.add(self.followCam, 'buildcamTask', extraArgs=['build'], appendTask=True)
        else:
            self.PlanetBuildPanel.hide()
            self.clearSelectedBuildSlot()
            self.clearBuildPanel()
            self.updateBuildingLables()
            self.fillPlanetInfo()
            taskMgr.remove('buildcamTask')
            zoomInterval = Sequence(camera.posHprInterval(0.3, Point3(pos[0]-scale * 1.5, pos[1]-scale * 4, scale * 4), Vec3(0,-45,0), camPos),
                                    Func(self.PlanetInfoPanel.show))
            zoomInterval.start()
            taskMgr.add(self.followCam, 'infocamTask', extraArgs=['info'], appendTask=True)

        return None

    def fillPlanetInfo(self):
        # Fills the content of the planet info gui every time a planet gets selected

        objID = self.selectedObjectName
        self.PlanetInfoTitle['text']=self.planetDB[objID]['name']


        PlanetInfoAttributesText = (
            'Type:\t\t' + str(self.planetDB[objID]['type']) + '\n'
            'Diameter:\t\t' + str(self.planetDB[objID]['scale'] * 10**5) + '\n')
        if self.planetDB[objID]['type'] != "Star":
            PlanetInfoAttributesText += (
                'Distance to Sun:\t' + str(self.planetDB[objID]['dist'] * 10**7) + '\n'
                'Athmosphere:\t' + str(self.planetDB[objID]['athm']) + '\n'
                'Windstrength:\t' + str(self.planetDB[objID]['wind']) + '\n')

        self.PlanetInfoAttributesTable['text']=PlanetInfoAttributesText


        if self.planetDB[objID]['type'] != "Star":
            PlanetInfoRescourceText = 'Rescources:\n'
            for k,v in self.planetDB[objID]['resc'].items():
                PlanetInfoRescourceText += k + ':\t\t' + str(v) + '\n'

            self.PlanetInfoRescourceTable['text']=PlanetInfoRescourceText

            if 'goods' in self.planetDB[objID]:
                PlanetInfoGoodsText = 'Goods:\n'
                for k,v in self.planetDB[objID]['goods'].items():
                    PlanetInfoGoodsText += k + ':\t' + str(v) + '\n'

                self.PlanetInfoGoodsTable['text']=PlanetInfoGoodsText
            
            self.PlanetInfoENRGTable['text']=(
                'Energy capacity:\t' + str(self.planetDB[objID]['enrgCap']) + '\n'
                'Energy usage:\t' + str(self.planetDB[objID]['enrgUsg']) + '\n\n'
                
                'Habitation capacity:\t' + str(self.planetDB[objID]['habCap']) + '\n'
                'Population count:\t' + str(self.planetDB[objID]['pop']) + '\n\n'

                'Per Capita GDP:\t' + str(self.taxFactor)
            )

    def updatePlanetInfoTask(self, task):
        self.fillPlanetInfo()
        return task.again

    def clearPlanetInfo(self):
        self.PlanetInfoTitle['text']='Unknown'
        self.PlanetInfoAttributesTable['text']=''
        self.PlanetInfoRescourceTable['text']=''
        self.PlanetInfoGoodsTable['text']=''
        self.PlanetInfoENRGTable['text']=''

    def checkForBuildButton(self):
        if self.planetDB[self.selectedObjectName]['type']=='Star':
            self.PlanetInfoBuildButton.hide()
        else:
            self.PlanetInfoBuildButton.show()

    def switchBuildSection(self, section):
        if section != self.ActiveBuildSection:
            self.clearBuildPanel()
            self.clearSelectedBuildSlot()
            self.checkForConstructButton()
            self.checkForSalvageButton()
            self.ActiveBuildSection = section
            pos = self.PlanetBuildSlotContainer.getPos()
            swipeOutInterval = self.PlanetBuildSlotContainer.posInterval(0.1, Point3(pos[0],pos[1],pos[2]+2), pos)

            def rename():
                self.PlanetBuildSlot1['text'] = section[0] + '1'
                self.PlanetBuildSlot2['text'] = section[0] + '2'
                self.PlanetBuildSlot3['text'] = section[0] + '3'
                self.PlanetBuildSlot4['text'] = section[0] + '4'
                self.PlanetBuildSlot5['text'] = section[0] + '5'
                self.updateBuildingLables()

            swipeInInterval = self.PlanetBuildSlotContainer.posInterval(0.1, pos, Point3(pos[0],pos[1],pos[2]-2))
            
            mySeq = Sequence(swipeOutInterval, Func(rename), swipeInInterval)      
            mySeq.start()
            self.fillBuildPanel()

    def switchBuildSlot(self, newSlot):
        self.clearSelectedBuildSlot()
        self.ActiveBuildSlot = newSlot
        newSlot['relief'] = 'sunken'
        self.checkForConstructButton()
        self.checkForSalvageButton()

    def switchBuildBlueprint(self, blueprint, building):
        if self.ActiveBlueprint != None:
            self.ActiveBlueprint['frameColor']=(0.15,0.15,0.15,0.9)
        else:
            self.PlanetBuildDescriptionField.show()
        self.ActiveBlueprint = blueprint
        blueprint['frameColor']=(0.3,0.3,0.3,0.9)
        
        self.PlanetBuildDescriptionText['text'] = ( building['desc'] + '\n\n'
                                                    'Requires: ' + building['reqText'] + '\n\n'
                                                    'Yields: ' + building['yieldText'])
        
        self.checkForConstructButton()

    def checkForConstructButton(self):
        planet=self.selectedObjectName
        section=self.ActiveBuildSection

        if self.ActiveBlueprint != None and self.ActiveBuildSlot != None and self.planetDB[planet]['slots'][section][self.ActiveBuildSlot['text']] == None:
            self.PlanetBuildConstructButton['state']='normal'
            self.PlanetBuildConstructButton['text_fg']=(1,1,1,1)
        else:
            self.PlanetBuildConstructButton['state']='disabled'
            self.PlanetBuildConstructButton['text_fg']=(0.5,0.5,0.5,1)
        
    def checkForSalvageButton(self):
        planet=self.selectedObjectName
        section=self.ActiveBuildSection

        if self.ActiveBuildSlot != None and self.planetDB[planet]['slots'][section][self.ActiveBuildSlot['text']] != None:
            self.PlanetBuildSalvageButton['state']='normal'
            self.PlanetBuildSalvageButton['text_fg']=(1,1,1,1)
        else:
            self.PlanetBuildSalvageButton['state']='disabled'
            self.PlanetBuildSalvageButton['text_fg']=(0.5,0.5,0.5,1)

    def fillBuildPanel(self):
        i = 0
        section = self.ActiveBuildSection
        for k,v in self.buildingsDB[section].items():
            newBlueprint = DirectButton(
                frameColor=(0.15, 0.15, 0.15, 0.9),
                frameSize=(-0.4, 0.4, -0.125, 0.125), relief='flat',
                text=k, text_fg=(0,0,0,0),
                pos=(0, 0, 0.53-i*0.25), parent=self.PlanetBuildPanel,
                command=self.switchBuildBlueprint)
            newBlueprint['extraArgs']=[newBlueprint,v]
            self.PlanetBuildPanelContent.append(newBlueprint)

            newImage = OnscreenImage(image=v['img'], pos=(-0.27, 0, 0.003), scale=(0.125, 1, 0.12),
                                     parent=(newBlueprint))

            newTitle = DirectLabel(text=k, 
            pos=(-0.1, 0, 0.05), text_fg=(1,1,1,1), frameColor=(0,0,0,0), 
            parent = newBlueprint, text_align=TextNode.ALeft, text_scale = 0.06)

            newAttributes = DirectLabel(text=('Price: ' + str(v['Price'])), 
            pos=(-0.1, 0, -0.02), text_fg=(1,1,1,1), frameColor=(0,0,0,0), 
            parent = newBlueprint, text_align=TextNode.ALeft, text_scale = 0.045)

            newRuler = DirectFrame(frameColor=(0,0,0,0.9), frameSize=(-0.4, 0.4, -0.003, 0.003),
            pos=(0,0,-0.12), parent=newBlueprint)

            i+=1
    
    def constructBuilding(self):
        planet = self.selectedObjectName
        section = self.ActiveBuildSection
        slot = self.ActiveBuildSlot['text']
        blueprint = self.ActiveBlueprint['text']
        price = self.buildingsDB[section][blueprint]['Price']
        enrgCap = self.planetDB[planet]['enrgCap']
        enrgUsg = self.planetDB[planet]['enrgUsg']

        getsBuild = False
        addTask = False

        if self.money >= price:
            if section == 'ENRG':
                getsBuild = True
                self.planetDB[planet]['enrgCap']+=self.buildingsDB[section][blueprint]['incVal']
            else:
                if enrgUsg + self.buildingsDB[section][blueprint]['enrgDrain'] <= enrgCap:
                    if section == 'RESC':
                        if self.buildingsDB[section][blueprint]['req'] in self.planetDB[planet]['resc']:
                            getsBuild = True
                            addTask = True
                        else:
                            self.createProblemDialog('Needed Rescource is not available')
                    elif section == 'PROD':
                        getsBuild = True
                        addTask = True
                        self.planetDB[planet]['enrgUsg']+=self.buildingsDB[section][blueprint]['enrgDrain']
                    elif section == 'HAB':
                        getsBuild = True
                        self.planetDB[planet]['habCap']+=self.buildingsDB[section][blueprint]['incVal']
                        self.planetDB[planet]['enrgUsg']+=self.buildingsDB[section][blueprint]['enrgDrain']
                else:
                    self.createProblemDialog('Not sufficient Energy')
        else:
            self.createProblemDialog('Not enough Money')
        
        if getsBuild:
            self.planetDB[planet]['slots'][section][slot] = blueprint
            self.money -= price
            self.updateBuildingLables()

        if addTask:
            good = self.buildingsDB[section][blueprint]['Yield']
            incVal = self.buildingsDB[section][blueprint]['incVal']
            taskMgr.doMethodLater(5, self.produceGoodTask, blueprint + slot, extraArgs=[planet,good,incVal], appendTask=True)

        self.checkForConstructButton()
        self.checkForSalvageButton()

    def salvageBuilding(self):
            planet = self.selectedObjectName
            slot = self.ActiveBuildSlot['text']
            section = self.ActiveBuildSection
            blueprint = self.planetDB[planet]['slots'][section][slot]
            price = self.buildingsDB[section][blueprint]['Price']
            
            self.planetDB[planet]['slots'][section][slot] = None
            self.money += round(price * self.salvageFactor)
            self.updateBuildingLables()
            self.checkForSalvageButton()
            
            taskMgr.remove(blueprint + slot)
            self.checkForSalvageButton()
            self.checkForConstructButton()

    def updateBuildingLables(self):
        planet = self.selectedObjectName
        section = self.ActiveBuildSection
        data = self.planetDB[planet]['slots'][section]
        fl = section[0]

        if data[fl+'1'] != None: self.PlanetBuildSlot1Lable['text'] = data[fl+'1']
        else: self.PlanetBuildSlot1Lable['text'] = ''   

        if data[fl+'2'] != None: self.PlanetBuildSlot2Lable['text'] = data[fl+'2']
        else: self.PlanetBuildSlot2Lable['text'] = '' 

        if data[fl+'3'] != None: self.PlanetBuildSlot3Lable['text'] = data[fl+'3']
        else: self.PlanetBuildSlot3Lable['text'] = '' 

        if data[fl+'4'] != None: self.PlanetBuildSlot4Lable['text'] = data[fl+'4']
        else: self.PlanetBuildSlot4Lable['text'] = '' 

        if data[fl+'5'] != None: self.PlanetBuildSlot5Lable['text'] = data[fl+'5']
        else: self.PlanetBuildSlot5Lable['text'] = '' 

    def clearBuildPanel(self):
        for element in self.PlanetBuildPanelContent:
            element.destroy()
        self.PlanetBuildPanelContent = []
        self.ActiveBlueprint = None
        self.PlanetBuildDescriptionText['text']=''

    def clearSelectedBuildSlot(self):
        if self.ActiveBuildSlot != None:
            self.ActiveBuildSlot['relief']='raised'
            self.ActiveBuildSlot = None

    def createProblemDialog(self, problemText):
        self.ProblemDialog = OkDialog(
            dialogName="OkDialog", text=problemText, command=self.cleanupProblemDialog, 
            frameColor=(0.15,0.15,0.15,0.8), text_fg=(1,1,1,1))

    def cleanupProblemDialog(self, args):
        self.ProblemDialog.cleanup()


    def produceGoodTask(self, celObj, good, incVal, task):
        if not ('goods' in self.planetDB[celObj]):
            self.planetDB[celObj].update({'goods':{}})
        if not (good in self.planetDB[celObj]['goods']):
            self.planetDB[celObj]['goods'].update({good:0})
        
        self.planetDB[celObj]['goods'][good]+=incVal
        
        return task.again

    def populatePlanetTask(self, planet, task):
        if self.planetDB[planet]['habCap'] > self.planetDB[planet]['pop']:
            self.planetDB[planet]['pop']+=random.randint(1,3)
        return task.again

    def generateMoneyTask(self, task):
        wholePop = 0
        for planet, data in self.planetDB.items():
            if data['type'] != 'Star':
                wholePop += data['pop']
        self.money += round(wholePop * self.taxFactor)
        return task.again


    #****************************************
    #       Initialisation Functions        *
    #****************************************

    def setUpGui(self):
        # Constant visible gui elements
        #------------------------------
        self.HeadGUI = OnscreenText(text='Year '+str(self.yearCounter)+', Day '+str(self.dayCounter) + ', Money: ' +str(self.money), 
            pos=(0.1, -0.1), fg=(1, 1, 1, 1),
            parent=base.a2dTopLeft,align=TextNode.ALeft, scale=.08)

        # All static gui elements for the planet info screen
        #---------------------------------------------------
        self.PlanetInfoPanel = DirectFrame(
            frameColor=(0.15, 0.15, 0.15, 0.9),
            frameSize=(-0.9, 1.1, -0.65, 0.65),
            pos=(-0.8, 0, 0))
        self.PlanetInfoPanel.hide()

        self.PlanetInfoTitle = DirectLabel(text='', pos=(-0.85, 0, 0.5), 
            text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = self.PlanetInfoPanel, 
            text_align=TextNode.ALeft, text_scale = 0.13)

        self.PlanetInfoAttributesTable = DirectLabel(text='', pos=(-0.85, 0, 0.4), 
            text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = self.PlanetInfoPanel, 
            text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)

        self.PlanetInfoRescourceTable = DirectLabel(text='', pos=(-0.85, 0, 0), 
            text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = self.PlanetInfoPanel, 
            text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)
        
        self.PlanetInfoGoodsTable = DirectLabel(text='', pos=(-0.85, 0, -0.35), 
            text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = self.PlanetInfoPanel, 
            text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)

        self.PlanetInfoENRGTable = DirectLabel(text='', pos=(0.28, 0, 0.4), 
            text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = self.PlanetInfoPanel, 
            text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)

        self.PlanetInfoCloseButton = DirectButton(text='Close', 
            pos=(-0.745,0,0.7), pad=(0.05, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.togglePlanetInfoMode, extraArgs=[False])
        self.PlanetInfoCloseButton.reparentTo(self.PlanetInfoPanel)

        self.PlanetInfoBuildButton = DirectButton(text='Build', 
            pos=(1.8,0,-0.58), pad=(0.06, 0.05), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.togglePlanetBuildMode, extraArgs=[True])
        self.PlanetInfoBuildButton.reparentTo(self.PlanetInfoPanel)

        # All static gui elements for the planet build panel
        #---------------------------------------------------
        self.PlanetBuildPanel = DirectFrame(
            frameColor=(0.15, 0.15, 0.15, 0.9),
            frameSize=(-0.4, 1.23, 0.66, -0.65),
            pos=(-1.3, 0, 0))
        self.PlanetBuildPanel.hide()

        self.PlanetBuildPanelContent = []

        self.PlanetBuildPanelRuler = DirectFrame(frameColor=(0,0,0,0.9), frameSize=(-0.003, 0.003, -1.305, 0),
            pos=(0.408,0,0.657), parent=self.PlanetBuildPanel)

        self.PlanetBuildDescriptionField = DirectFrame(
            frameColor=(0.2, 0.2, 0.22, 0.9),
            frameSize=(-0.4, 0.4, 0.25, -0.25),
            pos=(0.825, 0, 0.41), parent=self.PlanetBuildPanel)

        self.PlanetBuildDescriptionText = DirectLabel(text='', 
            pos=(-0.36, 0, 0.18), text_fg=(1,1,1,1), frameColor=(0,0,0,0), text_scale = 0.05, text_wordwrap=15,
            frameSize=(0,0.8,0,0.5), parent = self.PlanetBuildDescriptionField, text_align=TextNode.ALeft)

        self.PlanetBuildConstructButton = DirectButton(text='Construct ->', 
            pos=(-0.122,0,-0.37), pad=(0.05, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.constructBuilding, parent=self.PlanetBuildDescriptionField, state='disabled')

        self.PlanetBuildSalvageButton  = DirectButton(text='<- Salvage', 
            pos=(-0.126,0,-0.52), pad=(0.085, 0.013), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.salvageBuilding, parent=self.PlanetBuildDescriptionField, state='disabled')

        self.PlanetBuildCloseButton = DirectButton(text='Back', 
            pos=(-0.26,0,0.7), pad=(0.05, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.togglePlanetBuildMode, extraArgs=[False], parent=self.PlanetBuildPanel)

        self.PlanetBuildSectionDropdown = DirectOptionMenu(text="options", 
            pos=(-0.1,0,0.68),pad=(1.7, 1), borderWidth=(0.06,0.06),
            scale=0.15, text_scale=0.5, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            items=["RESC", "PROD", "ENRG", "DEV", "HAB"], command=self.switchBuildSection, 
            initialitem=0, highlightColor=(0.65, 0.65, 0.65, 1), parent=self.PlanetBuildPanel)

        self.PlanetBuildQuickInfo = DirectFrame(frameSize=(0, 1.63, -0.08, 0.07), pos=(-0.4,0,-0.73),
            frameColor=(0.15, 0.15, 0.15, 0.9), parent=self.PlanetBuildPanel)

        self.PlanetBuildQuickText1 = DirectLabel(text='ATHM: Yes  -  WIND: 1  -  HAB: 20/100  -  ENRG: 60/100', 
            pos=(0.03, 0, 0.015), text_fg=(0.9,0.9,0.9,1), frameColor=(0,0,0,0), text_scale = 0.05,
            frameSize=(0,0.8,0,0.5), parent=self.PlanetBuildQuickInfo, text_align=TextNode.ALeft)
        
        self.PlanetBuildQuickText2 = DirectLabel(text='RESC: Cole, Iron, Uranium', 
            pos=(0.03, 0, -0.038), text_fg=(0.9,0.9,0.9,1), frameColor=(0,0,0,0), text_scale = 0.05,
            frameSize=(0,0.8,0,0.5), parent=self.PlanetBuildQuickInfo, text_align=TextNode.ALeft)

        self.PlanetBuildQuickText3 = DirectLabel(text='GOODS: Cole sacks, Uranium rods', 
            pos=(0.7, 0, -0.038), text_fg=(0.9,0.9,0.9,1), frameColor=(0,0,0,0), text_scale = 0.05,
            frameSize=(0,0.8,0,0.5), parent=self.PlanetBuildQuickInfo, text_align=TextNode.ALeft)

        # All static gui elements for the planet build slots
        #---------------------------------------------------
        self.PlanetBuildSlotContainer = DirectFrame(pos=(1.45,0,0), frameColor=(0.5,0.5,0.5,1))
        self.PlanetBuildSlotContainer.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildSlot1 = DirectButton(text='R1', 
            pos=(0.45,0,0.65), hpr=(0,0,45), pad=(0.05, 0.05), borderWidth=(0.02,0.02),
            text_scale=0.06, frameColor=(0.2,0.2,0.2,1), text_fg=(1,1,1,1), text_roll=45,
            command=self.switchBuildSlot, parent=self.PlanetBuildSlotContainer)
        self.PlanetBuildSlot1['extraArgs'] = [self.PlanetBuildSlot1]
        self.PlanetBuildSlot1Lable = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1), text_bg=(0.2,0.2,0.2,0.9),
            frameColor=(0,0,0,0), hpr=(0,0,-45), pos=(-0.07,0,0.07), parent=self.PlanetBuildSlot1)

        self.PlanetBuildSlot2 = DirectButton(text='R2', 
            pos=(0.17,0,0.39), hpr=(0,0,45), pad=(0.05, 0.05), borderWidth=(0.02,0.02),
            text_scale=0.06, frameColor=(0.2,0.2,0.2,1), text_fg=(1,1,1,1), text_roll=45,
            command=self.switchBuildSlot, parent=self.PlanetBuildSlotContainer)
        self.PlanetBuildSlot2['extraArgs'] = [self.PlanetBuildSlot2]
        self.PlanetBuildSlot2Lable = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
            frameColor=(0,0,0,0), hpr=(0,0,-45), pos=(-0.07,0,0.07), parent=self.PlanetBuildSlot2)

        self.PlanetBuildSlot3 = DirectButton(text='R3', 
            pos=(0.05,0,0), hpr=(0,0,45), pad=(0.05, 0.05), borderWidth=(0.02,0.02),
            text_scale=0.06, frameColor=(0.2,0.2,0.2,1), text_fg=(0.5,0.5,0.5,1), text_roll=45,
            command=self.switchBuildSlot, parent=self.PlanetBuildSlotContainer, state='disabled')
        self.PlanetBuildSlot3['extraArgs'] = [self.PlanetBuildSlot3]
        self.PlanetBuildSlot3Lable = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
            frameColor=(0,0,0,0), hpr=(0,0,-45), pos=(-0.07,0,0.07), parent=self.PlanetBuildSlot3)

        self.PlanetBuildSlot4 = DirectButton(text='R4', 
            pos=(0.17,0,-0.39), hpr=(0,0,45), pad=(0.05, 0.05), borderWidth=(0.02,0.02),
            text_scale=0.06, frameColor=(0.2,0.2,0.2,1), text_fg=(0.5,0.5,0.5,1), text_roll=45,
            command=self.switchBuildSlot, parent=self.PlanetBuildSlotContainer, state='disabled')
        self.PlanetBuildSlot4['extraArgs'] = [self.PlanetBuildSlot4]
        self.PlanetBuildSlot4Lable = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
            frameColor=(0,0,0,0), hpr=(0,0,-45), pos=(-0.07,0,0.07), parent=self.PlanetBuildSlot4)

        self.PlanetBuildSlot5 = DirectButton(text='R5', 
            pos=(0.45,0,-0.65), hpr=(0,0,45), pad=(0.05, 0.05), borderWidth=(0.02,0.02),
            text_scale=0.06, frameColor=(0.2,0.2,0.2,1), text_fg=(0.5,0.5,0.5,1), text_roll=45,
            command=self.switchBuildSlot, parent=self.PlanetBuildSlotContainer, state='disabled')
        self.PlanetBuildSlot5['extraArgs'] = [self.PlanetBuildSlot5]
        self.PlanetBuildSlot5Lable = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
            frameColor=(0,0,0,0), hpr=(0,0,-45), pos=(-0.07,0,0.07), parent=self.PlanetBuildSlot5)


        #self.PlanetBuildWire1 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(0,1,0,1),
        #    pos=(1.7,-0.5,-0.035))
        #self.PlanetBuildWire1.reparentTo(self.PlanetBuildSlotContainer)

        #self.PlanetBuildWire2 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(1,0,0,1),
        #    pos=(1.4,-0.5, 0.165))
        #self.PlanetBuildWire2.reparentTo(self.PlanetBuildSlotContainer)

        #self.PlanetBuildWire3 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(1,0,0,1),
        #    pos=(1.4,-0.5,-0.235))
        #self.PlanetBuildWire3.reparentTo(self.PlanetBuildSlotContainer)

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
        self.sun.setTag('clickable', 'yes')
        self.sun.setTag('name', 'sun')

        self.planetDB.update({'mercury':{
            'name':'Mercury',   'scale':0.385,  'dist':0.38, 
            'type':'Planet',    'athm':False,   'wind':1, 
            'enrgCap':0,        'enrgUsg':0,    'pop':0,
            'habCap':0,
            'resc':{'Coal':'Common', 'Iron':'Common'} }})
        self.mercury = loader.loadModel("models/planet_sphere")
        self.mercury_tex = loader.loadTexture("models/mercury_1k_tex.jpg")
        self.mercury.setTexture(self.mercury_tex, 1)
        self.mercury.reparentTo(self.orbit_root_mercury)
        self.mercury.setPos(self.planetDB['mercury']['dist'] * self.orbitscale, 0, 0)
        self.mercury.setScale(self.planetDB['mercury']['scale'] * self.sizescale)
        self.mercury.setTag('clickable', 'yes')
        self.mercury.setTag('name', 'mercury')
        
        self.planetDB.update({'venus':{
            'name':'Venus',     'scale':0.923,  'dist':0.72, 
            'type':'Planet',    'athm':False,   'wind':2, 
            'enrgCap':0,        'enrgUsg':0,    'pop':0,
            'habCap':0,
            'resc':{'Coal':'Common', 'Uranium':'Normal'} }})
        self.venus = loader.loadModel("models/planet_sphere")
        self.venus_tex = loader.loadTexture("models/venus_1k_tex.jpg")
        self.venus.setTexture(self.venus_tex, 1)
        self.venus.reparentTo(self.orbit_root_venus)
        self.venus.setPos(self.planetDB['venus']['dist'] * self.orbitscale, 0, 0)
        self.venus.setScale(self.planetDB['venus']['scale'] * self.sizescale)
        self.venus.setTag('clickable', 'yes')
        self.venus.setTag('name', 'venus')

        self.planetDB.update({'mars':{
            'name':'Mars',      'scale':0.512,  'dist':1.52, 
            'type':'Planet',    'athm':False,   'wind':1, 
            'enrgCap':0,        'enrgUsg':0,    'pop':0,
            'habCap':0,
            'resc':{'Gemstone':'Rare', 'Iron':'Rare'} }})
        self.mars = loader.loadModel("models/planet_sphere")
        self.mars_tex = loader.loadTexture("models/mars_1k_tex.jpg")
        self.mars.setTexture(self.mars_tex, 1)
        self.mars.reparentTo(self.orbit_root_mars)
        self.mars.setPos(self.planetDB['mars']['dist'] * self.orbitscale, 0, 0)
        self.mars.setScale(self.planetDB['mars']['scale'] * self.sizescale)
        self.mars.setTag('clickable', 'yes')
        self.mars.setTag('name', 'mars')

        self.planetDB.update({'earth':{
            'name':'Earth',     'scale':1,      'dist':1, 
            'type':'Planet',    'athm':True,    'wind':1, 
            'enrgCap':0,        'enrgUsg':0,    'pop':0,
            'habCap':0,
            'resc':{'Iron':'Normal', 'Cole':'Common', 'Gemstone':'Rare'} }})
        self.earth = loader.loadModel("models/planet_sphere")
        self.earth_tex = loader.loadTexture("models/earth_1k_tex.jpg")
        self.earth.setTexture(self.earth_tex, 1)
        self.earth.reparentTo(self.orbit_root_earth)
        self.earth.setScale(self.planetDB['earth']['scale'] * self.sizescale)
        self.earth.setPos(self.planetDB['earth']['dist'] * self.orbitscale, 0, 0)
        self.earth.setTag('clickable', 'yes')
        self.earth.setTag('name', 'earth')

        self.orbit_root_moon.setPos(self.orbitscale, 0, 0)

        self.planetDB.update({'moon':{
            'name':'Moon',      'scale':0.1,    'dist':0.1, 
            'type':'Moon',      'athm':False,   'wind':0, 
            'enrgCap':0,        'enrgUsg':0,    'pop':0,
            'habCap':0,
            'resc':{'Coal':'Common', 'Cheese':'Rare'} }})
        self.moon = loader.loadModel("models/planet_sphere")
        self.moon_tex = loader.loadTexture("models/moon_1k_tex.jpg")
        self.moon.setTexture(self.moon_tex, 1)
        self.moon.reparentTo(self.orbit_root_moon)
        self.moon.setScale(0.1 * self.sizescale)
        self.moon.setPos(0.1 * self.orbitscale, 0, 0)
        self.moon.setTag('clickable', 'yes')
        self.moon.setTag('name', 'moon')

    def prepareSlotsInPlanetDB(self):
        for planet, data in self.planetDB.items():
            self.planetDB[planet].update({'slots':{
                'RESC':{'R1':None, 'R2':None, 'R3':None, 'R4':None, 'R5':None},
                'PROD':{'P1':None, 'P2':None, 'P3':None, 'P4':None, 'P5':None},
                'ENRG':{'E1':None, 'E2':None, 'E3':None, 'E4':None, 'E5':None},
                'DEV': {'D1':None, 'D2':None, 'D3':None, 'D4':None, 'D5':None},
                'HAB': {'H1':None, 'H2':None, 'H3':None, 'H4':None, 'H5':None}
            }})

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

    def fillBuildingsDB(self):
        self.buildingsDB = {
            'RESC':{
                'Cole Drill': {     'Price':300, 'Time':60, 'Yield':'Cole sacks', 'incVal':10, 'yieldText':'10 Cole sacks per tick', 
                                    'req':'Cole', 'decVal':0, 'reqText':'Cole, 100 Energy', 'enrgDrain': 100, 
                                    'desc':'Simple mining drill to extract cole rescources of a planet.', 
                                    'img':'models/coledrill.jpg'},

                'Iron Mine': {      'Price':450, 'Time':100, 'Yield':'Iron ingots', 'incVal':15, 'yieldText':'15 Iron ingots per tick',
                                    'req':'Iron', 'decVal':0, 'reqText':'Iron, 150 Energy', 'enrgDrain': 150, 
                                    'desc':'Sophisticated mine to faciliate iron, which is used for further Production.', 
                                    'img':'models/ironmine.jpg'},

                'Uranium Site': {   'Price':600, 'Time':300, 'Yield':'Uranium containers', 'incVal':5, 'yieldText':'5 Uranium containters per tick',
                                    'req':'Uranium', 'decVal':0, 'reqText':'Uranium, 500 Energy', 'enrgDrain': 500, 
                                    'desc':'High tech facility to gather raw uranium. This has then to be enriched for further use.', 
                                    'img':'models/placeholder.jpg'},

                'Organic Farm': {   'Price':250, 'Time':60, 'Yield':'Vegetable crates', 'incVal':20, 'yieldText':'20 Vegetable crates per tick',
                                    'req':'Athmosphere', 'decVal':0, 'reqText':'Athmosphere, 200 Energy', 'enrgDrain': 200, 
                                    'desc':'Basic vegetable farm to satisfy nutrition needs.', 
                                    'img':'models/placeholder.jpg'}
            },
            'PROD':{
                'Weapon Forge': {   'Price':500, 'Time':120, 'Yield':'Weapons', 'incVal':10, 'yieldText':'10 Weapons per tick',
                                    'req':'Iron ingots', 'decVal':10, 'reqText':'10 Iron ingots per tick, 250 Energy', 'enrgDrain': 250, 
                                    'desc':'Simple mining drill to extract cole rescources of a planet.', 
                                    'img':'models/placeholder.jpg'},

                'Ship Yard': {      'Price':550, 'Time':130, 'Yield':'Ships', 'incVal':10, 'yieldText':'10 Ships per tick',
                                    'req':'Iron ingots', 'decVal':30, 'reqText':'30 Iron ingots per tick, 250 Energy', 'enrgDrain': 300, 
                                    'desc':'Simple mining drill to extract cole rescources of a planet.', 
                                    'img':'models/placeholder.jpg'},

                'Uranium Enricher':{'Price':750, 'Time':400, 'Yield':'Uranium rods', 'incVal':10, 'yieldText':'10 Uranium rods per tick',
                                    'req':'Uranium containers', 'decVal':5, 'reqText': '5 Uranium container per tick, 650 Energy','enrgDrain': 650, 
                                    'desc':'Simple mining drill to extract cole rescources of a planet.', 
                                    'img':'models/placeholder.jpg'}
            },
            'ENRG':{
                'Wind Turbine': {   'Price':150, 'Time':30, 'Yield':'Energy', 'incVal':150, 'yieldText':'150 Energy',
                                    'req':'Wind', 'decVal':0, 'reqText':'Wind',
                                    'desc':'First instance of energy supply. Needs at least level 1 Wind activities.', 
                                    'img':'models/windgenerator.jpg'},

                'Cole Generator': { 'Price':300, 'Time':50, 'Yield':'Energy', 'incVal':500, 'yieldText':'500 Energy', 
                                    'req':'Cole sacks', 'decVal':5, 'reqText':'5 Cole sacks per tick',
                                    'desc':'Delivers bigger and more reliable energy output. Polution might be a Prolbem though.', 
                                    'img':'models/coleplant.jpg'},

                'M.W. Transmitter':{'Price':650, 'Time':250, 'Yield':'Energy', 'incVal':1000, 'yieldText':'1000 Energy', 
                                    'req':'Micro waves', 'decVal':0, 'reqText':'Micro wave connection to other planet',
                                    'desc':'Enables multiple Planents to send energy supply to each other.', 
                                    'img':'models/mw_transmitter.jpg'},

                'Nuclear Reactor': {'Price':850, 'Time':350, 'Yield':'Energy', 'incVal':5000, 'yieldText':'5000 Energy', 
                                    'req':'Uranium rods', 'decVal':7, 'reqText':'7 Uranium rods per tick',
                                    'desc':'Highest energy source that can be constructed planet site.', 
                                    'img':'models/powerplant.jpg'},

                'Dyson Sphere': {   'Price':3200, 'Time':600, 'Yield':'Energy', 'incVal':50000, 'yieldText':'50000 Energy', 
                                    'req':'Sun', 'decVal':0, 'reqText':'Sun as center of construction',
                                    'desc':'Experimental construction, which others refer to as the newest wonder of the known worlds.', 'img':'models/dysonsphere.jpg'}
            },
            'DEV':{
                'Trading Center': { 'Price':575, 'Time':300, 'Yield':'Trading ability', 'incVal':0, 'yieldText':'Trading ability',
                                    'req':None, 'decVal':0, 'reqText':'450 Energy', 'enrgDrain': 450,
                                    'desc':'Allows to set trading routes and to trade with the open galaxy market. Only one needed per solar system.', 
                                    'img':'models/placeholder.jpg'},
                
                'Milkyway Uni.': {  'Price':350, 'Time':200, 'Yield':'Society improvements', 'incVal':0, 'yieldText':'Society improvements',
                                    'req':None, 'decVal':0, 'reqText':'240 Energy', 'enrgDrain': 240,
                                    'desc':'Simple mining drill to extract cole rescources of a planet.', 
                                    'img':'models/placeholder.jpg'},
                
                'Science Institut':{'Price':500, 'Time':280, 'Yield':'New researches', 'incVal':0, 'yieldText':'New researches',
                                    'req':None, 'decVal':0, 'reqText':'310 Energy', 'enrgDrain': 310,
                                    'desc':'Researches conducted by this institute allow enhancements of productivity and habitation standards.', 
                                    'img':'models/placeholder.jpg'},
                
                'Space Port': {     'Price':190, 'Time':150, 'Yield':'Space abilities', 'incVal':0, 'yieldText':'Space abilities',
                                    'req':None, 'decVal':0, 'reqText':'560 Energy', 'enrgDrain': 560,
                                    'desc':'Extends the interactions of a planet with its surrounding objects like asteroids or other celestial objects.', 
                                    'img':'models/placeholder.jpg'}
            },
            'HAB':{
                'Pod Settlement': { 'Price':120, 'Time':30, 'Yield':'Nomads', 'incVal':100, 'yieldText': '100 Nomads',
                                    'req':None, 'decVal':0, 'reqText':'120 Energy', 'enrgDrain': 120, 
                                    'desc':'Simple mining drill to extract cole rescources of a planet.', 
                                    'img':'models/placeholder.jpg'},
                
                'Skyscraper City': {'Price':400, 'Time':230, 'Yield':'900 Nomads', 'incVal':900,  'yieldText': '900 Nomads',
                                    'req':'Autom. Hospital', 'decVal':0, 'reqText':'Autom. Hospital, 290 Energy', 'enrgDrain': 290, 
                                    'desc':'Simple mining drill to extract cole rescources of a planet.', 
                                    'img':'models/placeholder.jpg'},
                
                'Sol Resort': {     'Price':625, 'Time':240, 'Yield':'Tourism ability', 'incVal':0, 'yieldText': 'Tourism ability',
                                    'req':'Skyscraper City', 'decVal':0, 'reqText':'Skyscraper City, 360 Energy', 'enrgDrain': 360, 
                                    'desc':'Simple mining drill to extract cole rescources of a planet.', 
                                    'img':'models/placeholder.jpg'},
                
                'Autom. Hospital': {'Price':350, 'Time':200, 'Yield':'TBD', 'incVal':0, 'yieldText': 'TBD',
                                    'req':None, 'decVal':0, 'reqText':'230 Energy', 'enrgDrain': 230, 
                                    'desc':'Simple mining drill to extract cole rescources of a planet.', 
                                    'img':'models/placeholder.jpg'}
            }
        }


    #****************************************
    #             Debug Functions           *
    #****************************************


# end class world

w = World()
base.run()