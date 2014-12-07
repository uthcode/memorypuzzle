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
    WINDOWWIDTH, GAME_WON_FLASH_WAIT, GAME_END_WAIT, PIECE_CLOSE_WAIT,
    QUARTER_BOXSIZE, HALF_BOXSIZE)
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
        """Calculate the x, y margins of the grid."""
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
    left, top = left_top_coords_of_box(box, game_grid)

    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(
            display_surface,
            color,
            (left + HALF_BOXSIZE, top + HALF_BOXSIZE),
            HALF_BOXSIZE - 5)
        pygame.draw.circle(
            display_surface,
            BGCOLOR,
            (left + HALF_BOXSIZE, top + HALF_BOXSIZE),
            QUARTER_BOXSIZE - 5)
    elif shape == SQUARE:
        pygame.draw.rect(
            display_surface,
            color,
            (left + QUARTER_BOXSIZE,
             top + QUARTER_BOXSIZE,
             BOXSIZE - HALF_BOXSIZE,
             BOXSIZE - HALF_BOXSIZE))
    elif shape == DIAMOND:
        pygame.draw.polygon(
            display_surface,
            color,
            ((left + HALF_BOXSIZE, top),
             (left + BOXSIZE - 1, top + HALF_BOXSIZE),
             (left + HALF_BOXSIZE, top + BOXSIZE - 1),
             (left, top + HALF_BOXSIZE)))
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
            (left, top + QUARTER_BOXSIZE, BOXSIZE, HALF_BOXSIZE))


def game_won(display_surface, board, game_grid):
    """Game is won by the place.

    Flash the background color celebrating the players win."""
    covered_boxes = generate_revealed_boxes_data(True, game_grid)
    flash_colors = [LIGHTBGCOLOR, BGCOLOR]
    for count in range(10):
        display_surface.fill(flash_colors[count % 2])
        draw_board(display_surface, board, covered_boxes, game_grid)
        pygame.display.update()
        pygame.time.wait(GAME_WON_FLASH_WAIT)
    pygame.time.wait(GAME_END_WAIT)


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
    """Do the box reveal animation."""
    for coverage in range(BOXSIZE, -1, -REVEALSPEED):
        draw_box_covers(
            display_surface,
            fps_clock,
            board,
            boxes_to_reveal,
            coverage,
            game_grid)


def draw_highlight_box(display_surface, box, game_grid):
    """Draw the highlight box."""
    left, top = left_top_coords_of_box(box, game_grid)
    pygame.draw.rect(
        display_surface,
        HIGHLIGHTCOLOR,
        (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10),
        4)


def get_mouse_click():
    """Gets the mouse click position.

    Returns a tuple of if a mouse was clocked and the x, y coordinates."""
    mouse_clicked = False
    mouse_xpos = 0
    mouse_ypos = 0
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
    revealed_boxes = [[val for _ in range(game_rows)] for _ in range(game_cols)]
    return revealed_boxes


def start_game_animation(display_surface, fps_clock, board, game_grid):
    """Starts the Game opening animation.

    Randomly reveals the boxes 8 box at a time.
    """
    game_rows, game_cols = game_grid

    def split_into_groups_of(group_size, the_list):
        """Splits the list into the given group size."""
        result = []
        for cut in range(0, len(the_list), group_size):
            result.append(the_list[cut:cut + group_size])
        return result

    covered_boxes = generate_revealed_boxes_data(False, game_grid)
    boxes = [(x_value, y_value)
             for y_value in range(game_rows)
             for x_value in range(game_cols)]
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


def get_game_level(display_surface, fps_clock):
    """Get the game level desired by the user."""

    def draw_welcome_screen():
        """Display the welcome and the three game levels."""
        font = pygame.font.Font(None, FONT_SIZE)

        easy_surf = font.render("Easy", True, IVORY)
        medium_surf = font.render("Medium", True, IVORY)
        hard_surf = font.render("Hard", True, IVORY)
        pygame.draw.rect(display_surface, CYAN, EASY_RECT, 3)

        display_surface.fill(CYAN, EASY_RECT)
        display_surface.blit(easy_surf, EASY_TEXT_POS)

        pygame.draw.rect(display_surface, ORANGE, MEDIUM_RECT, 3)
        display_surface.fill(ORANGE, MEDIUM_RECT)
        display_surface.blit(medium_surf, MEDIUM_TEXT_POS)

        pygame.draw.rect(display_surface, PURPLE, HARD_RECT, 3)
        display_surface.fill(PURPLE, HARD_RECT)
        display_surface.blit(hard_surf, HARD_TEXT_POS)

    while True:
        mouse_clicked, mouse_pointer = get_mouse_click()
        draw_welcome_screen()

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
    """Game loop encodes the logic of the game.

    During the game starts, prompts the player to choose the level and
    determines the game board size based on the level chosen. If two selections
    chosen by user are same, the boxes are left open, else they are closed.
    When all the chosen selections are open,  the game is won by the user and
    the game is reset.
    """

    def player_has_won(revealed):
        """Game is won when all boxes are revealed."""
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

        game_board = [[icons.pop(0) for _ in range(game_rows)]
                      for _ in range(game_cols)]
        return game_board

    def get_box_under_mouse(pointer, grid):
        """Get the box at a pixel."""
        game_rows, game_cols = grid
        mouse_over = False
        for boxx in range(game_cols):
            for boxy in range(game_rows):
                left, top = left_top_coords_of_box((boxx, boxy), grid)
                box_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                if box_rect.collidepoint(pointer):
                    mouse_over = True
                    return mouse_over, (boxx, boxy)
        return mouse_over, (None, None)

    def is_box_revealed(revealed, selected_box):
        """Returns the status of the box."""
        box_x, box_y = selected_box
        return revealed[box_x][box_y]

    def set_box_revealed(revealed, selected_box, status):
        """Sets the revealed status of the box."""
        box_x, box_y = selected_box
        revealed[box_x][box_y] = status
        return revealed

    game_started = False
    first_selection = None

    while True:
        display_surface.fill(BGCOLOR)
        if not game_started:
            game_grid = get_game_level(display_surface, fps_clock)
            board = get_randomized_board(game_grid)
            print board
            start_game_animation(display_surface, fps_clock, board, game_grid)
            revealed_boxes = generate_revealed_boxes_data(False, game_grid)
            game_started = True
        else:
            draw_board(display_surface, board, revealed_boxes, game_grid)
            mouse_clicked, mouse_pointer = get_mouse_click()
            mouse_over_box, box = get_box_under_mouse(mouse_pointer, game_grid)
            if mouse_over_box:
                if not is_box_revealed(revealed_boxes, box):
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
                            pygame.time.wait(PIECE_CLOSE_WAIT)
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

        pygame.display.update()
        fps_clock.tick(FPS)


def get_game_clock_display():
    """Initialize pygame and return clock and display.

    Return frames per second clock and Display Surface of the pygame.
    """
    pygame.init()
    pygame.display.set_caption("Memory Game")
    return (pygame.time.Clock(),
            pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)))


def main():
    """Memory puzzle game.

    Gets the clock and display surface and hands it over the game loop.
    """
    fps_clock, display_surface = get_game_clock_display()
    game_loop(display_surface, fps_clock)


if __name__ == '__main__':
    main()
