import unittest

from colors import (
    BGCOLOR,
    BLUE,
    BOXCOLOR,
    CYAN,
    GRAY,
    GREEN,
    HIGHLIGHTCOLOR,
    IVORY,
    LIGHTBGCOLOR,
    NAVYBLUE,
    ORANGE,
    PURPLE,
    RED,
    WHITE,
    YELLOW)
from constants import (
    BOXSIZE,
    EASY_GAME_COLS,
    EASY_GAME_ROWS,
    FPS,
    GAME_COLS,
    GAME_ROWS,
    GAPSIZE,
    HARD_GAME_COLS,
    HARD_GAME_ROWS,
    MEDIUM_GAME_COLS,
    MEDIUM_GAME_ROWS,
    REVEALSPEED,
    WINDOWHEIGHT,
    WINDOWWIDTH)
from shapes import (
    DIAMOND,
    DONUT,
    LINES,
    OVAL,
    SQUARE)
from memorypuzzle import ALLCOLORS, ALLSHAPES


class TestGame(unittest.TestCase):
    def test_constants(self):
        self.assertTrue(GAME_ROWS > 0)
        self.assertTrue(GAME_COLS > 0)
        self.assertTrue(BOXSIZE > 0)
        self.assertTrue(FPS > 0)
        self.assertTrue(GAPSIZE > 0)
        self.assertTrue(REVEALSPEED > 0)
        self.assertTrue(WINDOWHEIGHT > 0)
        self.assertTrue(WINDOWWIDTH > 0)

    def test_even_pairs(self):
        self.assertEqual(GAME_COLS * GAME_ROWS % 2, 0,
                         "Board needs to have even number of boxes"
                         "for pairs of matches.")

    def test_color_shape_ratio(self):
        self.assertTrue(
            len(ALLCOLORS) * len(ALLSHAPES) * 4 >= GAME_COLS * GAME_ROWS,
            "Board is too big for the number of shapes/colors defined.")

    def test_color_values(self):
        colors = [
            BGCOLOR,
            BLUE,
            BOXCOLOR,
            CYAN,
            GRAY,
            GREEN,
            HIGHLIGHTCOLOR,
            IVORY,
            LIGHTBGCOLOR,
            NAVYBLUE,
            ORANGE,
            PURPLE,
            RED,
            WHITE,
            YELLOW]
        for color in colors:
            self.assertTrue(isinstance(color, tuple))
            self.assertEqual(3, len(color))
            self.assertTrue(
                0 <= color[0] <= 255 and
                0 <= color[1] <= 255 and
                0 <= color[2] <= 255)

    def test_all_constants(self):
        constants = [
            BOXSIZE,
            EASY_GAME_COLS,
            EASY_GAME_ROWS,
            FPS,
            GAME_COLS,
            GAME_ROWS,
            GAPSIZE,
            HARD_GAME_COLS,
            HARD_GAME_ROWS,
            MEDIUM_GAME_COLS,
            MEDIUM_GAME_ROWS,
            REVEALSPEED,
            WINDOWHEIGHT,
            WINDOWWIDTH]
        for constant in constants:
            self.assertTrue(constant > 0)

    def test_shapes(self):
        shapes = [
            DIAMOND,
            DONUT,
            LINES,
            OVAL,
            SQUARE]
        for shape in shapes:
            self.assertTrue(isinstance(shape, str))
            self.assertTrue(shape in ALLSHAPES, "%s not in ALLCOLORS" % shape)
