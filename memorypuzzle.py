"""Memory Puzzle Game.

This is a small memory puzzle game, where blocks of similar images will be
shown and you will be asked to guess, which boxes contained similar images.

Original Author:
    Al Sweigart al@inventwithpython.com

Modifications:

Author:

    Senthil Kumaran <senthil@uthcode.com>
"""
from constants import (BOARDHEIGHT, BOARDWIDTH, BOXSIZE, FPS,  GAPSIZE,
                       REVEALSPEED, WINDOWHEIGHT, WINDOWWIDTH)
from colors import (BGCOLOR, RED, GREEN, YELLOW, BLUE, ORANGE, PURPLE, CYAN,
                    LIGHTBGCOLOR, BOXCOLOR, HIGHLIGHTCOLOR)
from shapes import (DONUT, SQUARE, DIAMOND, LINES, OVAL)

import random
import sys

import pygame
from pygame.constants import QUIT, KEYUP, K_ESCAPE, MOUSEMOTION, MOUSEBUTTONUP

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

FPSCLOCK = None
DISPLAYSURF = None

def main():
    """Run the Memory Puzzle Game."""
    assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, \
        "Board needs to have even number of boxes for pairs of matches."
    assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDHEIGHT * BOARDWIDTH, \
    "Board is too big for the number of shapes/colors defined."

    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mouse_xpos = 0  # used to store the x coordinate of the mouse event
    mouse_ypos = 0  # used to store the y coordinate of the mouse event
    pygame.display.set_caption("Memory Game")

    mainboard = get_randomized_board()
    revealed_boxes = generate_revealed_boxes_data(False)

    first_selection = None

    DISPLAYSURF.fill(BGCOLOR)
    start_game_animation(mainboard)

    while True:
        mouse_clicked = False
        DISPLAYSURF.fill(BGCOLOR)
        draw_board(mainboard, revealed_boxes)

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (
                            event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_xpos, mouse_ypos = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_xpos, mouse_ypos = event.pos
                mouse_clicked = True

        boxx, boxy = get_box_at_pixel(mouse_xpos, mouse_ypos)
        if boxx is not None and boxy is not None:
            # The mouse is currently over the box
            if not revealed_boxes[boxx][boxy]:
                draw_highlight_box(boxx, boxy)
            if not revealed_boxes[boxx][boxy] and mouse_clicked:
                reveal_boxes_animation(mainboard, [(boxx, boxy)])
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
                        cover_boxes_animation(mainboard, [
                            (first_selection[0], first_selection[1]),
                            (boxx, boxy)])
                        revealed_boxes[first_selection[0]][
                            first_selection[1]] = False
                        revealed_boxes[boxx][boxy] = False
                    elif has_won(revealed_boxes):  # check if all pairs found.
                        game_won_animation(mainboard)
                        pygame.time.wait(2000)

                        # Reset the board
                        mainboard = get_randomized_board()
                        revealed_boxes = generate_revealed_boxes_data(False)

                        # Show the fully unrevealed board for a second
                        draw_board(mainboard, revealed_boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation
                        start_game_animation(mainboard)
                    first_selection = None

        # Redraw the screen and wait for the clock tick
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_revealed_boxes_data(val):
    """Generate Revealed Boxes Data."""
    revealed_boxes = []
    for _ in range(BOARDWIDTH):
        revealed_boxes.append([val] * BOARDHEIGHT)
    return revealed_boxes


def get_randomized_board():
    """Get the Randomized Board."""
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    random.shuffle(icons)
    num_icons_used = int(BOARDHEIGHT * BOARDWIDTH / 2)
    icons = icons[:num_icons_used] * 2
    random.shuffle(icons)

    # Create a board data structure with randomly placed icons
    board = []
    for _ in range(BOARDWIDTH):
        column = []
        for _ in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
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
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = left_top_coords_of_box(boxx, boxy)
            box_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box_rect.collidepoint(mouse_xpos, mouse_ypos):
                return boxx, boxy
    return None, None


def draw_icon(shape, color, boxx, boxy):
    """Draw the game Icon."""
    quarter = int(BOXSIZE * 0.25)  # syntactic sugar
    half = int(BOXSIZE * 0.5)  # syntactic sugar
    left, top = left_top_coords_of_box(boxx, boxy)

    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half),
                           half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half),
                           quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(
            DISPLAYSURF, color,
            (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, (
            (left + half, top), (left + BOXSIZE - 1, top + half),
            (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i),
                             (left + i, top))
            pygame.draw.line(
                DISPLAYSURF, color, (left + i, top + BOXSIZE - 1),
                (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color,
                            (left, top + quarter, BOXSIZE, half))


def get_shape_and_color(board, boxx, boxy):
    """Get the Shape and Color."""
    return board[boxx][boxy][0], board[boxx][boxy][1]


def draw_box_covers(board, boxes, coverage):
    """Draw the box covers."""
    # Draw boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box
    for box in boxes:
        left, top = left_top_coords_of_box(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = get_shape_and_color(board, box[0], box[1])
        draw_icon(shape, color, box[0], box[1])
        if coverage > 0:  # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR,
                             (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def reveal_boxes_animation(board, boxes_to_reveal):
    """Reveal Boxes Animation."""
    # Do the "box reveal" animation
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        draw_box_covers(board, boxes_to_reveal, coverage)


def cover_boxes_animation(board, boxes_to_cover):
    """Do the box cover animation."""
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        draw_box_covers(board, boxes_to_cover, coverage)


def draw_board(board, revealed):
    """Draw the Board."""
    # Draws all of the boxes in their covered or revealed state
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = left_top_coords_of_box(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered Box
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR,
                                 (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = get_shape_and_color(board, boxx, boxy)
                draw_icon(shape, color, boxx, boxy)


def draw_highlight_box(boxx, boxy):
    """Draw the Highlight box."""
    left, top = left_top_coords_of_box(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR,
                     (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def start_game_animation(board):
    """Randomly reveal the boxes 8 at a time."""
    covered_boxes = generate_revealed_boxes_data(False)
    boxes = []
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            boxes.append((boxx, boxy))
    random.shuffle(boxes)
    box_groups = split_into_groups_of(8, boxes)

    draw_board(board, covered_boxes)
    for box_group in box_groups:
        reveal_boxes_animation(board, box_group)
        cover_boxes_animation(board, box_group)


def game_won_animation(board):
    """flash the background color when the player has won."""
    covered_boxes = generate_revealed_boxes_data(board)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for _ in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        draw_board(board, covered_boxes)
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
