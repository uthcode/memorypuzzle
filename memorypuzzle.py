"""Memory Puzzle Game.

This is a small memory puzzle game, where blocks of similar images will be
shown and you will be asked to guess, which boxes contained similar images.

Adapted from the original game written by Al Sweigart al@inventwithpython.com

@author: Senthil Kumaran <senthil@uthcode.com>
"""
import random
import sys

import pygame
from pygame.constants import QUIT, KEYUP, K_ESCAPE, MOUSEMOTION, MOUSEBUTTONUP

from constants import (
    GAME_ROWS, GAME_COLS, BOXSIZE, FPS, GAPSIZE, REVEALSPEED, WINDOWHEIGHT,
    WINDOWWIDTH, XMARGIN, YMARGIN)
from colors import (
    BGCOLOR, RED, GREEN, YELLOW, BLUE, ORANGE, PURPLE, CYAN, LIGHTBGCOLOR,
    BOXCOLOR, HIGHLIGHTCOLOR)
from shapes import (DONUT, SQUARE, DIAMOND, LINES, OVAL)


ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)


def get_fpsclock_displaysurface():
    """Get the Frames per second clock and Display Surface."""
    return pygame.time.Clock(), \
           pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


def game_won(display_surface, fps_clock, mainboard):
    """Won the game."""
    game_won_animation(display_surface, mainboard)
    pygame.time.wait(2000)
    # Reset the board
    mainboard = get_randomized_board()
    revealed_boxes = generate_revealed_boxes_data(False)
    # Show the fully unrevealed board for a second
    draw_board(display_surface, mainboard, revealed_boxes)
    pygame.display.update()
    pygame.time.wait(1000)
    # Replay the start game animation
    start_game_animation(display_surface,
                         fps_clock,
                         mainboard)
    return mainboard, revealed_boxes


def get_mouse_click():
    mouse_clicked = False
    mouse_xpos = 0  # used to store the x coordinate of the mouse event
    mouse_ypos = 0  # used to store the y coordinate of the mouse event
    for event in pygame.event.get():  # event handling loop
        if (event.type == QUIT or
                (event.type == KEYUP and event.key == K_ESCAPE)):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_xpos, mouse_ypos = event.pos
        elif event.type == MOUSEBUTTONUP:
            mouse_xpos, mouse_ypos = event.pos
            mouse_clicked = True
    return mouse_clicked, mouse_xpos, mouse_ypos


def game_loop(display_surface, fps_clock, mainboard):
    """The main loop of the game."""
    revealed_boxes = generate_revealed_boxes_data(False)
    first_selection = None

    while True:
        display_surface.fill(BGCOLOR)
        draw_board(display_surface, mainboard, revealed_boxes)
        mouse_clicked, mouse_xpos, mouse_ypos = get_mouse_click()
        boxx, boxy = get_box_at_pixel(mouse_xpos, mouse_ypos)
        if boxx is not None and boxy is not None:
            # The mouse is currently over the box
            if not revealed_boxes[boxx][boxy]:
                draw_highlight_box(display_surface, boxx, boxy)
            if not revealed_boxes[boxx][boxy] and mouse_clicked:
                reveal_boxes_animation(
                    display_surface,
                    fps_clock,
                    mainboard,
                    [(boxx, boxy)])
                revealed_boxes[boxx][boxy] = True  # Set the box as revealed.
                if first_selection is None:
                    first_selection = (boxx, boxy)
                else:
                    icon1shape, icon1color = \
                        get_shape_and_color(mainboard,
                                            first_selection[0],
                                            first_selection[1])
                    icon2shape, icon2color = \
                        get_shape_and_color(mainboard,
                                            boxx,
                                            boxy)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons do not match, Re-cover up both selections
                        pygame.time.wait(1000)
                        cover_boxes_animation(
                            display_surface,
                            fps_clock,
                            mainboard,
                            [(first_selection[0], first_selection[1]),
                             (boxx, boxy)])
                        revealed_boxes[first_selection[0]][
                            first_selection[1]] = False
                        revealed_boxes[boxx][boxy] = False
                    elif has_won(revealed_boxes):
                        # check if all pairs found.
                        mainboard, revealed_boxes = game_won(display_surface,
                                                             fps_clock,
                                                             mainboard)
                    first_selection = None
        # Redraw the screen and wait for the clock tick
        pygame.display.update()
        fps_clock.tick(FPS)


def main():
    """Run the Memory Puzzle Game."""
    pygame.init()
    pygame.display.set_caption("Memory Game")
    fps_clock, display_surface = get_fpsclock_displaysurface()
    mainboard = get_randomized_board()
    display_surface.fill(BGCOLOR)
    start_game_animation(display_surface, fps_clock, mainboard)
    game_loop(display_surface, fps_clock, mainboard)


def generate_revealed_boxes_data(val):
    """Generate Revealed Boxes Data."""
    revealed_boxes = []
    for _ in range(GAME_COLS):
        revealed_boxes.append([val] * GAME_ROWS)
    return revealed_boxes


