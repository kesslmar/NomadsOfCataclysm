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
from panda3d.core import (WindowProperties, CollisionNode, GeomNode, CollisionRay)
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

import sys
import random
import math
import buildingsDB

from cameraController import CameraController
from planetInfoView import PlanetInfoView
from planetBuildView import PlanetBuildView
from star import Star
from planet import Planet
from moon import Moon

base = ShowBase()
wp = WindowProperties()
wp.setSize(1080, 600)
base.win.requestProperties(wp)


class World(DirectObject):

    def __init__(self):

        # The standard camera position and background initialization
        base.setBackgroundColor(0, 0, 0)
        base.disableMouse()
        self.cam_ctrl = CameraController()
        self.cam_ctrl.reset()

        # The global variables we use to control the speed and size of objects
        self.yearscale = 900
        self.dayscale = self.yearscale / 365.0 * 30
        self.yearCounter = 0
        self.dayCounter = 0
        self.money = 2000
        self.system_population = 0
        self.orbitscale = 10
        self.sizescale = 0.6

        # Global game balance variables
        self.population_time_delta = 3
        self.tax_factor = 0.1
        self.salvage_factor = 0.75
        self.food_consuming_factor = 0.75
        self.goods_cap = 1000

        self.PlanetInfoModeOn = False
        self.capitalPlanet = None

        self.galaxy_objects = []
        self.BuildingsDB = {}  # Will contain all buildable structures

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
        self.create_gui()
        self.NewPlanetInfoView = PlanetInfoView(self)
        self.NewPlanetBuildView = PlanetBuildView(self)

        self.load_planets()
        self.rotate_planets()
        self.BuildingsDB = buildingsDB.loadDB()
        self.set_capital_planet()

        # Add all constantly running checks to the taskmanager
        taskMgr.add(self.redraw_head_gui, "redrawHeadGUITask")
        taskMgr.doMethodLater(
            self.population_time_delta, self.populate_planet_task, 'populatePlanetTask',
            extraArgs=[self.Earth], appendTask=True)
        taskMgr.doMethodLater(2, self.generate_money_task, 'generateMoneyTask')

        # Open up all listeners for varous mouse and keyboard inputs
        self.accept("escape", sys.exit)
        self.accept('mouse1', self.handle_mouse_click)

    # ****************************************
    #         Main Gameplay Functions        *
    # ****************************************

    # Camera, controle and main GUI functions
    # ----------------------------------------

    def handle_mouse_click(self):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
            base.cTrav.traverse(render)
            if self.collQueue.getNumEntries() > 0:
                self.collQueue.sortEntries()
                pickedObj = self.collQueue.getEntry(0).getIntoNodePath()
                pickedObj = pickedObj.findNetTag('clickable')
                if not pickedObj.isEmpty() and not self.PlanetInfoModeOn:
                    instance = pickedObj.getPythonTag('instance')
                    self.toggle_planet_info_mode(True, instance)

    def redraw_head_gui(self, task):
        self.HeadGUIText['text'] = ('Year ' + str(self.yearCounter) + ', '
                                    'Day ' + str(self.dayCounter) + ', '
                                    'Money: ' + str(self.money) + ', '
                                    'Population: ' + str(self.system_population))
        return task.cont

    # Smaller single line functions
    # -----------------------------

    def incYear(self):
        self.yearCounter += 1

    def incDay(self):
        self.dayCounter += 1

    # Functions to interact with the planet info view
    # ------------------------------------------------

    def toggle_planet_info_mode(self, mode=False, obj=None):

        if mode:
            self.MapViewPanel.hide()
            self.PlanetInfoModeOn = True

            self.NewPlanetInfoView.reset(obj)
            zoomInterval = Sequence(
                Func(self.cam_ctrl.info_view_to, obj),
                Wait(0.2),
                Func(self.NewPlanetInfoView.show)
            )
            zoomInterval.start()
        else:
            self.PlanetInfoModeOn = False
            self.cam_ctrl.reset()
            taskMgr.remove('updatePlanetInfoTask')
            self.NewPlanetInfoView.hide()

    # Global general purpose functions and tasks
    # ---------------------------------------------------

    def populate_planet_task(self, planet, task):
        habProblem = planet.habitation_cap <= planet.population
        foodProblem = (not('Vegetable crates' in planet.goods)
                       or planet.goods['Vegetable crates'] < planet.population)
        nutrition_decrease = round(planet.population * self.food_consuming_factor)

        if foodProblem:
            d = random.randint(-1, 2)
            if planet.population - d <= 0:
                planet.population = 0
            else:
                planet.population -= d
        elif habProblem:
            pass
            planet.goods['Vegetable crates'] -= nutrition_decrease
        else:
            planet.population += random.randint(1, 3)
            planet.goods['Vegetable crates'] -= nutrition_decrease
        return task.again

    def count_system_population(self):
        wholePop = 0
        for obj in self.galaxy_objects:
            if type(obj) != Star:
                wholePop += obj.population
        self.system_population = wholePop

    def generate_money_task(self, task):
        self.count_system_population()
        self.money += round(self.system_population * self.tax_factor)
        return task.again

    def add_message(self, planet, id, mType, text, value):
        planet.messages.update({id: {'type': mType, 'text': text, 'value': value}})

    def remove_message(self, planet, id):
        if id in planet.messages:
            planet.messages.pop(id)

    def calc_distance_between_planets(self, planet1, planet2):
        pos1 = planet1.getPos()
        pos2 = planet2.getPos()
        diffX = abs(pos1[0] - pos2[0])
        diffY = abs(pos1[1] - pos2[1])
        dist = math.sqrt(diffX**2 + diffY**2)
        return dist

    def create_dialog(self, problemText, form='ok', function=lambda: None, args=[]):
        if form == 'ok':
            self.ProblemDialog = OkDialog(
                dialogName="OkDialog", text=problemText, text_pos=(0, 0.07),
                command=self.cleanup_dialog, midPad=(-0.15), frameColor=(0, 0, 0, 0),
                text_fg=(1, 1, 1, 1), text_align=TextNode.ACenter, geom=self.dialog_map,
                extraArgs=[function, args])
        elif form == 'yesNo':
            self.ProblemDialog = YesNoDialog(
                dialogName="OkDialog", text=problemText, text_pos=(0, 0.07),
                command=self.cleanup_dialog, midPad=(-0.15), frameColor=(0, 0, 0, 0),
                text_fg=(1, 1, 1, 1), text_align=TextNode.ACenter, geom=self.dialog_map,
                extraArgs=[function, args])

    def cleanup_dialog(self, value, function, args):
        self.ProblemDialog.cleanup()
        if value:
            function(*args)

    # ****************************************
    #        Initialisation Functions        *
    # ****************************************

    def load_planets(self):
        self.orbit_root_mercury = render.attachNewNode('orbit_root_mercury')
        self.orbit_root_venus = render.attachNewNode('orbit_root_venus')
        self.orbit_root_mars = render.attachNewNode('orbit_root_mars')
        self.orbit_root_earth = render.attachNewNode('orbit_root_earth')

        self.orbit_root_moon = (
            self.orbit_root_earth.attachNewNode('orbit_root_moon'))

        self.sky = loader.loadModel("models/sky_dome.blend")

        self.sky_tex = loader.loadTexture("models/sky_tex2_cut.jpg")
        self.sky_tex.setWrapU(Texture.WM_clamp)
        self.sky.setTexture(self.sky_tex, 1)
        self.sky.reparentTo(render)
        self.sky.setScale(300)
        self.sky.setHpr(270, 0, 0)

        self.Sun = Star(self, 'Sun', 'models/planet_sphere',
                        'models/sun_1k_tex.jpg', 2)

        self.Mercury = Planet(self, 'Mercury', 'models/planet_sphere',
                              'models/mercury_1k_tex.jpg', self.orbit_root_mercury,
                              0.385, 0.38, False, 1, {'Coal': 'Common', 'Iron': 'Common'})

        self.Venus = Planet(self, 'Venus', 'models/planet_sphere',
                            'models/venus_1k_tex.jpg', self.orbit_root_venus,
                            0.923, 0.72, False, 2, {'Coal': 'Common', 'Uranium': 'Normal'})

        self.Mars = Planet(self, 'Mars', 'models/planet_sphere',
                           'models/mars_1k_tex.jpg', self.orbit_root_mars,
                           0.512, 1.52, False, 1, {'Gemstone': 'Rare', 'Iron': 'Rare'})
        self.Mars.probed = True

        self.Earth = Planet(self, 'Earth', 'models/planet_sphere',
                            'models/earth_1k_tex.jpg', self.orbit_root_earth,
                            1, 1, True, 1, {'Iron': 'Normal', 'Coal': 'Common'})

        self.orbit_root_moon.setPos(self.orbitscale, 0, 0)

        self.Earth_Moon = Moon(self, 'Moon', 'models/planet_sphere',
                               'models/moon_1k_tex.jpg', self.orbit_root_moon,
                               0.1, 0.1, False, 0, {'Cheese': 'Rare', 'Coal': 'Common'})

    def rotate_planets(self):
        self.day_period_sun = self.Sun.model.hprInterval(20, (360, 0, 0))

        self.orbit_period_mercury = self.orbit_root_mercury.hprInterval(
            (0.241 * self.yearscale), (360, 0, 0))
        self.day_period_mercury = self.Mercury.model.hprInterval(
            (59 * self.dayscale), (360, 0, 0))

        self.orbit_period_venus = self.orbit_root_venus.hprInterval(
            (0.615 * self.yearscale), (360, 0, 0))
        self.day_period_venus = self.Venus.model.hprInterval(
            (243 * self.dayscale), (360, 0, 0))

        self.orbit_period_earth = Sequence(
            self.orbit_root_earth.hprInterval(self.yearscale, (360, 0, 0)),
            Func(self.incYear))
        self.day_period_earth = Sequence(self.Earth.model.hprInterval(
            self.dayscale, (360, 0, 0)), Func(self.incDay))

        self.orbit_period_moon = self.orbit_root_moon.hprInterval(
            (.0749 * self.yearscale), (360, 0, 0))
        self.day_period_moon = self.Earth_Moon.model.hprInterval(
            (.0749 * self.yearscale), (360, 0, 0))

        self.orbit_period_mars = self.orbit_root_mars.hprInterval(
            (1.881 * self.yearscale), (360, 0, 0))
        self.day_period_mars = self.Mars.model.hprInterval(
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

    def set_capital_planet(self):
        self.capitalPlanet = self.Earth
        self.Earth.probed = True
        self.Earth.colonised = True
        self.Earth.population = 100
        self.Earth.habitation_cap = 100

    def create_gui(self):
        self.buttonModel = loader.loadModel('models/gui/buttons/simple_button_maps.egg')
        self.buttonMaps = (self.buttonModel.find('**/normal'), self.buttonModel.find('**/active'),
                           self.buttonModel.find('**/normal'), self.buttonModel.find('**/disabled'))

        self.dialog_model = loader.loadModel('models/gui/panels/infodialogpanel_maps.egg')
        self.dialog_map = self.dialog_model.find('**/infodialogpanel')

        self.HeadGUIPanel = DirectFrame(
            frameColor=(0.2, 0.2, 0.22, 0.9), frameSize=(0, 1.55, -0.13, 0), pos=(-1.8, 0, 1))

        self.HeadGUIText = DirectLabel(
            text=('Year ' + str(self.yearCounter) + ', '
                  'Day ' + str(self.dayCounter) + ', '
                  'Money: ' + str(self.money) + ', '
                  'Population: ' + str(self.system_population)),
            pos=(0.1, 0, -0.085), text_fg=(1, 1, 1, 1), frameColor=(0, 0, 0, 0),
            parent=self.HeadGUIPanel, text_align=TextNode.ALeft, text_scale=.07)

        self.MapViewPanel = DirectFrame(
            frameColor=(0.2, 0.2, 0.22, 0.9),
            frameSize=(0, 0.5, -1.25, 0),
            pos=(-1.75, 0, 0.6))

        self.trading_button = DirectButton(
            text='Trading', pos=(0.25, 0, -0.12), scale=0.5, pad=(-0.1, -0.09),
            frameColor=(0, 0, 0, 0), parent=self.MapViewPanel,
            geom=(self.buttonMaps), geom_scale=(0.7, 0, 1),
            text_scale=0.15, text_pos=(0, -0.03), text_fg=(0.5, 0.5, 0.5, 1),
            state=DGG.DISABLED)

        self.research_button = DirectButton(
            text='Research', pos=(0.25, 0, -0.32), scale=0.5, pad=(-0.1, -0.09),
            frameColor=(0, 0, 0, 0), parent=self.MapViewPanel,
            geom=(self.buttonMaps), geom_scale=(0.7, 0, 1),
            text_scale=0.15, text_pos=(0, -0.03), text_fg=(0.5, 0.5, 0.5, 1),
            state=DGG.DISABLED)

        self.diplomacy_button = DirectButton(
            text='Diplomacy', pos=(0.25, 0, -0.52), scale=0.5, pad=(-0.1, -0.09),
            frameColor=(0, 0, 0, 0), parent=self.MapViewPanel,
            geom=(self.buttonMaps), geom_scale=(0.7, 0, 1),
            text_scale=0.14, text_pos=(0, -0.03), text_fg=(0.5, 0.5, 0.5, 1),
            state=DGG.DISABLED)

        self.military_button = DirectButton(
            text='Military', pos=(0.25, 0, -0.72), scale=0.5, pad=(-0.1, -0.09),
            frameColor=(0, 0, 0, 0), parent=self.MapViewPanel,
            geom=(self.buttonMaps), geom_scale=(0.7, 0, 1),
            text_scale=0.15, text_pos=(0, -0.03), text_fg=(0.5, 0.5, 0.5, 1),
            state=DGG.DISABLED)

        self.galacy_map_button = DirectButton(
            text='Galaxy Map', pos=(0.25, 0, -0.92), scale=0.5, pad=(-0.1, -0.09),
            frameColor=(0, 0, 0, 0), parent=self.MapViewPanel,
            geom=(self.buttonMaps), geom_scale=(0.7, 0, 1),
            text_scale=0.14, text_pos=(0, -0.03), text_fg=(0.5, 0.5, 0.5, 1),
            state=DGG.DISABLED)

        self.statistics_button = DirectButton(
            text='Statistics', pos=(0.25, 0, -1.12), scale=0.5, pad=(-0.1, -0.09),
            frameColor=(0, 0, 0, 0), parent=self.MapViewPanel,
            geom=(self.buttonMaps), geom_scale=(0.7, 0, 1),
            text_scale=0.14, text_pos=(0, -0.03), text_fg=(0.5, 0.5, 0.5, 1),
            state=DGG.DISABLED)

    # ****************************************
    #        Debug / Testing Functions       *
    # ****************************************

    def reset_game(self):
        self.NewPlanetInfoView.hide()
        self.NewPlanetBuildView.hide()
        self.PlanetInfoModeOn = False

        taskMgr.remove('quickinfoTask')
        taskMgr.remove('buildcamTask')
        taskMgr.remove('infocamTask')

        self.yearCounter = 0
        self.dayCounter = 0
        self.money = 2000
        self.system_population = 0

        for planet in self.galaxy_objects:
            planet.reset()

        self.set_capital_planet()

# end class world


if __name__ == '__main__':
    w = World()
    base.run()
