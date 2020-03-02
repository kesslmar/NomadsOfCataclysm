from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import *

from star import Star


class PlanetInfoView():

    def __init__(self, world):
        self.world = world
        self.obj = None
        self.selectedObjectName = None
        self.planetData = None
        self.followObjectScale = None
        self.NewPlanetBuildView = None
        self.messagesDict = {}

        self.create_gui()

    def reset(self, obj):
        self.clear()

        self.obj = obj
        self.selectedObjectName = obj.name
        self.followObjectScale = obj.scale
        self.NewPlanetBuildView = self.world.NewPlanetBuildView

        self.fill()
        taskMgr.doMethodLater(1, self.update_view_task, 'updatePlanetInfoTask')
        self.check_buttons()
        self.load_messages()

    def fill(self):
        # Fills the content of the planet info gui every time a planet gets selected

        self.PlanetInfoTitle['text'] = self.obj.name

        if type(self.obj) == Star or self.obj.probed:
            PlanetInfoAttributesText = (
                'Type:\t\t' + str(type(self.obj).__name__) + '\n'
                'Diameter:\t\t' + str(self.obj.scale * 10**5) + '\n')
            if type(self.obj) != Star:
                PlanetInfoAttributesText += (
                    'Distance to Sun:\t' + str(self.obj.distance * 10**7) + '\n'
                    'Athmosphere:\t' + str(self.obj.athmosphere) + '\n'
                    'Windstrength:\t' + str(self.obj.wind) + '\n')

            self.PlanetInfoAttributesTable['text'] = PlanetInfoAttributesText

            if type(self.obj) != Star:
                PlanetInfoRescourceText = 'Rescources:\n'
                for k, v in self.obj.rescources.items():
                    PlanetInfoRescourceText += k + ':\t\t' + str(v) + '\n'

                self.planet_info_rescource_table['text'] = PlanetInfoRescourceText

                if self.obj.goods:
                    planet_info_goods_text = 'Goods:\n'
                    for k, v in self.obj.goods.items():
                        planet_info_goods_text += k + ':\t' + str(v) + '\n'

                    self.planet_info_goods_table['text'] = planet_info_goods_text

                self.planet_info_ENR_table['text'] = (
                    'Energy capacity:\t' + str(self.obj.energy_cap) + '\n'
                    'Energy usage:\t' + str(self.obj.energy_usg) + '\n\n'

                    'Habitation capacity:\t' + str(self.obj.habitation_cap) + '\n'
                    'Population count:\t' + str(self.obj.population) + '\n\n'

                    'Per Capita GDP:\t' + str(self.world.tax_factor)
                )
        else:
            self.PlanetInfoAttributesTable['text'] = '???'

    def update_view_task(self, task):
        self.fill()
        self.check_buttons()
        self.empty_messages()
        self.load_messages()
        return task.again

    def clear(self):
        self.PlanetInfoTitle['text'] = 'Unknown'
        self.PlanetInfoAttributesTable['text'] = ''
        self.planet_info_rescource_table['text'] = ''
        self.planet_info_goods_table['text'] = ''
        self.planet_info_ENR_table['text'] = ''

        self.empty_messages()

    def show(self):
        self.PlanetInfoPanel.show()

    def hide(self):
        self.PlanetInfoPanel.hide()

    def check_buttons(self):
        if type(self.obj) == Star:
            self.PlanetInfoBuildButton.hide()
            self.PlanetInfoColoniseButton.hide()
            self.PlanetInfoProbeButton.hide()
            return

        if self.obj.colonised:
            self.PlanetInfoBuildButton.show()
            self.PlanetInfoColoniseButton.hide()
            self.PlanetInfoProbeButton.hide()
        elif self.obj.probed:
            self.PlanetInfoBuildButton.hide()
            self.PlanetInfoColoniseButton.show()
            self.PlanetInfoProbeButton.hide()
        else:
            self.PlanetInfoBuildButton.hide()
            self.PlanetInfoColoniseButton.hide()
            self.PlanetInfoProbeButton.show()

    def load_messages(self):
        if type(self.obj) != Star:
            if len(self.obj.messages) > 0:
                self.message_panel_bg_text.hide()
                i = 0
                for id, message in self.obj.messages.items():
                    mText = message['text'] + '\n' + str(message['value'])

                    msgPanel = DirectFrame(
                        pos=(0, 0, 0.35 - i * 0.21), frameColor=(0.2, 0.2, 0.3, 0.2), frameSize=(-0.2, 0.2, -0.1, 0.1),
                        text=mText, text_pos=(0, 0.05), text_scale=0.05, text_fg=(1, 1, 1, 1), text_wordwrap=8,
                        parent=self.PlanetInfoMessagePanel)

                    self.messagesDict.update({id: msgPanel})
                    i += 1
            else:
                self.message_panel_bg_text.show()

    def empty_messages(self):
        for id, panel in self.messagesDict.items():
            panel.destroy()
        self.messagesDict = {}

    def show_probe_mission(self):
        planet1 = self.world.capitalPlanet
        planet2 = self.obj
        name = self.selectedObjectName
        dist = round(self.world.calc_distance_between_planets(planet1, planet2), 3)
        time = round(dist * 2)
        cost = 500 + round(dist * 67)
        missionText = "Probe misson to {}:\nDistance: {}\nDuration: {}\nCosts: {}".format(name, dist, time, cost)
        self.world.create_dialog(missionText, 'yesNo', self.start_probe_mission, [planet2, name, dist, time, cost])

    def start_probe_mission(self, planet, name, dist, time, cost):
        if self.world.money >= cost:
            self.world.money -= cost
            id = 'probe' + planet.name
            self.world.add_message(planet, id, 'info', 'Probing Mission', time)
            taskMgr.doMethodLater(
                1, self.probe_mission_task,
                'probeMissionTask',
                extraArgs=[planet, id],
                appendTask=True
            )
        else:
            self.world.create_dialog("Not enough Money")

    def probe_mission_task(self, planet, id, task):
        if planet.messages[id]['value'] > 0:
            planet.messages[id]['value'] -= 1
        else:
            planet.probed = True
            self.world.remove_message(planet, id)
            return task.done
        return task.again

    def show_colonise_mission(self):
        planet1 = self.world.capitalPlanet
        planet2 = self.obj
        name = self.selectedObjectName
        dist = round(self.world.calc_distance_between_planets(planet1, planet2), 3)
        time = round(dist * 4)
        cost = 3900 + round(dist * 123)
        missionText = "Colonise misson to {}:\nDistance: {}\nDuration: {}\nCosts: {}".format(name, dist, time, cost)
        self.world.create_dialog(missionText, 'yesNo', self.start_colonise_mission, [planet2, name, dist, time, cost])

    def start_colonise_mission(self, planet, name, dist, time, cost):
        if self.world.money >= cost:
            self.world.money -= cost
            id = 'colonise' + planet.name
            self.world.add_message(planet, id, 'info', 'Colonise Mission', time)
            taskMgr.doMethodLater(1, self.colonise_mission_task, 'coloniseMissionTask', extraArgs=[planet, id], appendTask=True)
        else:
            self.world.create_dialog("Not enough Money")

    def colonise_mission_task(self, planet, id, task):
        if planet.messages[id]['value'] > 0:
            planet.messages[id]['value'] -= 1
        else:
            planet.colonised = True
            planet.messages.pop(id)
            taskMgr.doMethodLater(self.world.population_time_delta,
                                  self.world.populate_planet_task,
                                  'populatePlanetTask',
                                  extraArgs=[planet],
                                  appendTask=True)
            return task.done
        return task.again

    def toggle_planet_build_mode(self, mode=False):
        pos = self.obj.getPos()
        camPos = camera.getPos()
        obj = self.obj
        scale = self.followObjectScale

        if mode:
            self.hide()
            self.clear()
            taskMgr.remove('infocamTask')
            self.NewPlanetBuildView.reset(obj)

            zoomInterval = Sequence(
                camera.posHprInterval(0.3, Point3(pos[0] - scale * 0.9, pos[1] - scale * 3.4, 0), Vec3(0, 0, 0), camPos),
                Func(self.NewPlanetBuildView.show))
            zoomInterval.start()

            taskMgr.add(self.world.set_follow_cam_task, 'buildcamTask', extraArgs=[obj, scale, 'build'], appendTask=True)
            taskMgr.add(self.NewPlanetBuildView.refresh_quickinfo_task, 'quickinfoTask', extraArgs=[obj], appendTask=True)

        else:
            self.NewPlanetBuildView.hide()
            self.NewPlanetBuildView.clear()
            taskMgr.remove('quickinfoTask')
            taskMgr.remove('buildcamTask')
            self.reset(obj)

            zoomInterval = Sequence(
                camera.posHprInterval(0.3, Point3(pos[0] - scale * 1.25, pos[1] - scale * 4, scale * 4), Vec3(0, -45, 0), camPos),
                Func(self.show))
            zoomInterval.start()

            taskMgr.add(self.world.set_follow_cam_task, 'infocamTask', extraArgs=[obj, scale, 'info'], appendTask=True)

        return None

    def create_gui(self):
        self.infoPanelMap = loader.loadModel('models/gui/panels/planetinfopanel_maps.egg').find('**/planetinfopanel')
        self.problemPanelMap = loader.loadModel('models/gui/panels/planetproblempanel_maps.egg').find('**/planetproblempanel')

        self.PlanetInfoPanel = DirectFrame(
            pos=(-0.8, 0, 0), frameColor=(0.2, 0.2, 0.22, 0), frameSize=(-0.9, 1.1, -0.65, 0.65),
            geom=self.infoPanelMap, geom_scale=(0.65, 0, 0.65), geom_pos=(0.1, 0, 0), enableEdit=1)
        self.PlanetInfoPanel.hide()

        self.PlanetInfoTitle = DirectLabel(
            text='', pos=(0.1, 0, 0.5), frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1), text_align=TextNode.ACenter, text_scale=0.12,
            parent=self.PlanetInfoPanel,)

        self.PlanetInfoAttributesTable = DirectLabel(
            text='', pos=(-0.85, 0, 0.35), frameColor=(0, 0, 0, 0), scale=0.13,
            text_fg=(1, 1, 1, 1), text_align=TextNode.ALeft, text_scale=0.5,
            parent=self.PlanetInfoPanel)

        self.planet_info_rescource_table = DirectLabel(
            text='', pos=(-0.85, 0, -0.05), frameColor=(0, 0, 0, 0), scale=0.13,
            text_fg=(1, 1, 1, 1), text_align=TextNode.ALeft, text_scale=0.5,
            parent=self.PlanetInfoPanel)

        self.planet_info_goods_table = DirectLabel(
            text='', pos=(-0.85, 0, -0.4), frameColor=(0, 0, 0, 0), scale=0.13,
            text_fg=(1, 1, 1, 1), text_align=TextNode.ALeft, text_scale=0.5,
            parent=self.PlanetInfoPanel)

        self.planet_info_ENR_table = DirectLabel(
            text='', pos=(0.28, 0, 0.35), frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1), text_align=TextNode.ALeft, scale=0.13, text_scale=0.5,
            parent=self.PlanetInfoPanel)

        self.PlanetInfoCloseButton = DirectButton(
            text='Close', pos=(-0.735, 0, -0.9), scale=0.5, pad=(-0.1, -0.09),
            frameColor=(0, 0, 0, 0), parent=self.PlanetInfoPanel,
            geom=(self.world.buttonMaps), geom_scale=(0.7, 0, 1),
            text_scale=0.15, text_pos=(0, -0.03), text_fg=(1, 1, 1, 1),
            command=self.world.toggle_planet_info_mode, extraArgs=[False])

        self.PlanetInfoProbeButton = DirectButton(
            text='Probe', pos=(1.45, 0, 0.55), pad=(0.055, 0.02), borderWidth=(0.01, 0.01),
            text_scale=0.07, frameColor=(0.15, 0.15, 0.15, 0.9), text_fg=(1, 1, 1, 1),
            command=self.show_probe_mission, parent=self.PlanetInfoPanel)

        self.PlanetInfoColoniseButton = DirectButton(
            text='Colonise', pos=(1.85, 0, 0.55), pad=(0.03, 0.02), borderWidth=(0.01, 0.01),
            text_scale=0.07, frameColor=(0.15, 0.15, 0.15, 0.9), text_fg=(1, 1, 1, 1),
            command=self.show_colonise_mission, parent=self.PlanetInfoPanel)

        self.PlanetInfoBuildButton = DirectButton(
            text='Build', pos=(1.65, 0, -0.58), scale=0.5, pad=(-0.1, -0.09),
            frameColor=(0, 0, 0, 0), parent=self.PlanetInfoPanel,
            text_scale=0.15, text_pos=(0, -0.03), text_fg=(1, 1, 1, 1),
            geom_scale=(0.5, 0, 1.2), geom=(self.world.buttonMaps),
            command=self.toggle_planet_build_mode, extraArgs=[True])

        self.PlanetInfoMessagePanel = DirectFrame(
            pos=(2.33, 0, 0.16), frameColor=(0.2, 0.2, 0.22, 0), frameSize=(0, 0, 0, 0),
            geom=self.problemPanelMap, geom_scale=(0.7, 0, 0.7), geom_pos=(0, 0, 0),
            parent=self.PlanetInfoPanel)

        self.message_panel_bg_text = DirectLabel(
            text='No\nIncidents', pos=(0, 0, 0), frameColor=(0, 0, 0, 0),
            text_fg=(0.6, 0.6, 0.6, 0.6), text_align=TextNode.ACenter, text_scale=0.05,
            parent=self.PlanetInfoMessagePanel)
