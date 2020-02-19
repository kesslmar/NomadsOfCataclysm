from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from panda3d.core import *


class PlanetBuildView():
    def __init__(self, world):
        self.world = world
        self.selectedObject = None
        self.selectedObjectName = None
        self.ActiveBuildSection = 'RESC'
        self.ActiveBlueprint = None
        self.ActiveBuildSlot = [None]
        self.PlanetBuildPanelContent = []
        self.PlanetBuildSlotButtons = []

        self.createGui()
    
    def reset(self, obj):

        self.clear()
        
        self.selectedObject = obj
        self.selectedObjectName = obj.getNetTag('name')

        self.fill()
        self.checkConstructButton()
        self.checkSalvageAndInfo()
        self.updateSlots()
        

    def show(self):
        self.PlanetBuildPanel.show()

    def hide(self):
        self.PlanetBuildPanel.hide()

    def fill(self):
        i = 0
        section = self.ActiveBuildSection
        for k,v in self.world.buildingsDB[section].items():
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

    def clear(self):
        for element in self.PlanetBuildPanelContent:
            element.destroy()
        self.PlanetBuildPanelContent = []
        self.ActiveBlueprint = None
        self.PlanetBuildDescriptionText['text']=''

        slot = self.ActiveBuildSlot[0]

        if slot != None:
            self.ActiveBuildSlot[0] = None
            self.PlanetBuildSlotButtons[int(slot)-1]['indicatorValue']=0
    
    def switchBuildSection(self, section, button):
        if section != self.ActiveBuildSection:
            self.PlanetBuildRESCButton['relief'] = 'raised'
            self.PlanetBuildPRODButton['relief'] = 'raised'
            self.PlanetBuildENRGButton['relief'] = 'raised'
            self.PlanetBuildDEVButton['relief'] = 'raised'
            self.PlanetBuildHABButton['relief'] = 'raised'
            
            button['relief']='sunken'

            self.clear()
            self.checkConstructButton()
            self.checkSalvageAndInfo()
            self.ActiveBuildSection = section

            pos = self.PlanetBuildSlotContainer.getPos()
            swipeOutInterval = self.PlanetBuildSlotContainer.posInterval(0.2, Point3(pos[0],pos[1],pos[2]+2), pos)
            swipeInInterval = self.PlanetBuildSlotContainer.posInterval(0.2, pos, Point3(pos[0],pos[1],pos[2]-2))
            
            mySeq = Sequence(swipeOutInterval, Func(self.updateSlots), swipeInInterval)      
            mySeq.start()
            self.fill()

    def switchBuildSlot(self):

        self.checkConstructButton()
        self.checkSalvageAndInfo()

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
        
        self.checkConstructButton()

    def checkConstructButton(self):
        planet=self.selectedObjectName
        section=self.ActiveBuildSection

        if self.ActiveBlueprint != None and self.ActiveBuildSlot[0] != None and self.world.planetDB[planet]['slots'][section][self.ActiveBuildSlot[0]] == None:
            self.PlanetBuildConstructButton['state']='normal'
            self.PlanetBuildConstructButton['text_fg']=(1,1,1,1)
        else:
            self.PlanetBuildConstructButton['state']='disabled'
            self.PlanetBuildConstructButton['text_fg']=(0.5,0.5,0.5,1)
        
    def checkSalvageAndInfo(self):
        planet=self.selectedObjectName
        section=self.ActiveBuildSection

        if self.ActiveBuildSlot[0] != None and self.world.planetDB[planet]['slots'][section][self.ActiveBuildSlot[0]] != None:
            self.PlanetBuildSalvageButton['state']='normal'
            self.PlanetBuildSalvageButton['text_fg']=(1,1,1,1)
            self.PlanetBuildSlotInfo.show()
            self.fillSlotInfo(planet, section, self.ActiveBuildSlot[0])
        else:
            self.PlanetBuildSalvageButton['state']='disabled'
            self.PlanetBuildSalvageButton['text_fg']=(0.5,0.5,0.5,1)
            self.PlanetBuildSlotInfo.hide()

    def fillSlotInfo(self, planet, section, slot):
        if not None in (planet, section, slot):

            if self.world.planetDB[planet]['slots'][section][slot]['problemText'] == '':
                problemText = 'Running as intended'
            else:
                problemText = self.world.planetDB[planet]['slots'][section][slot]['problemText']
            
            self.PlanetBuildSlotInfoText['text'] = problemText

    def constructBuilding(self):
        planet = self.selectedObjectName
        section = self.ActiveBuildSection
        slot = self.ActiveBuildSlot[0]
        blueprint = self.ActiveBlueprint['text']
        price = self.world.buildingsDB[section][blueprint]['Price']
        enrgCap = self.world.planetDB[planet]['enrgCap']
        enrgUsg = self.world.planetDB[planet]['enrgUsg']

        getsBuild = False
        addPRODTask = False
        addRESCTask = False
        addConsumeTask = False

        if self.world.money >= price:
            if section == 'ENRG':
                getsBuild = True
                self.world.planetDB[planet]['enrgCap']+=self.world.buildingsDB[section][blueprint]['incVal']
                if blueprint == 'Coal Generator' or blueprint == 'Nuclear Reactor':
                    addConsumeTask = True
            else:
                if enrgUsg + self.world.buildingsDB[section][blueprint]['enrgDrain'] <= enrgCap:
                    if section == 'RESC':
                        if self.world.buildingsDB[section][blueprint]['req'] == 'Athmosphere':
                            if self.world.planetDB[planet]['athm']:
                                getsBuild = True
                                addRESCTask = True
                                self.world.planetDB[planet]['enrgUsg']+=self.world.buildingsDB[section][blueprint]['enrgDrain']    
                            else:
                                self.world.createProblemDialog('No Athmosphere present')
                        elif self.world.buildingsDB[section][blueprint]['req'] in self.world.planetDB[planet]['resc']:
                            getsBuild = True
                            addRESCTask = True
                            self.world.planetDB[planet]['enrgUsg']+=self.world.buildingsDB[section][blueprint]['enrgDrain']
                        else:
                            self.world.createProblemDialog('Needed Rescource is not available')
                    elif section == 'PROD':
                        getsBuild = True
                        addPRODTask = True
                        self.world.planetDB[planet]['enrgUsg']+=self.world.buildingsDB[section][blueprint]['enrgDrain']
                    elif section == 'HAB':
                        getsBuild = True
                        self.world.planetDB[planet]['habCap']+=self.world.buildingsDB[section][blueprint]['incVal']
                        self.world.planetDB[planet]['enrgUsg']+=self.world.buildingsDB[section][blueprint]['enrgDrain']
                    elif section == 'DEV':
                        getsBuild = True
                        self.world.planetDB[planet]['enrgUsg']+=self.world.buildingsDB[section][blueprint]['enrgDrain']
                else:
                    self.world.createProblemDialog('Not sufficient Energy')
        else:
            self.world.createProblemDialog('Not enough Money')
        
        if getsBuild:
            self.world.planetDB[planet]['slots'][section][slot] = {'name':blueprint, 'gotProblem':False, 'problemText':'', 'workers':0, 'output':0}
            self.world.money -= price
            self.updateSlots()

        if addRESCTask:
            good = self.world.buildingsDB[section][blueprint]['yield']
            incVal = self.world.buildingsDB[section][blueprint]['incVal']
            taskMgr.doMethodLater(3, self.extractRescourceTask, blueprint + slot, extraArgs=[planet,section, slot, good,incVal], appendTask=True)

        if addPRODTask:
            inGood = self.world.buildingsDB[section][blueprint]['req']
            outGood = self.world.buildingsDB[section][blueprint]['yield']
            incVal = self.world.buildingsDB[section][blueprint]['incVal']
            decVal = self.world.buildingsDB[section][blueprint]['decVal']
            taskMgr.doMethodLater(3, self.processGoodTask, blueprint + slot, extraArgs=[planet, section, slot, inGood, outGood, incVal, decVal], appendTask=True)
            
        if addConsumeTask:
            good = self.world.buildingsDB[section][blueprint]['req']
            decVal = self.world.buildingsDB[section][blueprint]['decVal']
            incVal = self.world.buildingsDB[section][blueprint]['incVal']
            taskMgr.doMethodLater(3, self.consumeGoodTask, blueprint + slot, extraArgs=[planet, section, slot, good, decVal, incVal], appendTask=True)

        self.checkConstructButton()
        self.checkSalvageAndInfo()

    def salvageBuilding(self):
            planet = self.selectedObjectName
            slot = self.ActiveBuildSlot[0]
            section = self.ActiveBuildSection
            blueprint = self.world.planetDB[planet]['slots'][section][slot]['name']
            price = self.world.buildingsDB[section][blueprint]['Price']
            incVal = self.world.buildingsDB[section][blueprint]['incVal']
            enrgDrain = self.world.buildingsDB[section][blueprint]['enrgDrain']
            
            getsSalvaged = True

            if section == 'ENRG': 
                if (self.world.planetDB[planet]['enrgCap'] - incVal) < self.world.planetDB[planet]['enrgUsg']:
                    self.world.createProblemDialog('Energy too low if salvaged')
                    getsSalvaged = False
                else:
                    self.world.planetDB[planet]['enrgCap'] -= incVal
            


            if getsSalvaged:
                self.world.planetDB[planet]['slots'][section][slot] = None
                self.world.planetDB[planet]['enrgUsg'] -= enrgDrain
                self.world.money += round(price * self.world.salvageFactor)
                self.updateSlots()
                
                taskMgr.remove(blueprint + slot)
                self.checkSalvageAndInfo()
                self.checkConstructButton()

    def updateSlots(self):
        planet = self.selectedObjectName
        section = self.ActiveBuildSection
        data = self.world.planetDB[planet]['slots'][section]
        fl = section[0]

        ctr=0
        for button in self.PlanetBuildSlotButtons:
            buttonLabel = self.PlanetBuildSlotLabels[ctr]
            
            if data[str(ctr+1)] != None:
                buttonLabel['text'] = data[str(ctr+1)]['name']
                if data[str(ctr+1)]['gotProblem']: buttonLabel['text']+= '\n/!\PROBLEM/!\\'
            else: buttonLabel['text'] = ''
            button['text'] = fl + str(ctr+1)
            ctr+=1



    def refreshTask(self, planet, task):
        data = self.world.planetDB[planet]
        athm = data['athm']
        wind = data['wind']
        enrgUsg = data['enrgUsg']
        enrgCap = data['enrgCap']
        pop = data['pop']
        habCap = data['habCap']

        
        self.PlanetBuildQuickText1['text'] = (
            'ATHM: {} - WIND: {} - ENRG: {}/{} - POP: {}/{}'.format(athm, wind, enrgUsg, enrgCap, pop, habCap)
        )

        self.PlanetBuildQuickText2['text'] = 'RESC: '
        for k,v in data['resc'].items():
            self.PlanetBuildQuickText2['text'] += k + ', '

        self.PlanetBuildQuickText3['text'] = 'GOODS: '
        if 'goods' in data:
            for k,v in data['goods'].items():
                self.PlanetBuildQuickText3['text'] += str(v) + ' ' + k + ' - '
        return task.cont

    def extractRescourceTask(self, celObj, section, slot, good, incVal, task):
        
        if not (good in self.world.planetDB[celObj]['goods']):
            self.world.planetDB[celObj]['goods'].update({good:0})
        
        if self.world.planetDB[celObj]['enrgCap'] < self.world.planetDB[celObj]['enrgUsg']:
            if self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] == False:
                self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] = True
                self.world.planetDB[celObj]['slots'][section][slot]['problemText'] = 'Not enough energy to continue extraction'
                self.updateBuildSlotButtons()
                self.fillSlotInfo(celObj, section, slot)
        elif self.world.planetDB[celObj]['goods'][good] >= self.world.goodsCap:
            if self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] == False:
                self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] = True
                self.world.planetDB[celObj]['slots'][section][slot]['problemText'] = 'Storage is full'
                self.updateBuildSlotButtons()
                self.fillSlotInfo(celObj, section, slot)
        else:
            if self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] == True:
                self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] = False
                self.world.planetDB[celObj]['slots'][section][slot]['problemText'] = ''
                self.updateBuildSlotButtons()
                self.fillSlotInfo(celObj, section, slot)
            self.world.planetDB[celObj]['goods'][good]+=incVal
        
        return task.again

    def processGoodTask(self, celObj, section, slot, inGood, outGood, incVal, decVal, task):

        if not (inGood in self.world.planetDB[celObj]['goods']) or self.world.planetDB[celObj]['goods'][inGood] < decVal:
            if self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] == False:
                self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] = True
                self.world.planetDB[celObj]['slots'][section][slot]['problemText'] = 'Missing {} to continue production'.format(inGood)
                self.updateBuildSlotButtons()
                self.fillSlotInfo(celObj, section, slot)
        elif self.world.planetDB[celObj]['enrgCap'] < self.world.planetDB[celObj]['enrgUsg']:
            if self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] == False:
                self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] = True
                self.world.planetDB[celObj]['slots'][section][slot]['problemText'] = 'Not enough energy to continue production'
                self.updateBuildSlotButtons()
                self.fillSlotInfo(celObj, section, slot)
        elif self.world.planetDB[celObj]['goods'][outGood] >= self.world.goodsCap:
            if self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] == False:
                self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] = True
                self.world.planetDB[celObj]['slots'][section][slot]['problemText'] = 'Storage is full'
                self.updateBuildSlotButtons()
                self.fillSlotInfo(celObj, section, slot)
        else:
            if self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] == True:
                self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] = False
                self.world.planetDB[celObj]['slots'][section][slot]['problemText'] = ''
                self.updateBuildSlotButtons()
                self.fillSlotInfo(celObj, section, slot)
                
            self.world.planetDB[celObj]['goods'][inGood]-=decVal
            if not (outGood in self.world.planetDB[celObj]['goods']):
                self.world.planetDB[celObj]['goods'].update({outGood:0})
            self.world.planetDB[celObj]['goods'][outGood]+=incVal
        
        return task.again

    def consumeGoodTask(self, celObj, section, slot, good, decVal, incVal, task):

        if not (good in self.world.planetDB[celObj]['goods']) or self.world.planetDB[celObj]['goods'][good] < decVal:
            if self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] == False:
                self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] = True
                self.world.planetDB[celObj]['slots'][section][slot]['problemText'] = 'Missing {} to continue service'.format(good)
                self.updateSlots()
                self.fillSlotInfo(celObj, section, slot)
                if section == 'ENRG': self.world.planetDB[celObj]['enrgCap'] -= incVal
        else:
            if self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] == True:
                self.world.planetDB[celObj]['slots'][section][slot]['gotProblem'] = False
                self.world.planetDB[celObj]['slots'][section][slot]['problemText'] = ''
                self.updateSlots()
                self.fillSlotInfo(celObj, section, slot)
                if section == 'ENRG': self.world.planetDB[celObj]['enrgCap'] += incVal
            self.world.planetDB[celObj]['goods'][good]-=decVal

        return task.again


    def createGui(self):

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
            pos=(-0.18,0,-0.9), scale=0.5, pad=(-0.1, -0.09), frameColor=(0,0,0,0),
            text_scale=0.15, text_pos=(0, -0.03), text_fg=(1,1,1,1), geom_scale=(0.7,0,1), geom=(self.world.buttonMaps),
            command=self.world.NewPlanetInfoView.togglePlanetBuildMode, extraArgs=[False], parent=self.PlanetBuildPanel)


        self.PlanetBuildRESCButton = DirectButton(text='Rescources', 
            pos=(0.4,0,0.75), pad=(0.03, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.06, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.switchBuildSection, parent=self.PlanetBuildPanel, relief='sunken')
        self.PlanetBuildRESCButton['extraArgs']=['RESC', self.PlanetBuildRESCButton]

        self.PlanetBuildPRODButton = DirectButton(text='Production', 
            pos=(0.79,0,0.75), pad=(0.03, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.06, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.switchBuildSection, parent=self.PlanetBuildPanel)
        self.PlanetBuildPRODButton['extraArgs']=['PROD', self.PlanetBuildPRODButton]

        self.PlanetBuildENRGButton = DirectButton(text='Energy', 
            pos=(1.19,0,0.755), pad=(0.1, 0.017), borderWidth=(0.01,0.01),
            text_scale=0.06, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.switchBuildSection, parent=self.PlanetBuildPanel)
        self.PlanetBuildENRGButton['extraArgs']=['ENRG', self.PlanetBuildENRGButton]

        self.PlanetBuildDEVButton = DirectButton(text='Developement', 
            pos=(1.64,0,0.755), pad=(0.03, 0.017), borderWidth=(0.01,0.01),
            text_scale=0.06, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.switchBuildSection, parent=self.PlanetBuildPanel)
        self.PlanetBuildDEVButton['extraArgs']=['DEV', self.PlanetBuildDEVButton]

        self.PlanetBuildHABButton = DirectButton(text='Habitation', 
            pos=(2.06,0,0.75), pad=(0.03, 0.02), borderWidth=(0.01,0.01),
            text_scale=0.06, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
            command=self.switchBuildSection, parent=self.PlanetBuildPanel)
        self.PlanetBuildHABButton['extraArgs']=['HAB', self.PlanetBuildHABButton]


        self.PlanetBuildQuickInfo = DirectFrame(frameSize=(0, 1.63, -0.08, 0.07), pos=(-0.4,0,-0.73),
            frameColor=(0.15, 0.15, 0.15, 0.9), parent=self.PlanetBuildPanel)

        self.PlanetBuildQuickText1 = DirectLabel(text='ATHM: Yes  -  WIND: 1  -  HAB: 20/100  -  ENRG: 60/100', 
            pos=(0.03, 0, 0.015), text_fg=(0.9,0.9,0.9,1), frameColor=(0,0,0,0), text_scale = 0.05,
            frameSize=(0,0.8,0,0.5), parent=self.PlanetBuildQuickInfo, text_align=TextNode.ALeft)
        
        self.PlanetBuildQuickText2 = DirectLabel(text='RESC: Coal, Iron, Uranium', 
            pos=(0.03, 0, -0.038), text_fg=(0.9,0.9,0.9,1), frameColor=(0,0,0,0), text_scale = 0.05,
            frameSize=(0,0.8,0,0.5), parent=self.PlanetBuildQuickInfo, text_align=TextNode.ALeft)

        self.PlanetBuildQuickText3 = DirectLabel(text='GOODS: Coal sacks, Uranium rods', 
            pos=(0.7, 0, -0.038), text_fg=(0.9,0.9,0.9,1), frameColor=(0,0,0,0), text_scale = 0.05,
            frameSize=(0,0.8,0,0.5), parent=self.PlanetBuildQuickInfo, text_align=TextNode.ALeft)

        # All static gui elements for the planet build slots
        #---------------------------------------------------
        slotModel = loader.loadModel('models/gui/slots/simple_slot_maps.egg')
        slotMaps = (slotModel.find('**/normal'),slotModel.find('**/active'),
                    slotModel.find('**/normal'),slotModel.find('**/disabled'))
        
        self.PlanetBuildSlotContainer = DirectFrame(pos=(1.45,0,0), frameColor=(0.5,0.5,0.5,1))
        self.PlanetBuildSlotContainer.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildSlotButtons = [

            DirectRadioButton(text='R1', 
                pos=(0.27,0,0.53), frameColor=(0,0,0,0), frameSize=(-0.035,0.035,-0.035,0.035), indicatorValue=0, boxPlacement='center',
                text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1,1,1,1), boxGeomScale=(0.18,0,0.18), boxGeom=(slotMaps), boxBorder=-0.245,
                command=self.switchBuildSlot, variable=self.ActiveBuildSlot, value=['1'], parent=self.PlanetBuildSlotContainer, scale=0.9),

            DirectRadioButton(text='R2', 
                pos=(0.12,0,0.29), frameColor=(0,0,0,0), frameSize=(-0.035,0.035,-0.035,0.035), indicatorValue=0, boxPlacement='center',
                text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1,1,1,1), boxGeomScale=(0.18,0,0.18), boxGeom=(slotMaps), boxBorder=-0.245,
                command=self.switchBuildSlot, variable=self.ActiveBuildSlot, value=['2'], parent=self.PlanetBuildSlotContainer, scale=0.9),

            DirectRadioButton(text='R3', 
                pos=(0.05,0,0), frameColor=(0,0,0,0), frameSize=(-0.035,0.035,-0.035,0.035), indicatorValue=0, boxPlacement='center',
                text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1,1,1,1), boxGeomScale=(0.18,0,0.18), boxGeom=(slotMaps), boxBorder=-0.245,
                command=self.switchBuildSlot, variable=self.ActiveBuildSlot, value=['3'], parent=self.PlanetBuildSlotContainer, scale=0.9),

            DirectRadioButton(text='R4', 
                pos=(0.12,0,-0.29), frameColor=(0,0,0,0), frameSize=(-0.035,0.035,-0.035,0.035), indicatorValue=0, boxPlacement='center',
                text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1,1,1,1), boxGeomScale=(0.18,0,0.18), boxGeom=(slotMaps), boxBorder=-0.245,
                command=self.switchBuildSlot, variable=self.ActiveBuildSlot, value=['4'], parent=self.PlanetBuildSlotContainer, scale=0.9),

            DirectRadioButton(text='R5', 
                pos=(0.27,0,-0.53), frameColor=(0,0,0,0), frameSize=(-0.035,0.035,-0.035,0.035), indicatorValue=0, boxPlacement='center',
                text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1,1,1,1), boxGeomScale=(0.18,0,0.18), boxGeom=(slotMaps), boxBorder=-0.245,
                command=self.switchBuildSlot, variable=self.ActiveBuildSlot, value=['5'], parent=self.PlanetBuildSlotContainer, scale=0.9)
        ]

        for button in self.PlanetBuildSlotButtons:
            button.setOthers(self.PlanetBuildSlotButtons)

        self.PlanetBuildSlotLabels = [

            DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1), text_bg=(0.2,0.2,0.2,0.9),
                frameColor=(0,0,0,0), pos=(0,0,0.07), parent=self.PlanetBuildSlotButtons[0]),

            DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
                frameColor=(0,0,0,0), pos=(0,0,0.07), parent=self.PlanetBuildSlotButtons[1]),

            DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
                frameColor=(0,0,0,0), pos=(0,0,0.07), parent=self.PlanetBuildSlotButtons[2]),

            DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
                frameColor=(0,0,0,0), pos=(0,0,0.07), parent=self.PlanetBuildSlotButtons[3]),

            DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
                frameColor=(0,0,0,0), pos=(0,0,0.07), parent=self.PlanetBuildSlotButtons[4])
        ]


        self.PlanetBuildSlotInfo = DirectFrame(pos=(0.4,0,0.35), frameSize=(0,0.9,-0.7,0), frameColor=(0.2,0.2,0.25,0.8),
            parent=self.PlanetBuildSlotContainer, text_scale=0.03, text_fg=(1,1,1,1))
        self.PlanetBuildSlotInfo.hide()
        self.PlanetBuildSlotInfoText = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0,0,0,0),
            frameColor=(0,0,0,0), pos=(0.04,0,-0.09), text_align=TextNode.ALeft, text_wordwrap=15,
            parent=self.PlanetBuildSlotInfo)