from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from panda3d.core import *

import math
from planetBuildView import PlanetBuildView


class PlanetInfoView():

    def __init__(self, world):
        self.world = world
        self.selectedObject = None
        self.selectedObjectName = None
        self.planetData = None
        self.followObjectScale = None
        self.NewPlanetBuildView = None
        self.messagesDict = {}

        self.createGui()
        
    def reset(self, obj):
        self.clear()

        self.selectedObject = obj
        self.selectedObjectName = obj.getNetTag('name')
        self.planetData = self.world.planetDB[self.selectedObjectName]
        self.followObjectScale = self.planetData['scale']
        self.NewPlanetBuildView = self.world.NewPlanetBuildView

        self.fill()
        taskMgr.doMethodLater(1, self.UpdateTask, 'updatePlanetInfoTask')
        self.checkButtons()
        self.loadMessages()
    
    def fill(self):
        # Fills the content of the planet info gui every time a planet gets selected

        objID = self.selectedObjectName
        self.PlanetInfoTitle['text']=self.planetData['name']

        if self.planetData['type']=='Star' or self.planetData['probed']:
            PlanetInfoAttributesText = (
                'Type:\t\t' + str(self.planetData['type']) + '\n'
                'Diameter:\t\t' + str(self.planetData['scale'] * 10**5) + '\n')
            if self.planetData['type'] != "Star":
                PlanetInfoAttributesText += (
                    'Distance to Sun:\t' + str(self.planetData['dist'] * 10**7) + '\n'
                    'Athmosphere:\t' + str(self.planetData['athm']) + '\n'
                    'Windstrength:\t' + str(self.planetData['wind']) + '\n')

            self.PlanetInfoAttributesTable['text']=PlanetInfoAttributesText


            if self.planetData['type'] != "Star":
                PlanetInfoRescourceText = 'Rescources:\n'
                for k,v in self.planetData['resc'].items():
                    PlanetInfoRescourceText += k + ':\t\t' + str(v) + '\n'

                self.PlanetInfoRescourceTable['text']=PlanetInfoRescourceText

                if 'goods' in self.planetData:
                    PlanetInfoGoodsText = 'Goods:\n'
                    for k,v in self.planetData['goods'].items():
                        PlanetInfoGoodsText += k + ':\t' + str(v) + '\n'

                    self.PlanetInfoGoodsTable['text']=PlanetInfoGoodsText
                
                self.PlanetInfoENRGTable['text']=(
                    'Energy capacity:\t' + str(self.planetData['enrgCap']) + '\n'
                    'Energy usage:\t' + str(self.planetData['enrgUsg']) + '\n\n'
                    
                    'Habitation capacity:\t' + str(self.planetData['habCap']) + '\n'
                    'Population count:\t' + str(self.planetData['pop']) + '\n\n'

                    'Per Capita GDP:\t' + str(self.world.taxFactor)
                )
        else:
            self.PlanetInfoAttributesTable['text']='???'

    def UpdateTask(self, task):
        self.fill()
        self.checkButtons()
        self.emptyMessages()
        self.loadMessages()
        return task.again

    def clear(self):
        self.PlanetInfoTitle['text']='Unknown'
        self.PlanetInfoAttributesTable['text']=''
        self.PlanetInfoRescourceTable['text']=''
        self.PlanetInfoGoodsTable['text']=''
        self.PlanetInfoENRGTable['text']=''

        self.emptyMessages()

    def show(self):
        self.PlanetInfoPanel.show()

    def hide(self):
        self.PlanetInfoPanel.hide()

    def checkButtons(self):
        if self.planetData['type'] == 'Star':
            self.PlanetInfoBuildButton.hide()
            self.PlanetInfoColoniseButton.hide()
            self.PlanetInfoProbeButton.hide()
            return
        
        if self.planetData['colonised']:
            self.PlanetInfoBuildButton.show()
            self.PlanetInfoColoniseButton.hide()
            self.PlanetInfoProbeButton.hide()
        elif self.planetData['probed']:
            self.PlanetInfoBuildButton.hide()
            self.PlanetInfoColoniseButton.show()
            self.PlanetInfoProbeButton.hide()
        else:
            self.PlanetInfoBuildButton.hide()
            self.PlanetInfoColoniseButton.hide()
            self.PlanetInfoProbeButton.show()

    def loadMessages(self):
        if 'messages' in self.world.planetDB[self.selectedObjectName]:
            i=0
            for id, message in self.world.planetDB[self.selectedObjectName]['messages'].items():
                mText = message['text'] + '\n' + str(message['value'])
                
                msgPanel = DirectFrame(
                    pos=(0, 0, 0.35-i*0.21), frameColor=(0.2, 0.2, 0.3, 0.2), frameSize=(-0.2, 0.2, -0.1, 0.1), text_pos=(0,0.05),
                    parent=self.PlanetInfoMessagePanel, text=mText, text_scale=0.05, text_fg = (1,1,1,1), text_wordwrap=8)
                
                self.messagesDict.update({id: msgPanel})
                i+=1
    
    def emptyMessages(self):
        for id, panel in self.messagesDict.items():
            panel.destroy()
        self.messagesDict = {}


    def showProbeMission(self):
            planet1 = self.world.capitalPlanet
            planet2 = self.selectedObject
            name = self.selectedObjectName
            dist = round(self.world.calcDistanceBetweenPlanets(planet1, planet2),3)
            time = round(dist * 15)
            cost = 500 + round(dist * 67)
            missionText = "Probe misson to {}:\nDistance: {}\nDuration: {}\nCosts: {}".format(name,dist,time,cost)
            self.world.createProblemDialog(missionText, 'yesNo', self.startProbeMission, [planet1, planet2, name, dist, time, cost])

    def startProbeMission(self, planet1, planet2, name, dist, time, cost):
        id = 'probe' + planet2.getNetTag('name')
        self.world.addMessage(planet2, id, 'info', 'Probing Mission', time)
        taskMgr.doMethodLater(1, self.probeMissionTask, 'probeMissionTask', extraArgs=[planet2, id], appendTask=True)
        if self.world.money >= cost:
            self.world.money-=cost
        else:
            self.world.createProblemDialog("Not enough Money")

    def probeMissionTask(self, planet2, id, task):
        planetName = planet2.getNetTag('name')
        if self.world.planetDB[planetName]['messages'][id]['value'] > 0:
            self.world.planetDB[planetName]['messages'][id]['value']-=1
        else:
            self.world.planetDB[planetName].update({'probed':True})
            self.world.planetDB[planetName]['messages'].pop(id)
            return task.done
        return task.again


    def showColoniseMission(self):
        planet1 = self.world.capitalPlanet
        planet2 = self.selectedObject
        name = self.selectedObjectName
        dist = round(self.world.calcDistanceBetweenPlanets(planet1, planet2),3)
        time = round(dist * 30)
        cost = 3900 + round(dist * 123)
        missionText = "Colonise misson to {}:\nDistance: {}\nDuration: {}\nCosts: {}".format(name,dist,time,cost)
        self.world.createProblemDialog(missionText, 'yesNo', self.startColoniseMission, [planet1, planet2, name, dist, time, cost])

    def startColoniseMission(self, planet1, planet2, name, dist, time, cost):
        if self.world.money >= cost:
            self.world.money-=cost
            id = 'colonise' + planet2.getNetTag('name')
            self.world.addMessage(planet2, id, 'info', 'Colonise Mission', time)
            taskMgr.doMethodLater(1, self.coloniseMissionTask, 'coloniseMissionTask', extraArgs=[planet1, planet2, id, name, dist, time, cost], appendTask=True)
        else:
            self.world.createProblemDialog("Not enough Money")

    def coloniseMissionTask(self, planet1, planet2, id, name, dist, time, cost, task):
        planetName = planet2.getNetTag('name')
        if self.world.planetDB[planetName]['messages'][id]['value'] > 0:
            self.world.planetDB[planetName]['messages'][id]['value']-=1
        else:
            self.world.planetDB[planetName].update({'colonised':True})
            self.world.planetDB[planetName]['messages'].pop(id)
            taskMgr.doMethodLater(self.world.PopulationTimeDelta, 
                                  self.world.populatePlanetTask, 
                                  'populatePlanetTask', 
                                  extraArgs=[planetName], 
                                  appendTask=True)
            return task.done
        return task.again


    def togglePlanetBuildMode(self, mode=False):
        pos = self.selectedObject.getPos(base.render)
        camPos = camera.getPos()
        obj = self.selectedObject
        scale = self.followObjectScale

        if mode:
            self.hide()
            self.clear()
            taskMgr.remove('infocamTask')

            zoomInterval = Sequence(
                Func(self.NewPlanetBuildView.reset, obj),
                camera.posHprInterval(0.3, Point3(pos[0]-scale * 0.9, pos[1]-scale * 3.4, 0), Vec3(0,0,0), camPos),
                Func(self.NewPlanetBuildView.show))
            zoomInterval.start()

            taskMgr.add(self.world.followCam, 'buildcamTask', extraArgs=[obj, scale, 'build'], appendTask=True)
            taskMgr.add(self.NewPlanetBuildView.refreshTask, 'quickinfoTask', extraArgs=[self.selectedObjectName], appendTask=True)

        else:
            self.NewPlanetBuildView.hide()
            self.NewPlanetBuildView.clear()
            taskMgr.remove('quickinfoTask')
            taskMgr.remove('buildcamTask')

            zoomInterval = Sequence(
                Func(self.reset, obj),
                camera.posHprInterval(0.3, Point3(pos[0]-scale * 1.25, pos[1]-scale * 4, scale * 4), Vec3(0,-45,0), camPos),
                Func(self.show))
            zoomInterval.start()
            
            taskMgr.add(self.world.followCam, 'infocamTask', extraArgs=[obj, scale, 'info'], appendTask=True)

        return None

    def createGui(self):
        self.infoPanelMap = loader.loadModel('models/gui/panels/planetinfopanel_maps.egg').find('**/planetinfopanel')
        self.problemPanelMap = loader.loadModel('models/gui/panels/planetproblempanel_maps.egg').find('**/planetproblempanel')

        self.PlanetInfoPanel = DirectFrame(
            pos=(-0.8, 0, 0), frameColor=(0.2, 0.2, 0.22, 0), frameSize=(-0.9, 1.1, -0.65, 0.65),
            geom=self.infoPanelMap, geom_scale=(0.65,0,0.65), geom_pos=(0.1,0,0), enableEdit=1)
        self.PlanetInfoPanel.hide()

        self.PlanetInfoTitle = DirectLabel(text='', pos=(0.1, 0, 0.5), 
            text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = self.PlanetInfoPanel, 
            text_align=TextNode.ACenter, text_scale = 0.12)

        self.PlanetInfoAttributesTable = DirectLabel(text='', pos=(-0.85, 0, 0.35), 
            text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = self.PlanetInfoPanel, 
            text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)

        self.PlanetInfoRescourceTable = DirectLabel(text='', pos=(-0.85, 0, -0.05), 
            text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = self.PlanetInfoPanel, 
            text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)
        
        self.PlanetInfoGoodsTable = DirectLabel(text='', pos=(-0.85, 0, -0.4), 
            text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = self.PlanetInfoPanel, 
            text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)

        self.PlanetInfoENRGTable = DirectLabel(text='', pos=(0.28, 0, 0.35), 
            text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = self.PlanetInfoPanel, 
            text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)

        self.PlanetInfoCloseButton = DirectButton(text='Close', 
            pos=(-0.68,0,-0.85), scale=0.5, pad=(-0.1, -0.09), frameColor=(0,0,0,0),
            text_scale=0.15, text_pos=(0,-0.03), text_fg=(1,1,1,1), geom_scale=(0.7,0,1),
            command=self.world.togglePlanetInfoMode, extraArgs=[False], parent=self.PlanetInfoPanel,
            geom=(self.world.buttonMaps))

        self.PlanetInfoProbeButton = DirectButton(text='Probe', 
            pos=(1.45,0,0.55), pad=(0.055, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.07, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.showProbeMission, parent=self.PlanetInfoPanel)

        self.PlanetInfoColoniseButton = DirectButton(text='Colonise', 
            pos=(1.85,0,0.55), pad=(0.03, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.07, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.showColoniseMission, parent=self.PlanetInfoPanel)

        self.PlanetInfoBuildButton = DirectButton(text='Build', 
            pos=(1.65,0,-0.58), scale=0.5, pad=(-0.1, -0.09), frameColor=(0,0,0,0),
            text_scale=0.15, text_pos=(0, -0.03), text_fg=(1,1,1,1), geom_scale=(0.5,0,1.2), geom=(self.world.buttonMaps),
            command=self.togglePlanetBuildMode, extraArgs=[True], parent=self.PlanetInfoPanel)

        self.PlanetInfoMessagePanel = DirectFrame(frameColor=(0.2, 0.2, 0.22, 0),
            frameSize=(0, 0, 0, 0),pos=(2.33, 0, 0.16), parent=self.PlanetInfoPanel,
            geom=self.problemPanelMap, geom_scale=(0.7,0,0.7), geom_pos=(0,0,0), enableEdit=1)