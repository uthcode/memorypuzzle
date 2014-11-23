"""Constants used by the Memory Puzzle Game."""

# number of rows of icons
BOARDHEIGHT = 7

# number of columns of icons
BOARDWIDTH = 10

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

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)