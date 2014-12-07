"""Memory Puzzle Game.

This is a small memory puzzle game, where blocks of similar images will be
shown and you will be asked to guess, which boxes contained similar images.

Adapted from the original game written by Al Sweigart al@inventwithpython.com

@author: Senthil Kumaran <senthil@uthcode.com>
"""
import random
import sys

import pygame
from pygame.constants import K_ESCAPE, KEYUP, MOUSEBUTTONUP, MOUSEMOTION, QUIT

from colors import (
    BGCOLOR,
    BLUE,
    BOXCOLOR,
    CYAN,
    GREEN,
    HIGHLIGHTCOLOR,
    IVORY,
    LIGHTBGCOLOR,
    ORANGE,
    PURPLE,
    RED,
    YELLOW)
from constants import (
    BOXSIZE,
    EASY_GAME_COLS,
    EASY_GAME_ROWS,
    EASY_RECT,
    EASY_TEXT_POS,
    FPS,
    FONT_SIZE,
    GAPSIZE,
    HARD_GAME_COLS,
    HARD_GAME_ROWS,
    HARD_RECT,
    HARD_TEXT_POS,
    MEDIUM_GAME_COLS,
    MEDIUM_GAME_ROWS,
    MEDIUM_RECT,
    MEDIUM_TEXT_POS,
    REVEALSPEED,
    WINDOWHEIGHT,
    WINDOWWIDTH)
from shapes import (
    DIAMOND,
    DONUT,
    LINES,
    OVAL,
    SQUARE)


ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)


def left_top_coords_of_box(box, game_grid):
    """Top left coordinates of a box."""

    def get_xy_margins(grid):
        game_rows, game_cols = grid
        return (int((WINDOWWIDTH - (game_cols * (BOXSIZE + GAPSIZE))) / 2),
                int((WINDOWHEIGHT - (game_rows * (BOXSIZE + GAPSIZE))) / 2))

    xmargin, ymargin = get_xy_margins(game_grid)
    x_value, y_value = box
    left = xmargin + x_value * (BOXSIZE + GAPSIZE)
    top = ymargin + y_value * (BOXSIZE + GAPSIZE)
    return left, top


def draw_box_covers(display_surface, fps_clock, board, boxes, coverage,
                    game_grid):
    """Draw boxes being covered/revealed.

    boxes is a list of two-item lists, which have the x & y spot of the box.
    """
    for box in boxes:
        left, top = left_top_coords_of_box(box, game_grid)
        pygame.draw.rect(
            display_surface,
            BGCOLOR,
            (left, top, BOXSIZE, BOXSIZE))
        shape, color = get_shape_and_color(board, box)
        draw_icon(display_surface, shape, color, box, game_grid)
        if coverage > 0:  # only draw the cover if there is an coverage
            pygame.draw.rect(
                display_surface,
                BOXCOLOR,
                (left, top, coverage, BOXSIZE))
    pygame.display.update()
    fps_clock.tick(FPS)