def get_randomized_board():
    """Get the Randomized Board."""
    # Get a list of every possible shape in every possible color.
    icons = [(shape, color) for shape in ALLSHAPES for color in ALLCOLORS]
    random.shuffle(icons)
    num_icons_used = int(GAME_ROWS * GAME_COLS / 2)
    icons = icons[:num_icons_used] * 2
    random.shuffle(icons)

    # Create a board data structure with randomly placed icons
    board = []
    for _ in range(GAME_COLS):
        column = []
        for _ in range(GAME_ROWS):
            column.append(icons.pop(0))
        board.append(column)
    return board


def split_into_groups_of(group_size, the_list):
    """Split into Groups."""
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i:i + group_size])
    return result


def left_top_coords_of_box(boxx, boxy):
    """Top left coordinates of a box."""
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


def get_box_at_pixel(mouse_xpos, mouse_ypos):
    """Get the Box at a Pixel."""
    for boxx in range(GAME_COLS):
        for boxy in range(GAME_ROWS):
            left, top = left_top_coords_of_box(boxx, boxy)
            box_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box_rect.collidepoint(mouse_xpos, mouse_ypos):
                return boxx, boxy
    return None, None


def draw_icon(display_surface, shape, color, boxx, boxy):
    """Draw the game Icon."""
    quarter = int(BOXSIZE * 0.25)  # syntactic sugar
    half = int(BOXSIZE * 0.5)  # syntactic sugar
    left, top = left_top_coords_of_box(boxx, boxy)

    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(display_surface, color, (left + half, top + half),
                           half - 5)
        pygame.draw.circle(display_surface, BGCOLOR, (left + half, top + half),
                           quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(
            display_surface, color,
            (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(display_surface, color, (
            (left + half, top), (left + BOXSIZE - 1, top + half),
            (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(display_surface, color, (left, top + i),
                             (left + i, top))
            pygame.draw.line(
                display_surface, color, (left + i, top + BOXSIZE - 1),
                (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(display_surface, color,
                            (left, top + quarter, BOXSIZE, half))


def get_shape_and_color(board, boxx, boxy):
    """Get the Shape and Color."""
    return board[boxx][boxy][0], board[boxx][boxy][1]


def draw_box_covers(display_surface, fps_clock, board, boxes, coverage):
    """Draw the box covers."""
    # Draw boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box
    for box in boxes:
        left, top = left_top_coords_of_box(box[0], box[1])
        pygame.draw.rect(display_surface, BGCOLOR,
                         (left, top, BOXSIZE, BOXSIZE))
        shape, color = get_shape_and_color(board, box[0], box[1])
        draw_icon(display_surface, shape, color, box[0], box[1])
        if coverage > 0:  # only draw the cover if there is an coverage
            pygame.draw.rect(display_surface, BOXCOLOR,
                             (left, top, coverage, BOXSIZE))
    pygame.display.update()
    fps_clock.tick(FPS)


def reveal_boxes_animation(display_surface, fps_clock, board, boxes_to_reveal):
    """Reveal Boxes Animation."""
    # Do the "box reveal" animation
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        draw_box_covers(display_surface, fps_clock, board, boxes_to_reveal,
                        coverage)


def cover_boxes_animation(display_surface, fps_clock, board, boxes_to_cover):
    """Do the box cover animation."""
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        draw_box_covers(display_surface, fps_clock, board, boxes_to_cover,
                        coverage)


def draw_board(display_surface, board, revealed):
    """Draw the Board."""
    # Draws all of the boxes in their covered or revealed state
    for boxx in range(GAME_COLS):
        for boxy in range(GAME_ROWS):
            left, top = left_top_coords_of_box(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered Box
                pygame.draw.rect(display_surface, BOXCOLOR,
                                 (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = get_shape_and_color(board, boxx, boxy)
                draw_icon(display_surface, shape, color, boxx, boxy)


def draw_highlight_box(display_surface, boxx, boxy):
    """Draw the Highlight box."""
    left, top = left_top_coords_of_box(boxx, boxy)
    pygame.draw.rect(display_surface, HIGHLIGHTCOLOR,
                     (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def start_game_animation(display_surface, fps_clock, board):
    """Randomly reveal the boxes 8 at a time."""
    covered_boxes = generate_revealed_boxes_data(False)
    boxes = []
    for boxx in range(GAME_COLS):
        for boxy in range(GAME_ROWS):
            boxes.append((boxx, boxy))
    random.shuffle(boxes)
    box_groups = split_into_groups_of(8, boxes)

    draw_board(display_surface, board, covered_boxes)
    for box_group in box_groups:
        reveal_boxes_animation(display_surface, fps_clock, board, box_group)
        cover_boxes_animation(display_surface, fps_clock, board, box_group)


def game_won_animation(display_surface, board):
    """flash the background color when the player has won."""
    covered_boxes = generate_revealed_boxes_data(board)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for _ in range(13):
        color1, color2 = color2, color1
        display_surface.fill(color1)
        draw_board(display_surface, board, covered_boxes)
        pygame.display.update()
        pygame.time.wait(300)


def has_won(revealed_boxes):
    """Returns True if all the boxes have been revealed, otherwise False"""
    for i in revealed_boxes:
        if False in i:
            return False
    return True


if __name__ == '__main__':
    main()
