"""Constants used by the Memory Puzzle Game."""

GAME_ROWS = 10
GAME_COLS = 10

EASY_GAME_ROWS = 4
EASY_GAME_COLS = 5

MEDIUM_GAME_ROWS = 6
MEDIUM_GAME_COLS = 6

HARD_GAME_ROWS = 7
HARD_GAME_COLS = 10

# size of box height and width in pixels
BOXSIZE = 40

# Frames per second, the general speed of the program.
FPS = 20

# size of gap between boxes in pixels
GAPSIZE = 10

# speed boxes sliding reveals and covers
REVEALSPEED = 8

# size of windows height in pixels
WINDOWHEIGHT = 480

# size of window's width in pixels
WINDOWWIDTH = 640

# welcome screen coordinates

FONT_SIZE = 60

LEVEL_BOX_WIDTH = WINDOWWIDTH / 2
LEVEL_BOX_HEIGHT = WINDOWHEIGHT / 6
LEVEL_BOX_LEFT = WINDOWWIDTH / 4
LEVEL_BOX_TOP = WINDOWHEIGHT / 4

EASY_RECT = ((LEVEL_BOX_LEFT, LEVEL_BOX_TOP),
             (LEVEL_BOX_WIDTH, LEVEL_BOX_HEIGHT))
MEDIUM_RECT = ((LEVEL_BOX_LEFT, LEVEL_BOX_TOP + LEVEL_BOX_HEIGHT),
               (LEVEL_BOX_WIDTH, LEVEL_BOX_HEIGHT))
HARD_RECT = ((LEVEL_BOX_LEFT, LEVEL_BOX_TOP + LEVEL_BOX_HEIGHT * 2),
             (LEVEL_BOX_WIDTH, LEVEL_BOX_HEIGHT))

EASY_TEXT_POS = (LEVEL_BOX_LEFT + LEVEL_BOX_LEFT / 2,
                 LEVEL_BOX_TOP + LEVEL_BOX_TOP / 4)
MEDIUM_TEXT_POS = (LEVEL_BOX_LEFT + LEVEL_BOX_LEFT / 2,
                   LEVEL_BOX_TOP + LEVEL_BOX_TOP / 4 + LEVEL_BOX_HEIGHT)
HARD_TEXT_POS = (LEVEL_BOX_LEFT + LEVEL_BOX_LEFT / 2,
                 LEVEL_BOX_TOP + LEVEL_BOX_TOP / 4 + LEVEL_BOX_HEIGHT * 2)

# Game wait times

GAME_END_WAIT = 2000

GAME_WON_FLASH_WAIT = 300

PIECE_CLOSE_WAIT = 1000
