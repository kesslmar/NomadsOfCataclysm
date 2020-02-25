
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from panda3d.core import *


class PlanetBuildView():
    def __init__(self, world):
        self.world = world
        self.obj = None
        self.ActiveBuildSection = 'RES'
        self.ActiveBlueprint = None
        self.ActiveBuildSlot = [None]
        self.PlanetBuildPanelContent = []
        self.PlanetBuildSlotButtons = []

        self.create_gui()

    def reset(self, obj):
        self.clear()
        self.obj = obj
        self.fill()
        self.check_construct_button()
        self.check_salvage_and_info()
        self.update_slots()

    def show(self):
        self.PlanetBuildPanel.show()

    def hide(self):
        self.PlanetBuildPanel.hide()

    def fill(self):
        i = 0
        section = self.ActiveBuildSection

        for k, v in self.world.BuildingsDB[section].items():
            newBlueprint = DirectButton(
                frameColor=(0.15, 0.15, 0.15, 0.7),
                frameSize=(-0.4, 0.4, -0.125, 0.125), relief='flat',
                text=k, text_fg=(0, 0, 0, 0),
                pos=(0, 0, 0.53 - i * 0.26), parent=self.PlanetBuildPanel,
                command=self.switch_build_blueprint)
            newBlueprint['extraArgs'] = [newBlueprint, v]
            self.PlanetBuildPanelContent.append(newBlueprint)

            OnscreenImage(  # Append image to blueprint
                image=v['img'], pos=(-0.27, 0, 0.003), scale=(0.125, 1, 0.12), parent=(newBlueprint))

            DirectLabel(  # Add title to blueprint
                text=k, pos=(-0.1, 0, 0.05), text_fg=(1, 1, 1, 1), frameColor=(0, 0, 0, 0),
                parent=newBlueprint, text_align=TextNode.ALeft, text_scale=0.06)

            DirectLabel(  # Add attribute text to blueprint
                text=('Price: ' + str(v['Price'])), pos=(-0.1, 0, -0.02), text_fg=(1, 1, 1, 1),
                frameColor=(0, 0, 0, 0), parent=newBlueprint, text_align=TextNode.ALeft, text_scale=0.045)

            i += 1

    def clear(self):
        for element in self.PlanetBuildPanelContent:
            element.destroy()
        self.PlanetBuildPanelContent = []
        self.ActiveBlueprint = None
        self.PlanetBuildDescriptionText['text'] = ''

        slot = self.ActiveBuildSlot[0]

        if slot is not None:
            self.ActiveBuildSlot[0] = None
            self.PlanetBuildSlotButtons[int(slot) - 1]['indicatorValue'] = 0

    def switch_build_section(self, section, button):
        if section != self.ActiveBuildSection:
            self.PlanetBuildRESButton['relief'] = 'raised'
            self.PlanetBuildPROButton['relief'] = 'raised'
            self.PlanetBuildENRButton['relief'] = 'raised'
            self.PlanetBuildDEVButton['relief'] = 'raised'
            self.PlanetBuildHABButton['relief'] = 'raised'

            button['relief'] = 'sunken'

            self.clear()
            self.check_construct_button()
            self.check_salvage_and_info()
            self.ActiveBuildSection = section

            pos = self.PlanetBuildSlotContainer.getPos()
            swipeOutInterval = self.PlanetBuildSlotContainer.posInterval(0.2, Point3(pos[0], pos[1], pos[2] + 2), pos)
            swipeInInterval = self.PlanetBuildSlotContainer.posInterval(0.2, pos, Point3(pos[0], pos[1], pos[2] - 2))

            mySeq = Sequence(swipeOutInterval, Func(self.update_slots), swipeInInterval)
            mySeq.start()
            self.fill()

    def switch_build_slot(self):

        self.check_construct_button()
        self.check_salvage_and_info()

    def switch_build_blueprint(self, blueprint, building):
        if self.ActiveBlueprint is not None:
            self.ActiveBlueprint['frameColor'] = (0.15, 0.15, 0.15, 0.9)
        else:
            self.PlanetBuildDescriptionField.show()
        self.ActiveBlueprint = blueprint
        blueprint['frameColor'] = (0.3, 0.3, 0.3, 0.9)

        self.PlanetBuildDescriptionText['text'] = (building['desc'] + '\n\n'
                                                   'Requires: ' + building['reqText'] + '\n\n'
                                                   'Yields: ' + building['yieldText'])

        self.check_construct_button()

    def check_construct_button(self):
        section = self.ActiveBuildSection

        construction_possible = (
            self.ActiveBlueprint is not None
            and self.ActiveBuildSlot[0] is not None
            and self.obj.slots[section][self.ActiveBuildSlot[0]] is None
        )

        if construction_possible:
            self.PlanetBuildConstructButton['state'] = 'normal'
            self.PlanetBuildConstructButton['text_fg'] = (1, 1, 1, 1)
        else:
            self.PlanetBuildConstructButton['state'] = 'disabled'
            self.PlanetBuildConstructButton['text_fg'] = (0.5, 0.5, 0.5, 1)

    def check_salvage_and_info(self):
        planet = self.obj.name
        section = self.ActiveBuildSection

        if self.ActiveBuildSlot[0] is not None and self.obj.slots[section][self.ActiveBuildSlot[0]] is not None:
            self.PlanetBuildSalvageButton['state'] = 'normal'
            self.PlanetBuildSalvageButton['text_fg'] = (1, 1, 1, 1)
            self.PlanetBuildSlotInfo.show()
            self.fill_slot_info(planet, section, self.ActiveBuildSlot[0])
        else:
            self.PlanetBuildSalvageButton['state'] = 'disabled'
            self.PlanetBuildSalvageButton['text_fg'] = (0.5, 0.5, 0.5, 1)
            self.PlanetBuildSlotInfo.hide()

    def fill_slot_info(self, planet, section, slot):
        if None not in (planet, section, slot):
            DBslot = self.obj.slots[section][slot]

            if DBslot['problemText'] == '':
                problemText = DBslot['name'] + ' is running as intended'
            else:
                problemText = DBslot['problemText']

            self.PlanetBuildSlotInfoText['text'] = problemText

    def construct_building(self):
        planet = self.obj
        section = self.ActiveBuildSection
        slot = self.ActiveBuildSlot[0]
        blueprint = self.ActiveBlueprint['text']
        price = self.world.BuildingsDB[section][blueprint]['Price']

        getsBuild = False
        add_PRO_task = False
        add_RES_task = False
        add_consume_task = False

        if self.world.money >= price:
            if section == 'ENR':
                getsBuild = True
                self.obj.energy_cap += self.world.BuildingsDB[section][blueprint]['incVal']
                if blueprint == 'Coal Generator' or blueprint == 'Nuclear Reactor':
                    add_consume_task = True
            else:
                if self.obj.energy_usg + self.world.BuildingsDB[section][blueprint]['enrgDrain'] <= self.obj.energy_cap:
                    if section == 'RES':
                        if self.world.BuildingsDB[section][blueprint]['req'] == 'Athmosphere':
                            if self.obj.athmosphere:
                                getsBuild = True
                                add_RES_task = True
                                self.obj.energy_usg += self.world.BuildingsDB[section][blueprint]['enrgDrain']
                            else:
                                self.world.create_dialog('No Athmosphere present')
                        elif self.world.BuildingsDB[section][blueprint]['req'] in self.obj.rescources:
                            getsBuild = True
                            add_RES_task = True
                            self.obj.energy_usg += self.world.BuildingsDB[section][blueprint]['enrgDrain']
                        else:
                            self.world.create_dialog('Needed Rescource is not available')
                    elif section == 'PRO':
                        getsBuild = True
                        add_PRO_task = True
                        self.obj.energy_usg += self.world.BuildingsDB[section][blueprint]['enrgDrain']
                    elif section == 'HAB':
                        getsBuild = True
                        self.obj.habitation_cap += self.world.BuildingsDB[section][blueprint]['incVal']
                        self.obj.energy_usg += self.world.BuildingsDB[section][blueprint]['enrgDrain']
                    elif section == 'DEV':
                        getsBuild = True
                        self.obj.energy_usg += self.world.BuildingsDB[section][blueprint]['enrgDrain']
                else:
                    self.world.create_dialog('Not sufficient Energy')
        else:
            self.world.create_dialog('Not enough Money')

        if getsBuild:
            self.obj.slots[section][slot] = {'name': blueprint, 'gotProblem': False, 'problemText': '', 'workers': 0, 'output': 0}
            self.world.money -= price
            self.update_slots()

        if add_RES_task:
            good = self.world.BuildingsDB[section][blueprint]['yield']
            incVal = self.world.BuildingsDB[section][blueprint]['incVal']
            taskMgr.doMethodLater(
                3, self.extract_rescource_task, blueprint + slot,
                extraArgs=[planet, section, slot, good, incVal],
                appendTask=True)

        if add_PRO_task:
            inGood = self.world.BuildingsDB[section][blueprint]['req']
            outGood = self.world.BuildingsDB[section][blueprint]['yield']
            incVal = self.world.BuildingsDB[section][blueprint]['incVal']
            decVal = self.world.BuildingsDB[section][blueprint]['decVal']
            taskMgr.doMethodLater(
                3, self.process_good_task, blueprint + slot,
                extraArgs=[planet, section, slot, inGood, outGood, incVal, decVal],
                appendTask=True)

        if add_consume_task:
            good = self.world.BuildingsDB[section][blueprint]['req']
            decVal = self.world.BuildingsDB[section][blueprint]['decVal']
            incVal = self.world.BuildingsDB[section][blueprint]['incVal']
            taskMgr.doMethodLater(
                3, self.consume_good_task, blueprint + slot,
                extraArgs=[planet, section, slot, good, decVal, incVal],
                appendTask=True)

        self.check_construct_button()
        self.check_salvage_and_info()

    def salvage_building(self):
        slot = self.ActiveBuildSlot[0]
        section = self.ActiveBuildSection
        blueprint = self.obj.slots[section][slot]['name']
        price = self.world.BuildingsDB[section][blueprint]['Price']
        incVal = self.world.BuildingsDB[section][blueprint]['incVal']
        enrgDrain = self.world.BuildingsDB[section][blueprint]['enrgDrain']

        getsSalvaged = True

        if section == 'ENR':
            if (self.obj.energy_cap - incVal) < self.obj.energy_usg:
                self.world.create_dialog('Energy too low if salvaged')
                getsSalvaged = False
            else:
                self.obj.energy_cap -= incVal

        if getsSalvaged:
            self.obj.slots[section][slot] = None
            self.obj.energy_usg -= enrgDrain
            self.world.money += round(price * self.world.salvage_factor)
            self.update_slots()

            taskMgr.remove(blueprint + slot)
            self.check_salvage_and_info()
            self.check_construct_button()

    def update_slots(self):
        section = self.ActiveBuildSection
        data = self.obj.slots[section]
        fl = section[0]

        ctr = 0
        for button in self.PlanetBuildSlotButtons:
            buttonLabel = self.PlanetBuildSlotLabels[ctr]

            if data[str(ctr + 1)] is not None:
                buttonLabel['text'] = data[str(ctr + 1)]['name']
                if data[str(ctr + 1)]['gotProblem']:
                    buttonLabel['text'] += '\n/!\\PROBLEM/!\\'
            else:
                buttonLabel['text'] = ''
            button['text'] = fl + str(ctr + 1)
            ctr += 1

    def refresh_quickinfo_task(self, planet, task):
        athm = planet.athmosphere
        wind = planet.wind
        enrgUsg = planet.energy_usg
        enrgCap = planet.energy_cap
        pop = planet.population
        habCap = planet.habitation_cap

        self.PlanetBuildQuickText1['text'] = (
            'ATHM: {} - WIND: {} - ENR: {}/{} - POP: {}/{}'.format(athm, wind, enrgUsg, enrgCap, pop, habCap)
        )

        self.PlanetBuildQuickText2['text'] = 'RES: '
        for k, v in planet.rescources.items():
            self.PlanetBuildQuickText2['text'] += k + ', '

        self.PlanetBuildQuickText3['text'] = 'GOODS: '
        if planet.goods:
            for k, v in planet.goods.items():
                self.PlanetBuildQuickText3['text'] += str(v) + ' ' + k + ' - '
        return task.cont

    def extract_rescource_task(self, planet, section, slot, good, incVal, task):

        if not (good in planet.goods):
            planet.goods.update({good: 0})

        if planet.energy_cap < planet.energy_usg:
            if not planet.slots[section][slot]['gotProblem']:
                planet.slots[section][slot]['gotProblem'] = True
                planet.slots[section][slot]['problemText'] = 'Not enough energy to continue extraction'
                self.update_slots()
                self.fill_slot_info(planet, section, slot)
        elif planet.goods[good] >= self.world.goods_cap:
            if not planet.slots[section][slot]['gotProblem']:
                planet.slots[section][slot]['gotProblem'] = True
                planet.slots[section][slot]['problemText'] = 'Storage is full'
                self.update_slots()
                self.fill_slot_info(planet, section, slot)
        else:
            if planet.slots[section][slot]['gotProblem']:
                planet.slots[section][slot]['gotProblem'] = False
                planet.slots[section][slot]['problemText'] = ''
                self.update_slots()
                self.fill_slot_info(planet, section, slot)
            planet.goods[good] += incVal

        return task.again

    def process_good_task(self, planet, section, slot, inGood, outGood, incVal, decVal, task):

        if not (inGood in planet.goods) or planet.goods[inGood] < decVal:
            if not planet.slots[section][slot]['gotProblem']:
                planet.slots[section][slot]['gotProblem'] = True
                planet.slots[section][slot]['problemText'] = 'Missing {} to continue production'.format(inGood)
                self.update_slots()
                self.fill_slot_info(planet, section, slot)
        elif planet.energy_cap < planet.energy_usg:
            if not planet.slots[section][slot]['gotProblem']:
                planet.slots[section][slot]['gotProblem'] = True
                planet.slots[section][slot]['problemText'] = 'Not enough energy to continue production'
                self.update_slots()
                self.fill_slot_info(planet, section, slot)
        elif planet.goods[outGood] >= self.world.goods_cap:
            if not planet.slots[section][slot]['gotProblem']:
                planet.slots[section][slot]['gotProblem'] = True
                planet.slots[section][slot]['problemText'] = 'Storage is full'
                self.update_slots()
                self.fill_slot_info(planet, section, slot)
        else:
            if planet.slots[section][slot]['gotProblem']:
                planet.slots[section][slot]['gotProblem'] = False
                planet.slots[section][slot]['problemText'] = ''
                self.update_slots()
                self.fill_slot_info(planet, section, slot)

            planet.goods[inGood] -= decVal
            if not (outGood in planet.goods):
                planet.goods.update({outGood: 0})
            planet.goods[outGood] += incVal

        return task.again

    def consume_good_task(self, planet, section, slot, good, decVal, incVal, task):

        if not (good in planet.goods) or planet.goods[good] < decVal:
            if not planet.slots[section][slot]['gotProblem']:
                planet.slots[section][slot]['gotProblem'] = True
                planet.slots[section][slot]['problemText'] = 'Missing {} to continue service'.format(good)
                self.update_slots()
                self.fill_slot_info(planet, section, slot)
                if section == 'ENR':
                    planet.energy_cap -= incVal
        else:
            if planet.slots[section][slot]['gotProblem']:
                planet.slots[section][slot]['gotProblem'] = False
                planet.slots[section][slot]['problemText'] = ''
                self.update_slots()
                self.fill_slot_info(planet, section, slot)
                if section == 'ENR':
                    planet.energy_cap += incVal
            planet.goods[good] -= decVal

        return task.again

    def create_gui(self):

        # Main build panel, description field and construct/salvage buttons
        # -----------------------------------------------------------------
        self.build_panel_map = loader.loadModel(
            'models/gui/panels/blueprintlist_maps.egg').find('**/blueprintlist')
        self.build_description_map = loader.loadModel(
            'models/gui/panels/blueprintdescription_maps.egg').find('**/blueprintdescription')

        self.PlanetBuildPanel = DirectFrame(
            frameColor=(0.15, 0.15, 0.15, 0), frameSize=(-0.4, 1.23, 0.66, -0.65), pos=(-1.35, 0, 0),
            geom=self.build_panel_map, geom_scale=(0.77, 1, 0.77), geom_pos=(0, 0, 0.08))
        self.PlanetBuildPanel.hide()

        self.PlanetBuildPanelContent = []

        self.PlanetBuildDescriptionField = DirectFrame(
            pos=(0.825, 0, 0.41), frameColor=(0.2, 0.2, 0.22, 0), frameSize=(-0.4, 0.4, 0.25, -0.25),
            geom=self.build_description_map, geom_scale=(0.7, 1, 0.77), geom_pos=(0.02, 0, -0.047),
            parent=self.PlanetBuildPanel)

        self.PlanetBuildDescriptionText = DirectLabel(
            text='', pos=(-0.35, 0, 0.19), frameSize=(0, 0.8, 0, 0.5), frameColor=(0, 0, 0, 0),
            text_scale=0.05, text_wordwrap=15, text_fg=(1, 1, 1, 1), text_align=TextNode.ALeft,
            parent=self.PlanetBuildDescriptionField)

        self.PlanetBuildConstructButton = DirectButton(
            text='Construct ->', pos=(-0.095, 0, -0.48), pad=(0.05, 0.02), borderWidth=(0.01, 0.01),
            text_scale=0.08, frameColor=(0.15, 0.15, 0.15, 0.9), text_fg=(1, 1, 1, 1),
            command=self.construct_building, parent=self.PlanetBuildDescriptionField, state='disabled')

        self.PlanetBuildSalvageButton = DirectButton(
            text='<- Salvage', pos=(-0.099, 0, -0.62), pad=(0.085, 0.013), borderWidth=(0.01, 0.01),
            text_scale=0.08, frameColor=(0.15, 0.15, 0.15, 0.9), text_fg=(1, 1, 1, 1),
            command=self.salvage_building, parent=self.PlanetBuildDescriptionField, state='disabled')

        self.PlanetBuildCloseButton = DirectButton(
            text='Back', pos=(-0.18, 0, -0.9), scale=0.5, pad=(-0.1, -0.09), frameColor=(0, 0, 0, 0),
            text_scale=0.15, text_pos=(0, -0.03), text_fg=(1, 1, 1, 1), geom_scale=(0.7, 0, 1), geom=(self.world.buttonMaps),
            command=self.world.NewPlanetInfoView.toggle_planet_build_mode, extraArgs=[False], parent=self.PlanetBuildPanel)

        # Section select buttons
        # ----------------------
        self.PlanetBuildRESButton = DirectButton(
            text='Rescources', pos=(0.4, 0, 0.75), pad=(0.03, 0.02), borderWidth=(0.01, 0.01),
            text_scale=0.06, frameColor=(0.15, 0.15, 0.15, 0.9), text_fg=(1, 1, 1, 1),
            command=self.switch_build_section, parent=self.PlanetBuildPanel, relief='sunken')
        self.PlanetBuildRESButton['extraArgs'] = ['RES', self.PlanetBuildRESButton]

        self.PlanetBuildPROButton = DirectButton(
            text='Production', pos=(0.79, 0, 0.75), pad=(0.03, 0.02), borderWidth=(0.01, 0.01),
            text_scale=0.06, frameColor=(0.15, 0.15, 0.15, 0.9), text_fg=(1, 1, 1, 1),
            command=self.switch_build_section, parent=self.PlanetBuildPanel)
        self.PlanetBuildPROButton['extraArgs'] = ['PRO', self.PlanetBuildPROButton]

        self.PlanetBuildENRButton = DirectButton(
            text='Energy', pos=(1.19, 0, 0.755), pad=(0.1, 0.017), borderWidth=(0.01, 0.01),
            text_scale=0.06, frameColor=(0.15, 0.15, 0.15, 0.9), text_fg=(1, 1, 1, 1),
            command=self.switch_build_section, parent=self.PlanetBuildPanel)
        self.PlanetBuildENRButton['extraArgs'] = ['ENR', self.PlanetBuildENRButton]

        self.PlanetBuildDEVButton = DirectButton(
            text='Developement', pos=(1.64, 0, 0.755), pad=(0.03, 0.017), borderWidth=(0.01, 0.01),
            text_scale=0.06, frameColor=(0.15, 0.15, 0.15, 0.9), text_fg=(1, 1, 1, 1),
            command=self.switch_build_section, parent=self.PlanetBuildPanel)
        self.PlanetBuildDEVButton['extraArgs'] = ['DEV', self.PlanetBuildDEVButton]

        self.PlanetBuildHABButton = DirectButton(
            text='Habitation', pos=(2.06, 0, 0.75), pad=(0.03, 0.02), borderWidth=(0.01, 0.01),
            text_scale=0.06, frameColor=(0.15, 0.15, 0.15, 0.9), text_fg=(1, 1, 1, 1),
            command=self.switch_build_section, parent=self.PlanetBuildPanel)
        self.PlanetBuildHABButton['extraArgs'] = ['HAB', self.PlanetBuildHABButton]

        # Elements for the quick info
        # ---------------------------
        self.PlanetBuildQuickInfo = DirectFrame(
            frameSize=(0, 1.63, -0.08, 0.07), pos=(-0.4, 0, -0.73),
            frameColor=(0.15, 0.15, 0.15, 0.9), parent=self.PlanetBuildPanel)

        self.PlanetBuildQuickText1 = DirectLabel(
            text='ATHM: Yes  -  WIND: 1  -  HAB: 20/100  -  ENR: 60/100',
            pos=(0.03, 0, 0.015), text_fg=(0.9, 0.9, 0.9, 1), frameColor=(0, 0, 0, 0), text_scale=0.05,
            frameSize=(0, 0.8, 0, 0.5), parent=self.PlanetBuildQuickInfo, text_align=TextNode.ALeft)

        self.PlanetBuildQuickText2 = DirectLabel(
            text='RES: Coal, Iron, Uranium',
            pos=(0.03, 0, -0.038), text_fg=(0.9, 0.9, 0.9, 1), frameColor=(0, 0, 0, 0), text_scale=0.05,
            frameSize=(0, 0.8, 0, 0.5), parent=self.PlanetBuildQuickInfo, text_align=TextNode.ALeft)

        self.PlanetBuildQuickText3 = DirectLabel(
            text='GOODS: Coal sacks, Uranium rods',
            pos=(0.7, 0, -0.038), text_fg=(0.9, 0.9, 0.9, 1), frameColor=(0, 0, 0, 0), text_scale=0.05,
            frameSize=(0, 0.8, 0, 0.5), parent=self.PlanetBuildQuickInfo, text_align=TextNode.ALeft)

        # Buttons and labels for the planet build slots
        # ----------------------------------------------
        slot_model = loader.loadModel('models/gui/slots/simple_slot_maps.egg')
        slot_maps = (slot_model.find('**/normal'), slot_model.find('**/active'),
                     slot_model.find('**/normal'), slot_model.find('**/disabled'))

        self.PlanetBuildSlotContainer = DirectFrame(pos=(1.5, 0, 0), frameColor=(0.5, 0.5, 0.5, 1))
        self.PlanetBuildSlotContainer.reparentTo(self.PlanetBuildPanel)

        self.PlanetBuildSlotButtons = [

            DirectRadioButton(
                text='R1', frameSize=(-0.035, 0.035, -0.035, 0.035), frameColor=(0, 0, 0, 0),
                pos=(0.27, 0, 0.53), scale=0.9, boxPlacement='center',
                text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1, 1, 1, 1),
                boxGeomScale=(0.18, 0, 0.18), boxGeom=(slot_maps), boxBorder=-0.245,
                command=self.switch_build_slot, variable=self.ActiveBuildSlot,
                indicatorValue=0, value=['1'], parent=self.PlanetBuildSlotContainer),

            DirectRadioButton(
                text='R2', frameSize=(-0.035, 0.035, -0.035, 0.035), frameColor=(0, 0, 0, 0),
                pos=(0.12, 0, 0.29), scale=0.9, boxPlacement='center',
                text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1, 1, 1, 1),
                boxGeomScale=(0.18, 0, 0.18), boxGeom=(slot_maps), boxBorder=-0.245,
                command=self.switch_build_slot, variable=self.ActiveBuildSlot,
                indicatorValue=0, value=['2'], parent=self.PlanetBuildSlotContainer),

            DirectRadioButton(
                text='R3', frameSize=(-0.035, 0.035, -0.035, 0.035), frameColor=(0, 0, 0, 0),
                pos=(0.05, 0, 0), scale=0.9, boxPlacement='center',
                text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1, 1, 1, 1),
                boxGeomScale=(0.18, 0, 0.18), boxGeom=(slot_maps), boxBorder=-0.245,
                command=self.switch_build_slot, variable=self.ActiveBuildSlot,
                indicatorValue=0, value=['3'], parent=self.PlanetBuildSlotContainer),

            DirectRadioButton(
                text='R4', frameSize=(-0.035, 0.035, -0.035, 0.035), frameColor=(0, 0, 0, 0),
                pos=(0.12, 0, -0.29), scale=0.9, boxPlacement='center',
                text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1, 1, 1, 1),
                boxGeomScale=(0.18, 0, 0.18), boxGeom=(slot_maps), boxBorder=-0.245,
                command=self.switch_build_slot, variable=self.ActiveBuildSlot,
                indicatorValue=0, value=['4'], parent=self.PlanetBuildSlotContainer),

            DirectRadioButton(
                text='R5', frameSize=(-0.035, 0.035, -0.035, 0.035), frameColor=(0, 0, 0, 0),
                pos=(0.27, 0, -0.53), scale=0.9, boxPlacement='center',
                text_scale=0.08, text_pos=(-0.22, -0.02), text_fg=(1, 1, 1, 1),
                boxGeomScale=(0.18, 0, 0.18), boxGeom=(slot_maps), boxBorder=-0.245,
                command=self.switch_build_slot, variable=self.ActiveBuildSlot,
                indicatorValue=0, value=['5'], parent=self.PlanetBuildSlotContainer),

        ]

        for button in self.PlanetBuildSlotButtons:
            button.setOthers(self.PlanetBuildSlotButtons)

        self.PlanetBuildSlotLabels = [

            DirectLabel(
                text='', text_scale=0.06, text_fg=(1, 1, 1, 1), text_bg=(0.2, 0.2, 0.2, 0.9),
                frameColor=(0, 0, 0, 0), pos=(0, 0, 0.07), parent=self.PlanetBuildSlotButtons[0]),

            DirectLabel(
                text='', text_scale=0.06, text_fg=(1, 1, 1, 1), text_bg=(0.2, 0.2, 0.2, 0.9),
                frameColor=(0, 0, 0, 0), pos=(0, 0, 0.07), parent=self.PlanetBuildSlotButtons[1]),

            DirectLabel(
                text='', text_scale=0.06, text_fg=(1, 1, 1, 1), text_bg=(0.2, 0.2, 0.2, 0.9),
                frameColor=(0, 0, 0, 0), pos=(0, 0, 0.07), parent=self.PlanetBuildSlotButtons[2]),

            DirectLabel(
                text='', text_scale=0.06, text_fg=(1, 1, 1, 1), text_bg=(0.2, 0.2, 0.2, 0.9),
                frameColor=(0, 0, 0, 0), pos=(0, 0, 0.07), parent=self.PlanetBuildSlotButtons[3]),

            DirectLabel(
                text='', text_scale=0.06, text_fg=(1, 1, 1, 1), text_bg=(0.2, 0.2, 0.2, 0.9),
                frameColor=(0, 0, 0, 0), pos=(0, 0, 0.07), parent=self.PlanetBuildSlotButtons[4])
        ]

        self.PlanetBuildSlotInfo = DirectFrame(
            pos=(0.4, 0, 0.35), frameSize=(0, 0.9, -0.7, 0), frameColor=(0.2, 0.2, 0.25, 0.8),
            parent=self.PlanetBuildSlotContainer, text_scale=0.03, text_fg=(1, 1, 1, 1))
        self.PlanetBuildSlotInfo.hide()

        self.PlanetBuildSlotInfoText = DirectLabel(
            text='', text_scale=0.06, text_fg=(1, 1, 1, 1), text_bg=(0, 0, 0, 0),
            frameColor=(0, 0, 0, 0), pos=(0.04, 0, -0.09), text_align=TextNode.ALeft, text_wordwrap=15,
            parent=self.PlanetBuildSlotInfo)
