import unittest

from constants import (
    BOARDHEIGHT, BOARDWIDTH, BOXSIZE, FPS, GAPSIZE, REVEALSPEED, WINDOWHEIGHT,
    WINDOWWIDTH)


class TestColors(unittest.TestCase):
    def test_constants(self):
        self.assertTrue(BOARDHEIGHT > 0)
        self.assertTrue(BOARDWIDTH > 0)
        self.assertTrue(BOXSIZE > 0)
        self.assertTrue(FPS > 0)
        self.assertTrue(GAPSIZE > 0)
        self.assertTrue(REVEALSPEED > 0)
        self.assertTrue(WINDOWHEIGHT > 0)
        self.assertTrue(WINDOWWIDTH > 0)

    def test_even_pairs(self):
        self.assertEquals(BOARDWIDTH * BOARDHEIGHT % 2, 0,
                          "Board needs to have even number of boxes"
                          "for pairs of matches.")
