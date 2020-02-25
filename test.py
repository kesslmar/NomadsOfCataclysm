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


if __name__ == "__main__":
    unittest.main(verbosity=2)
