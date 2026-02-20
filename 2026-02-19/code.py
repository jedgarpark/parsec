# Manual Wordle score canvas for NeoTrellis 8x8

import time
import board
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis

i2c = busio.I2C(board.SCL, board.SDA)

# create the trellis
trelli = [
     [NeoTrellis(i2c, False, addr=0x2E), NeoTrellis(i2c, False, addr=0x2F)],
     [NeoTrellis(i2c, False, addr=0x30), NeoTrellis(i2c, False, addr=0x31)]
]
trellis = MultiTrellis(trelli)

# Set the brightness value (0.0 to 1.0)
trellis.brightness = 0.4

# Color definitions
BLACK = (3, 5, 4)              # For "off" state in wordle grid
YELLOW = (255, 150, 0)         # Yellow squares
GREEN = (0, 255, 0)            # Green squares
CANVAS = (0, 0, 0)             # Canvas background

# Wordle grid is 5 columns x 6 rows, set inside the 8x8 grid
WORDLE_START_X = 0  # Columns 1-5
WORDLE_START_Y = 0  # Rows 1-6
WORDLE_WIDTH = 5
WORDLE_HEIGHT = 6

# Track the state of each cell in the 5x6 grid in an array
# 0 = black, 1 = yellow, 2 = green
wordle_grid = [[0 for _ in range(WORDLE_WIDTH)] for _ in range(WORDLE_HEIGHT)]

# def xy_to_pos(x, y):  # convert from 2D xy coordinates to position number 0-63
#     return x + (y * 8)

def pos_to_xy(pos):  # convert from position number to 2D xy coord
    return (pos % 8, pos // 8)

def is_in_wordle_grid(x, y):
    """Check if x,y is within the 5x6 Wordle grid"""
    return (WORDLE_START_X <= x < WORDLE_START_X + WORDLE_WIDTH and
            WORDLE_START_Y <= y < WORDLE_START_Y + WORDLE_HEIGHT)

def get_color_for_state(state):
    """Convert state number to color"""
    if state == 0:
        return BLACK
    elif state == 1:
        return YELLOW
    elif state == 2:
        return GREEN

def initialize_display():
    """Set up the initial display"""
    for y in range(8):
        for x in range(8):
            if is_in_wordle_grid(x, y):
                # Wordle grid starts as black (off)
                trellis.color(x, y, BLACK)
            else:
                # Surrounding canvas
                trellis.color(x, y, CANVAS)

def handle_button(x, y, edge):
    global wordle_grid

    if edge == NeoTrellis.EDGE_RISING:
        # Only respond to buttons in the Wordle grid
        if is_in_wordle_grid(x, y):
            # Convert to grid coordinates
            grid_x = x - WORDLE_START_X
            grid_y = y - WORDLE_START_Y

            # Cycle through states: 0 (black) -> 1 (yellow) -> 2 (green) -> 0
            wordle_grid[grid_y][grid_x] = (wordle_grid[grid_y][grid_x] + 1) % 3  # wrap around

            # Update the LED
            new_color = get_color_for_state(wordle_grid[grid_y][grid_x])
            trellis.color(x, y, new_color)

# Setup all buttons
for i in range(64):
    xy_pos = pos_to_xy(i)
    trellis.activate_key(xy_pos[0], xy_pos[1], NeoTrellis.EDGE_RISING)
    trellis.set_callback(xy_pos[0], xy_pos[1], handle_button)

# Initialize the display
initialize_display()
print("Wordle Pixel Art Canvas Ready!")
print("Press buttons in the 5x6 grid to cycle: Black -> Yellow -> Green -> Black")

while True:
    trellis.sync()
    time.sleep(0.02)
