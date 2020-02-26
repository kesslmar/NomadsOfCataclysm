import unittest
from panda3d.core import *
from NoC import World


class TestNoC(unittest.TestCase):
    """ Testing if possible all game features and functions. Calls and
    potential Exceptions are more focused than actual test outcome"""

    @classmethod
    def setUpClass(cls):
        loadPrcFileData("", "window-type offscreen")
        cls.w = World()

    def setUp(self):
        self.w.reset_game

    def test_click_on_earth(self):
        """ Simulate click on Earth from Map View """
        self.w.toggle_planet_info_mode(True, self.w.Earth)
        self.assertEqual(self.w.NewPlanetInfoView.PlanetInfoTitle['text'], 'Earth')

    def test_build_windturbine(self):
        """ Simulate build process of a wind turbine on earth"""
        self.w.toggle_planet_info_mode(True, self.w.Earth)
        self.w.NewPlanetInfoView.toggle_planet_build_mode(True)
        
        self.w.NewPlanetBuildView.switch_build_section(
            'ENR', self.w.NewPlanetBuildView.PlanetBuildENRButton)
        
        self.w.NewPlanetBuildView.switch_build_blueprint(
            self.w.NewPlanetBuildView.PlanetBuildPanelContent[0],
            self.w.NewPlanetBuildView.PlanetBuildPanelContent[0]['extraArgs'][1])
        
        self.w.NewPlanetBuildView.ActiveBuildSlot = '1'
        self.w.NewPlanetBuildView.switch_build_slot()

        self.w.NewPlanetBuildView.construct_building()

        self.assertEqual(
            self.w.NewPlanetBuildView.PlanetBuildSlotLabels[0]['text'],
            'Wind Turbine')



if __name__ == "__main__":
    unittest.main(verbosity=2)
