""" Module to setup all neede GUI elements right after starting up the game.
use setUpGUI(self) and make them visible with element.show() as it gets needed."""

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import *

def setUpGui(world):

    # Constant visible gui elements
    #------------------------------

    #world.infoDialogPanelMap = loader.loadModel('models/gui/panels/infodialogpanel_maps.egg').find('**/infodialogpanel')

    
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
    #infoPanelMap = loader.loadModel('models/gui/panels/planetinfopanel_maps.egg').find('**/planetinfopanel')
    #problemPanelMap = loader.loadModel('models/gui/panels/planetproblempanel_maps.egg').find('**/planetproblempanel')
    
    
    

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
        pos=(-0.18,0,-0.9), scale=0.5, pad=(-0.1, -0.09), frameColor=(0,0,0,0),
        text_scale=0.15, text_pos=(0, -0.03), text_fg=(1,1,1,1), geom_scale=(0.7,0,1), geom=(world.buttonMaps),
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
    slotModel = loader.loadModel('models/gui/slots/simple_slot_maps.egg')
    slotMaps = (slotModel.find('**/normal'),slotModel.find('**/active'),
                  slotModel.find('**/normal'),slotModel.find('**/disabled'))
    
    world.PlanetBuildSlotContainer = DirectFrame(pos=(1.45,0,0), frameColor=(0.5,0.5,0.5,1))
    world.PlanetBuildSlotContainer.reparentTo(world.PlanetBuildPanel)

    world.PlanetBuildSlotButtons = [

        DirectRadioButton(text='R1', 
            pos=(0.27,0,0.53), frameColor=(0,0,0,0), frameSize=(-0.035,0.035,-0.035,0.035), indicatorValue=0, boxPlacement='center',
            text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1,1,1,1), boxGeomScale=(0.18,0,0.18), boxGeom=(slotMaps), boxBorder=-0.245,
            command=world.switchBuildSlot, variable=world.ActiveBuildSlot, value=['1'], parent=world.PlanetBuildSlotContainer, scale=0.9),

        DirectRadioButton(text='R2', 
            pos=(0.12,0,0.29), frameColor=(0,0,0,0), frameSize=(-0.035,0.035,-0.035,0.035), indicatorValue=0, boxPlacement='center',
            text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1,1,1,1), boxGeomScale=(0.18,0,0.18), boxGeom=(slotMaps), boxBorder=-0.245,
            command=world.switchBuildSlot, variable=world.ActiveBuildSlot, value=['2'], parent=world.PlanetBuildSlotContainer, scale=0.9),

        DirectRadioButton(text='R3', 
            pos=(0.05,0,0), frameColor=(0,0,0,0), frameSize=(-0.035,0.035,-0.035,0.035), indicatorValue=0, boxPlacement='center',
            text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1,1,1,1), boxGeomScale=(0.18,0,0.18), boxGeom=(slotMaps), boxBorder=-0.245,
            command=world.switchBuildSlot, variable=world.ActiveBuildSlot, value=['3'], parent=world.PlanetBuildSlotContainer, scale=0.9),

        DirectRadioButton(text='R4', 
            pos=(0.12,0,-0.29), frameColor=(0,0,0,0), frameSize=(-0.035,0.035,-0.035,0.035), indicatorValue=0, boxPlacement='center',
            text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1,1,1,1), boxGeomScale=(0.18,0,0.18), boxGeom=(slotMaps), boxBorder=-0.245,
            command=world.switchBuildSlot, variable=world.ActiveBuildSlot, value=['4'], parent=world.PlanetBuildSlotContainer, scale=0.9),

        DirectRadioButton(text='R5', 
            pos=(0.27,0,-0.53), frameColor=(0,0,0,0), frameSize=(-0.035,0.035,-0.035,0.035), indicatorValue=0, boxPlacement='center',
            text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1,1,1,1), boxGeomScale=(0.18,0,0.18), boxGeom=(slotMaps), boxBorder=-0.245,
            command=world.switchBuildSlot, variable=world.ActiveBuildSlot, value=['5'], parent=world.PlanetBuildSlotContainer, scale=0.9)
    ]

    for button in world.PlanetBuildSlotButtons:
        button.setOthers(world.PlanetBuildSlotButtons)

    world.PlanetBuildSlotLabels = [

        DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1), text_bg=(0.2,0.2,0.2,0.9),
            frameColor=(0,0,0,0), pos=(0,0,0.07), parent=world.PlanetBuildSlotButtons[0]),

        DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
            frameColor=(0,0,0,0), pos=(0,0,0.07), parent=world.PlanetBuildSlotButtons[1]),

        DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
            frameColor=(0,0,0,0), pos=(0,0,0.07), parent=world.PlanetBuildSlotButtons[2]),

        DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
            frameColor=(0,0,0,0), pos=(0,0,0.07), parent=world.PlanetBuildSlotButtons[3]),

        DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0.2,0.2,0.2,0.9),
            frameColor=(0,0,0,0), pos=(0,0,0.07), parent=world.PlanetBuildSlotButtons[4])
    ]


    world.PlanetBuildSlotInfo = DirectFrame(pos=(0.4,0,0.35), frameSize=(0,0.9,-0.7,0), frameColor=(0.2,0.2,0.25,0.8),
        parent=world.PlanetBuildSlotContainer, text_scale=0.03, text_fg=(1,1,1,1))
    world.PlanetBuildSlotInfo.hide()
    world.PlanetBuildSlotInfoText = DirectLabel(text='', text_scale=0.06, text_fg=(1,1,1,1),  text_bg=(0,0,0,0),
        frameColor=(0,0,0,0), pos=(0.04,0,-0.09), text_align=TextNode.ALeft, text_wordwrap=15,
        parent=world.PlanetBuildSlotInfo)

        #world.PlanetBuildWire1 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(0,1,0,1),
        #    pos=(1.7,-0.5,-0.035))
        #world.PlanetBuildWire1.reparentTo(world.PlanetBuildSlotContainer)

        #world.PlanetBuildWire2 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(1,0,0,1),
        #    pos=(1.4,-0.5, 0.165))
        #world.PlanetBuildWire2.reparentTo(world.PlanetBuildSlotContainer)

        #world.PlanetBuildWire3 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(1,0,0,1),
        #    pos=(1.4,-0.5,-0.235))
        #world.PlanetBuildWire3.reparentTo(world.PlanetBuildSlotContainer)