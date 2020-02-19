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
    

        #world.PlanetBuildWire1 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(0,1,0,1),
        #    pos=(1.7,-0.5,-0.035))
        #world.PlanetBuildWire1.reparentTo(world.PlanetBuildSlotContainer)

        #world.PlanetBuildWire2 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(1,0,0,1),
        #    pos=(1.4,-0.5, 0.165))
        #world.PlanetBuildWire2.reparentTo(world.PlanetBuildSlotContainer)

        #world.PlanetBuildWire3 = DirectFrame(frameSize=(0,0.005,0,0.13), frameColor=(1,0,0,1),
        #    pos=(1.4,-0.5,-0.235))
        #world.PlanetBuildWire3.reparentTo(world.PlanetBuildSlotContainer)