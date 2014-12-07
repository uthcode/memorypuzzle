import sys
import unittest

import mock
from pygame.constants import QUIT, MOUSEBUTTONUP
import pygame
from mock import MagicMock

import memorypuzzle
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
    WINDOWWIDTH, HALF_BOXSIZE, QUARTER_BOXSIZE, GAME_WON_FLASH_WAIT,
    GAME_END_WAIT)
from shapes import (
    DIAMOND,
    DONUT,
    LINES,
    OVAL,
    SQUARE)
from memorypuzzle import ALLCOLORS, ALLSHAPES


TEST_BOARD = [
    [(LINES, ORANGE), (DIAMOND, ORANGE), (SQUARE, RED), (SQUARE, RED)],
    [(DIAMOND, CYAN), (SQUARE, PURPLE), (DIAMOND, ORANGE), (LINES, CYAN)],
    [(LINES, CYAN), (LINES, YELLOW), (SQUARE, PURPLE), (LINES, ORANGE)],
    [(DONUT, GREEN), (DONUT, CYAN), (DONUT, RED), (DONUT, CYAN)],
    [(DONUT, GREEN), (DIAMOND, CYAN), (LINES, YELLOW), (DONUT, RED)]]

TEST_BOX = (0, 0)
TEST_GRID = (EASY_GAME_ROWS, EASY_GAME_COLS)
LEFT_TOP_COORDS_OF_TEST_BOX = (195, 140)


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

    def test_get_game_clock_display(self):
        pygame.init = MagicMock()
        pygame.display = MagicMock()
        pygame.time = MagicMock()
        memorypuzzle.get_game_clock_display()
        pygame.init.assert_called_once_with()
        pygame.display.set_caption.assert_called_once_with("Memory Game")
        pygame.time.Clock.assert_called_once_with()
        pygame.display.set_mode.assert_called_once_with(
            (WINDOWWIDTH, WINDOWHEIGHT))

    def test_left_top_coords_of_box(self):
        left, top = memorypuzzle.left_top_coords_of_box(TEST_BOX, TEST_GRID)
        self.assertEquals(
            (left, top),
            LEFT_TOP_COORDS_OF_TEST_BOX,
            "Coordinates Differ From the calculated expected Value.")

    def test_draw_box_covers(self):
        pygame.draw = MagicMock()
        pygame.display = MagicMock()
        display_surface = MagicMock()
        fps_clock = MagicMock()
        left, top = LEFT_TOP_COORDS_OF_TEST_BOX
        memorypuzzle.draw_box_covers(
            display_surface,
            fps_clock,
            TEST_BOARD,
            [TEST_BOX],
            10,
            TEST_GRID)

        # TODO: How to assert the intermediaries with mock?
        # pygame.draw.rect.assert_called_with(
        # display_surface, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        # shape = DONUT
        # color = RED
        # quarter = int(BOXSIZE * 0.25)
        # half = int(BOXSIZE * 0.5)
        # pygame.draw.circle.assert_called_with(
        # display_surface, color, (left + half, top + half), (half - 5))
        # pygame.draw.circle.assert_called_with(
        #    display_surface, BGCOLOR, (left + half, top + half), quarter - 5)

        pygame.draw.rect.assert_called_with(
            display_surface, BOXCOLOR, (left, top, 10, BOXSIZE))
        pygame.display.update.assert_called_once_with()
        fps_clock.tick.assert_called_once_with(FPS)

    def test_draw_icon(self):
        pygame.draw = MagicMock()
        display_surface = MagicMock()
        left, top = LEFT_TOP_COORDS_OF_TEST_BOX
        memorypuzzle.draw_icon(display_surface, DONUT, RED, TEST_BOX, TEST_GRID)
        expected = [
            mock.call(
                display_surface,
                RED,
                (left + HALF_BOXSIZE, top + HALF_BOXSIZE),
                HALF_BOXSIZE - 5),
            mock.call(
                display_surface,
                BGCOLOR,
                (left + HALF_BOXSIZE, top + HALF_BOXSIZE),
                QUARTER_BOXSIZE - 5)
        ]
        self.assertTrue(pygame.draw.circle.call_args_list, expected)

    @mock.patch('memorypuzzle.draw_board', MagicMock())
    def test_game_won(self):
        display_surface = MagicMock()
        pygame.time = MagicMock()
        pygame.display = MagicMock()
        covered_boxes = memorypuzzle.generate_revealed_boxes_data(
            True,
            TEST_GRID)
        display_update_expected = [mock.call() for _ in range(10)]
        flash_colors = [LIGHTBGCOLOR, BGCOLOR]
        display_surface_fill_expected = [
            mock.call(flash_colors[count % 2]) for count in range(10)]
        time_wait_expected = [mock.call(GAME_WON_FLASH_WAIT) for _ in range(10)]
        time_wait_expected.append(mock.call(GAME_END_WAIT))
        draw_board_called = [
            mock.call(display_surface, TEST_BOARD, covered_boxes, TEST_GRID)
            for _ in range(10)]
        memorypuzzle.game_won(display_surface, TEST_BOARD, TEST_GRID)
        self.assertEqual(
            pygame.display.update.call_args_list,
            display_update_expected)
        self.assertEqual(display_surface.fill.call_args_list,
                         display_surface_fill_expected)
        self.assertEqual(pygame.time.wait.call_args_list,
                         time_wait_expected)
        self.assertEqual(
            memorypuzzle.draw_board.call_args_list,
            draw_board_called)

    @mock.patch('memorypuzzle.draw_box_covers', MagicMock())
    def test_cover_boxes_animation(self):
        display_surface = MagicMock()
        fps_clock = MagicMock()
        expected_box_covers = [
            mock.call(
                display_surface,
                fps_clock,
                TEST_BOARD,
                [TEST_BOX],
                coverage,
                TEST_GRID)
            for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED)]

        memorypuzzle.cover_boxes_animation(
            display_surface,
            fps_clock,
            TEST_BOARD,
            [TEST_BOX],
            TEST_GRID)
        self.assertEquals(
            memorypuzzle.draw_box_covers.call_args_list,
            expected_box_covers)

    def test_get_shape_and_color(self):
        self.assertEqual(
            (LINES, ORANGE),
            memorypuzzle.get_shape_and_color(TEST_BOARD, TEST_BOX))

    @mock.patch("memorypuzzle.draw_box_covers", MagicMock())
    def test_reveal_boxes_animation(self):
        display_surface = MagicMock()
        fps_clock = MagicMock()
        expected_draw_box_covers = [
            mock.call(
                display_surface,
                fps_clock,
                TEST_BOARD,
                [TEST_BOX],
                coverage,
                TEST_GRID)
            for coverage in range(BOXSIZE, -1, -REVEALSPEED)]
        memorypuzzle.reveal_boxes_animation(
            display_surface,
            fps_clock,
            TEST_BOARD,
            [TEST_BOX],
            TEST_GRID)
        self.assertEqual(
            expected_draw_box_covers,
            memorypuzzle.draw_box_covers.call_args_list)

    def test_draw_highlight_box(self):
        display_surface = MagicMock()
        left, top = LEFT_TOP_COORDS_OF_TEST_BOX
        pygame.draw = MagicMock()
        memorypuzzle.draw_highlight_box(display_surface, TEST_BOX, TEST_GRID)
        pygame.draw.rect.assert_called_once_with(
            display_surface,
            HIGHLIGHTCOLOR,
            (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10),
            4)

    def test_get_mouse_click(self):
        pygame.event = MagicMock()
        pygame.quit = MagicMock()
        sys.exit = MagicMock()
        pygame.event.type = QUIT
        pygame.event.get.return_value = [pygame.event]
        memorypuzzle.get_mouse_click()
        pygame.quit.assert_called_once_with()
        sys.exit.assert_called_once_with()

        pygame.event.type = MOUSEBUTTONUP
        pygame.event.pos = (100, 100)
        pygame.event.get.return_value = [pygame.event]
        self.assertEqual(
            (True, (100, 100)),
            memorypuzzle.get_mouse_click())

