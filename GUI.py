""" Module to setup all neede GUI elements right after starting up the game.
use setUpGUI(self) and make them visible with element.show() as it gets needed."""

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import *

def setUpGui(world):


    # Constant visible gui elements
    #------------------------------
    world.HeadGUIPanel = DirectFrame(frameColor=(0.2, 0.2, 0.22, 0.9), frameSize=(0, 1.55, -0.13, 0), pos=(-1.8, 0, 1))
    
    world.HeadGUIText = DirectLabel(text=('Year '+str(world.yearCounter)+', '
                                            'Day '+str(world.dayCounter) + ', '
                                            'Money: ' +str(world.money) + ', '
                                            'Population: ' +str(world.systemPopulation)), 
        pos=(0.1, 0, -0.085), text_fg=(1, 1, 1, 1), frameColor=(0,0,0,0),
        parent=world.HeadGUIPanel, text_align=TextNode.ALeft, text_scale=.07)

    world.MapViewPanel = DirectFrame(
        frameColor=(0.2, 0.2, 0.22, 0.9),
        frameSize=(0, 0.5, -1.2, 0),
        pos=(-1.75, 0, 0.6))




    # All static gui elements for the planet info screen
    #---------------------------------------------------
    world.PlanetInfoPanel = DirectFrame(
        frameColor=(0.2, 0.2, 0.22, 0.9),
        frameSize=(-0.9, 1.1, -0.65, 0.65),
        pos=(-0.8, 0, 0))
    world.PlanetInfoPanel.hide()

    world.PlanetInfoTitle = DirectLabel(text='', pos=(-0.85, 0, 0.5), 
        text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = world.PlanetInfoPanel, 
        text_align=TextNode.ALeft, text_scale = 0.13)

    world.PlanetInfoAttributesTable = DirectLabel(text='', pos=(-0.85, 0, 0.4), 
        text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = world.PlanetInfoPanel, 
        text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)

    world.PlanetInfoRescourceTable = DirectLabel(text='', pos=(-0.85, 0, 0), 
        text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = world.PlanetInfoPanel, 
        text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)
    
    world.PlanetInfoGoodsTable = DirectLabel(text='', pos=(-0.85, 0, -0.35), 
        text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = world.PlanetInfoPanel, 
        text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)

    world.PlanetInfoENRGTable = DirectLabel(text='', pos=(0.28, 0, 0.4), 
        text_fg=(1,1,1,1), frameColor=(0,0,0,0), parent = world.PlanetInfoPanel, 
        text_align=TextNode.ALeft, scale=0.13, text_scale=0.5)

    world.PlanetInfoCloseButton = DirectButton(text='Close', 
        pos=(-0.745,0,-0.92), pad=(0.05, 0.02), borderWidth=(0.01,0.01),
        text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.togglePlanetInfoMode, extraArgs=[False], parent=world.PlanetInfoPanel)

    world.PlanetInfoProbeButton = DirectButton(text='Probe', 
        pos=(1.45,0,0.55), pad=(0.055, 0.02), borderWidth=(0.01,0.01),
        text_scale=0.07, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.showProbeMission, parent=world.PlanetInfoPanel)

    world.PlanetInfoColoniseButton = DirectButton(text='Colonise', 
        pos=(1.85,0,0.55), pad=(0.03, 0.02), borderWidth=(0.01,0.01),
        text_scale=0.07, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.showProbeMission, parent=world.PlanetInfoPanel)

    world.PlanetInfoBuildButton = DirectButton(text='Build', 
        pos=(1.65,0,-0.58), pad=(0.06, 0.05), borderWidth=(0.01,0.01),
        text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.togglePlanetBuildMode, extraArgs=[True], parent=world.PlanetInfoPanel)

    world.PlanetInfoProblemPanel = DirectFrame(frameColor=(0.2, 0.2, 0.22, 0.9),
        frameSize=(0, 0.4, -1.3, 0),pos=(2.25, 0, 0.65), parent=world.PlanetInfoPanel)

    # All static gui elements for the planet build panel
    #---------------------------------------------------
    world.PlanetBuildPanel = DirectFrame(
        frameColor=(0.15, 0.15, 0.15, 0.9),
        frameSize=(-0.4, 1.23, 0.66, -0.65),
        pos=(-1.3, 0, 0))
    world.PlanetBuildPanel.hide()

    world.PlanetBuildPanelContent = []

    world.PlanetBuildPanelRuler = DirectFrame(frameColor=(0,0,0,0.9), frameSize=(-0.003, 0.003, -1.305, 0),
        pos=(0.408,0,0.657), parent=world.PlanetBuildPanel)

    world.PlanetBuildDescriptionField = DirectFrame(
        frameColor=(0.2, 0.2, 0.22, 0.9),
        frameSize=(-0.4, 0.4, 0.25, -0.25),
        pos=(0.825, 0, 0.41), parent=world.PlanetBuildPanel)

    world.PlanetBuildDescriptionText = DirectLabel(text='', 
        pos=(-0.36, 0, 0.18), text_fg=(1,1,1,1), frameColor=(0,0,0,0), text_scale = 0.05, text_wordwrap=15,
        frameSize=(0,0.8,0,0.5), parent = world.PlanetBuildDescriptionField, text_align=TextNode.ALeft)

    world.PlanetBuildConstructButton = DirectButton(text='Construct ->', 
        pos=(-0.122,0,-0.37), pad=(0.05, 0.02), borderWidth=(0.01,0.01),
        text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.constructBuilding, parent=world.PlanetBuildDescriptionField, state='disabled')

    world.PlanetBuildSalvageButton  = DirectButton(text='<- Salvage', 
        pos=(-0.126,0,-0.52), pad=(0.085, 0.013), borderWidth=(0.01,0.01),
        text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.salvageBuilding, parent=world.PlanetBuildDescriptionField, state='disabled')

    world.PlanetBuildCloseButton = DirectButton(text='Back', 
        pos=(-0.26,0,-0.92), pad=(0.05, 0.02), borderWidth=(0.01,0.01),
        text_scale=0.08, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.togglePlanetBuildMode, extraArgs=[False], parent=world.PlanetBuildPanel)


    world.PlanetBuildRESCButton = DirectButton(text='Rescources', 
        pos=(0.4,0,0.75), pad=(0.03, 0.02), borderWidth=(0.01,0.01),
        text_scale=0.06, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.switchBuildSection, parent=world.PlanetBuildPanel, relief='sunken')
    world.PlanetBuildRESCButton['extraArgs']=['RESC', world.PlanetBuildRESCButton]

    world.PlanetBuildPRODButton = DirectButton(text='Production', 
        pos=(0.79,0,0.75), pad=(0.03, 0.02), borderWidth=(0.01,0.01),
        text_scale=0.06, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.switchBuildSection, parent=world.PlanetBuildPanel)
    world.PlanetBuildPRODButton['extraArgs']=['PROD', world.PlanetBuildPRODButton]

    world.PlanetBuildENRGButton = DirectButton(text='Energy', 
        pos=(1.19,0,0.755), pad=(0.1, 0.017), borderWidth=(0.01,0.01),
        text_scale=0.06, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.switchBuildSection, parent=world.PlanetBuildPanel)
    world.PlanetBuildENRGButton['extraArgs']=['ENRG', world.PlanetBuildENRGButton]

    world.PlanetBuildDEVButton = DirectButton(text='Developement', 
        pos=(1.64,0,0.755), pad=(0.03, 0.017), borderWidth=(0.01,0.01),
        text_scale=0.06, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.switchBuildSection, parent=world.PlanetBuildPanel)
    world.PlanetBuildDEVButton['extraArgs']=['DEV', world.PlanetBuildDEVButton]

    world.PlanetBuildHABButton = DirectButton(text='Habitation', 
        pos=(2.06,0,0.75), pad=(0.03, 0.02), borderWidth=(0.01,0.01),
        text_scale=0.06, frameColor=(0.15,0.15,0.15,0.9), text_fg=(1,1,1,1),
        command=world.switchBuildSection, parent=world.PlanetBuildPanel)
    world.PlanetBuildHABButton['extraArgs']=['HAB', world.PlanetBuildHABButton]


    world.PlanetBuildQuickInfo = DirectFrame(frameSize=(0, 1.63, -0.08, 0.07), pos=(-0.4,0,-0.73),
        frameColor=(0.15, 0.15, 0.15, 0.9), parent=world.PlanetBuildPanel)

    world.PlanetBuildQuickText1 = DirectLabel(text='ATHM: Yes  -  WIND: 1  -  HAB: 20/100  -  ENRG: 60/100', 
        pos=(0.03, 0, 0.015), text_fg=(0.9,0.9,0.9,1), frameColor=(0,0,0,0), text_scale = 0.05,
        frameSize=(0,0.8,0,0.5), parent=world.PlanetBuildQuickInfo, text_align=TextNode.ALeft)
    
    world.PlanetBuildQuickText2 = DirectLabel(text='RESC: Coal, Iron, Uranium', 
        pos=(0.03, 0, -0.038), text_fg=(0.9,0.9,0.9,1), frameColor=(0,0,0,0), text_scale = 0.05,
        frameSize=(0,0.8,0,0.5), parent=world.PlanetBuildQuickInfo, text_align=TextNode.ALeft)

    world.PlanetBuildQuickText3 = DirectLabel(text='GOODS: Coal sacks, Uranium rods', 
        pos=(0.7, 0, -0.038), text_fg=(0.9,0.9,0.9,1), frameColor=(0,0,0,0), text_scale = 0.05,
        frameSize=(0,0.8,0,0.5), parent=world.PlanetBuildQuickInfo, text_align=TextNode.ALeft)

    # All static gui elements for the planet build slots
    #---------------------------------------------------
    world.PlanetBuildSlotContainer = DirectFrame(pos=(1.45,0,0), frameColor=(0.5,0.5,0.5,1))
    world.PlanetBuildSlotContainer.reparentTo(world.PlanetBuildPanel)

    world.PlanetBuildSlot1 = DirectButton(text='R1', 
        pos=(0.27,0,0.5), hpr=(0,0,45), pad=(0.05, 0.05), borderWidth=(0.02,0.02),
        text_scale=0.06, frameColor=(0.2,0.2,0.2,1), text_fg=(1,1,1,1), text_roll=45,
        command=world.switchBuildSlot, parent=world.PlanetBuildSlotContainer)
    world.PlanetBuildSlot1['extraArgs'] = [world.PlanetBuildSlot1]
    world.PlanetBuildSlot1Lable = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1), text_bg=(0.2,0.2,0.2,0.9),
        frameColor=(0,0,0,0), hpr=(0,0,-45), pos=(-0.07,0,0.07), parent=world.PlanetBuildSlot1)

    world.PlanetBuildSlot2 = DirectButton(text='R2', 
        pos=(0.12,0,0.29), hpr=(0,0,45), pad=(0.05, 0.05), borderWidth=(0.02,0.02),
        text_scale=0.06, frameColor=(0.2,0.2,0.2,1), text_fg=(1,1,1,1), text_roll=45,
        command=world.switchBuildSlot, parent=world.PlanetBuildSlotContainer)
    world.PlanetBuildSlot2['extraArgs'] = [world.PlanetBuildSlot2]
    world.PlanetBuildSlot2Lable = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
        frameColor=(0,0,0,0), hpr=(0,0,-45), pos=(-0.07,0,0.07), parent=world.PlanetBuildSlot2)

    world.PlanetBuildSlot3 = DirectButton(text='R3', 
        pos=(0.05,0,0), hpr=(0,0,45), pad=(0.05, 0.05), borderWidth=(0.02,0.02),
        text_scale=0.06, frameColor=(0.2,0.2,0.2,1), text_fg=(1,1,1,1), text_roll=45,
        command=world.switchBuildSlot, parent=world.PlanetBuildSlotContainer)
    world.PlanetBuildSlot3['extraArgs'] = [world.PlanetBuildSlot3]
    world.PlanetBuildSlot3Lable = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
        frameColor=(0,0,0,0), hpr=(0,0,-45), pos=(-0.07,0,0.07), parent=world.PlanetBuildSlot3)

    world.PlanetBuildSlot4 = DirectButton(text='R4', 
        pos=(0.12,0,-0.29), hpr=(0,0,45), pad=(0.05, 0.05), borderWidth=(0.02,0.02),
        text_scale=0.06, frameColor=(0.2,0.2,0.2,1), text_fg=(0.5,0.5,0.5,1), text_roll=45,
        command=world.switchBuildSlot, parent=world.PlanetBuildSlotContainer, state='disabled')
    world.PlanetBuildSlot4['extraArgs'] = [world.PlanetBuildSlot4]
    world.PlanetBuildSlot4Lable = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
        frameColor=(0,0,0,0), hpr=(0,0,-45), pos=(-0.07,0,0.07), parent=world.PlanetBuildSlot4)

    world.PlanetBuildSlot5 = DirectButton(text='R5', 
        pos=(0.27,0,-0.51), hpr=(0,0,45), pad=(0.05, 0.05), borderWidth=(0.02,0.02),
        text_scale=0.06, frameColor=(0.2,0.2,0.2,1), text_fg=(0.5,0.5,0.5,1), text_roll=45,
        command=world.switchBuildSlot, parent=world.PlanetBuildSlotContainer, state='disabled')
    world.PlanetBuildSlot5['extraArgs'] = [world.PlanetBuildSlot5]
    world.PlanetBuildSlot5Lable = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
        frameColor=(0,0,0,0), hpr=(0,0,-45), pos=(-0.07,0,0.07), parent=world.PlanetBuildSlot5)


        #world.PlanetBuildWire1 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(0,1,0,1),
        #    pos=(1.7,-0.5,-0.035))
        #world.PlanetBuildWire1.reparentTo(world.PlanetBuildSlotContainer)

        #world.PlanetBuildWire2 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(1,0,0,1),
        #    pos=(1.4,-0.5, 0.165))
        #world.PlanetBuildWire2.reparentTo(world.PlanetBuildSlotContainer)

        #world.PlanetBuildWire3 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(1,0,0,1),
        #    pos=(1.4,-0.5,-0.235))
        #world.PlanetBuildWire3.reparentTo(world.PlanetBuildSlotContainer)