def draw_icon(display_surface, shape, color, box, game_grid):
    """Draw icon of the piece."""
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)
    left, top = left_top_coords_of_box(box, game_grid)

    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(
            display_surface,
            color,
            (left + half, top + half),
            half - 5)
        pygame.draw.circle(
            display_surface,
            BGCOLOR,
            (left + half, top + half),
            quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(
            display_surface,
            color,
            (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(
            display_surface,
            color,
            ((left + half, top),
             (left + BOXSIZE - 1, top + half),
             (left + half, top + BOXSIZE - 1),
             (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(
                display_surface,
                color,
                (left, top + i),
                (left + i, top))
            pygame.draw.line(
                display_surface,
                color,
                (left + i, top + BOXSIZE - 1),
                (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(
            display_surface,
            color,
            (left, top + quarter, BOXSIZE, half))


def game_won(display_surface, board, game_grid):
    """Won the game.

    Flash the background color celebrating the players win."""
    covered_boxes = generate_revealed_boxes_data(board, game_grid)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    for _ in range(13):
        color1, color2 = color2, color1
        display_surface.fill(color1)
        draw_board(
            display_surface,
            board,
            covered_boxes,
            game_grid)
        pygame.display.update()
        pygame.time.wait(300)
    pygame.time.wait(2000)


def cover_boxes_animation(display_surface, fps_clock, board, boxes_to_cover,
                          game_grid):
    """Do the box cover animation."""
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        draw_box_covers(
            display_surface,
            fps_clock,
            board,
            boxes_to_cover,
            coverage,
            game_grid)


def get_shape_and_color(board, box):
    """Get the Shape and Color."""
    x_value, y_value = box
    return board[x_value][y_value][0], board[x_value][y_value][1]


def reveal_boxes_animation(display_surface, fps_clock, board, boxes_to_reveal,
                           game_grid):
    """Reveal Boxes Animation."""
    # Do the "box reveal" animation
    for coverage in range(BOXSIZE, -1, -REVEALSPEED):
        draw_box_covers(
            display_surface,
            fps_clock,
            board,
            boxes_to_reveal,
            coverage,
            game_grid)


def draw_highlight_box(display_surface, box, game_grid):
    """Draw the Highlight box."""
    left, top = left_top_coords_of_box(box, game_grid)
    pygame.draw.rect(
        display_surface,
        HIGHLIGHTCOLOR,
        (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10),
        4)


def get_box_relative_to_grid(mouse_pointer, game_grid):
    """Get the Box at a Pixel."""
    game_rows, game_cols = game_grid
    for boxx in range(game_cols):
        for boxy in range(game_rows):
            left, top = left_top_coords_of_box((boxx, boxy), game_grid)
            box_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box_rect.collidepoint(mouse_pointer):
                return boxx, boxy
    return None, None


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
    return mouse_clicked, (mouse_xpos, mouse_ypos)


def draw_board(display_surface, board, revealed, game_grid):
    """Draw the Board."""
    game_rows, game_cols = game_grid
    for x_value in range(game_cols):
        for y_value in range(game_rows):
            box = (x_value, y_value)
            left, top = left_top_coords_of_box(box, game_grid)
            if not revealed[x_value][y_value]:
                # Draw a covered Box
                pygame.draw.rect(
                    display_surface,
                    BOXCOLOR,
                    (left, top, BOXSIZE, BOXSIZE),
                    3)
            else:
                shape, color = get_shape_and_color(board, box)
                draw_icon(
                    display_surface,
                    shape,
                    color,
                    box,
                    game_grid)


def generate_revealed_boxes_data(val, game_grid):
    """Generate Revealed Boxes Data."""
    game_rows, game_cols = game_grid
    revealed_boxes = []
    for x_value in range(game_cols):
        column_values = []
        for y_value in range(game_rows):
            column_values.append(val)
        revealed_boxes.append(column_values)
    return revealed_boxes


def start_game_animation(display_surface, fps_clock, board, game_grid):
    """Randomly reveal the boxes 8 at a time."""

    game_rows, game_cols = game_grid

    def split_into_groups_of(group_size, the_list):
        """Split into Groups."""
        result = []
        for cut in range(0, len(the_list), group_size):
            result.append(the_list[cut:cut + group_size])
        return result

    covered_boxes = generate_revealed_boxes_data(False, game_grid)
    boxes = []
    for x_value in range(game_cols):
        for y_value in range(game_rows):
            boxes.append((x_value, y_value))
    random.shuffle(boxes)
    box_groups = split_into_groups_of(8, boxes)

    draw_board(display_surface, board, covered_boxes, game_grid)
    for box_group in box_groups:
        reveal_boxes_animation(
            display_surface,
            fps_clock,
            board,
            box_group,
            game_grid)
        cover_boxes_animation(
            display_surface,
            fps_clock,
            board,
            box_group,
            game_grid)


def display_welcome_screen(display_surface, fps_clock):
    font = pygame.font.Font(None, FONT_SIZE)

    easy_surf = font.render("Easy", True, IVORY)
    medium_surf = font.render("Medium", True, IVORY)
    hard_surf = font.render("Hard", True, IVORY)

    display_surface.fill(BGCOLOR)

    while True:
        mouse_clicked, mouse_pointer = get_mouse_click()

        pygame.draw.rect(display_surface, CYAN, EASY_RECT, 3)
        display_surface.fill(CYAN, EASY_RECT)
        display_surface.blit(easy_surf, EASY_TEXT_POS)

        pygame.draw.rect(display_surface, ORANGE, MEDIUM_RECT, 3)
        display_surface.fill(ORANGE, MEDIUM_RECT)
        display_surface.blit(medium_surf, MEDIUM_TEXT_POS)

        pygame.draw.rect(display_surface, PURPLE, HARD_RECT, 3)
        display_surface.fill(PURPLE, HARD_RECT)
        display_surface.blit(hard_surf, HARD_TEXT_POS)

        if mouse_clicked:
            display_surface.fill(BGCOLOR)
            if pygame.Rect(EASY_RECT).collidepoint(mouse_pointer):
                return EASY_GAME_ROWS, EASY_GAME_COLS
            elif pygame.Rect(MEDIUM_RECT).collidepoint(mouse_pointer):
                return MEDIUM_GAME_ROWS, MEDIUM_GAME_COLS
            elif pygame.Rect(HARD_RECT).collidepoint(mouse_pointer):
                return HARD_GAME_ROWS, HARD_GAME_COLS

        pygame.display.update()
        fps_clock.tick(FPS)


def game_loop(display_surface, fps_clock):
    """The main loop of the game."""
    first_selection = None
    game_started = False

    def player_has_won(revealed):
        """Game is won when all boxes are revealed, that is set to True."""
        return all([all(boxes) for boxes in revealed])

    def get_randomized_board(grid):
        """Get the Randomized Board.

        Gets the list of every possible shape in every possible color
        and then creates a board, a list of lists, with randomly placed icons.
        """
        game_rows, game_cols = grid
        icons = [(shape, color) for shape in ALLSHAPES for color in ALLCOLORS]
        random.shuffle(icons)
        num_icons_used = int(game_rows * game_cols / 2)
        icons = icons[:num_icons_used] * 2
        random.shuffle(icons)

        game_board = []
        for x_value in range(game_cols):
            column_values = []
            for y_value in range(game_rows):
                column_values.append(icons.pop(0))
            game_board.append(column_values)
        return game_board

    def is_box_revealed(revealed, selected_box):
        box_x, box_y = selected_box
        return revealed[box_x][box_y]

    def set_box_revealed(revealed, selected_box, status):
        box_x, box_y = selected_box
        revealed[box_x][box_y] = status
        return revealed

    while True:
        if not game_started:
            game_grid = display_welcome_screen(display_surface, fps_clock)
            board = get_randomized_board(game_grid)
            start_game_animation(display_surface, fps_clock, board, game_grid)
            revealed_boxes = generate_revealed_boxes_data(False, game_grid)
            game_started = True
        else:
            display_surface.fill(BGCOLOR)
            draw_board(display_surface, board, revealed_boxes, game_grid)
            mouse_clicked, mouse_pointer = get_mouse_click()
            box = get_box_relative_to_grid(mouse_pointer, game_grid)
            if None not in box:
                if not is_box_revealed(revealed_boxes, box):
                    # The mouse is currently over the box
                    draw_highlight_box(display_surface, box, game_grid)
                if not is_box_revealed(revealed_boxes, box) and mouse_clicked:
                    reveal_boxes_animation(
                        display_surface,
                        fps_clock,
                        board,
                        [box],
                        game_grid)
                    revealed_boxes = set_box_revealed(revealed_boxes, box, True)
                    if first_selection is None:
                        first_selection = box
                    else:
                        first_piece = get_shape_and_color(
                            board,
                            first_selection)
                        second_piece = get_shape_and_color(board, box)
                        if first_piece != second_piece:
                            # Re-cover up both selections
                            pygame.time.wait(1000)
                            cover_boxes_animation(
                                display_surface,
                                fps_clock,
                                board,
                                [first_selection, box],
                                game_grid)
                            revealed_boxes = set_box_revealed(
                                revealed_boxes,
                                first_selection,
                                False)
                            revealed_boxes = set_box_revealed(
                                revealed_boxes,
                                box,
                                False)
                        elif player_has_won(revealed_boxes):
                            game_won(display_surface, board, game_grid)
                            game_started = False
                        first_selection = None
        # Redraw the screen and wait for the clock tick
        pygame.display.update()
        fps_clock.tick(FPS)


def get_game_clock_display():
    """Initialize PyGame and return clock and display.

    Return frames per second clock and Display Surface of the PyGame.
    """
    pygame.init()
    pygame.display.set_caption("Memory Game")
    return (pygame.time.Clock(),
            pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)))


def main():
    fps_clock, display_surface = get_game_clock_display()
    game_loop(display_surface, fps_clock)


if __name__ == '__main__':
    main()
