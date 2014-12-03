"""Constants used by the Memory Puzzle Game."""

GAME_ROWS = 10
GAME_COLS = 10

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

XMARGIN = int((WINDOWWIDTH - (GAME_COLS * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (GAME_ROWS * (BOXSIZE + GAPSIZE))) / 2)