# Neotrellis fill-between buttons
# if two buttons are pressed nearly-simultaneously
# fill the buttons between them with the first color
#
#
import time
import board
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis

num_switches = 64
# Track currently pressed buttons: list of (x, y, timestamp)
pressed_buttons = []
# Track button states: True = bright, False = dim
button_states = [False] * 64

i2c = busio.I2C(board.SCL, board.SDA)

# create the trellises
trelli = [  # adjust these to match your jumper settings if needed
     [NeoTrellis(i2c, False, addr=0x2E), NeoTrellis(i2c, False, addr=0x2F)],
     [NeoTrellis(i2c, False, addr=0x30), NeoTrellis(i2c, False, addr=0x31)]
]
trellis = MultiTrellis(trelli)

# Set the brightness value (0 to 1.0)
trellis.brightness = 0.3

# some color definitions
OFF = (0, 0, 0)             # 0
RED = (255, 0, 0)           # 1
YELLOW = (255, 150, 0)      # 2
GREEN = (0, 255, 0)         # 3
CYAN = (0, 255, 255)        # 4
BLUE = (0, 0, 255)          # 5
PURPLE = (180, 0, 255)      # 6
WHITE = (100, 100, 100)     # 7
CC_WHITE = (50, 100, 110)   # 8

colors = [OFF, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE, CC_WHITE]

# Dim versions of each color (about 10% brightness)
dim_colors = [
    (0, 0, 0),        # 0 - OFF (stays off)
    (25, 0, 0),       # 1 - DIM RED
    (25, 15, 0),      # 2 - DIM YELLOW
    (0, 25, 0),       # 3 - DIM GREEN
    (0, 25, 25),      # 4 - DIM CYAN
    (0, 0, 25),       # 5 - DIM BLUE
    (18, 0, 25),      # 6 - DIM PURPLE
    (10, 10, 10),     # 7 - DIM WHITE
    (5, 10, 11)       # 8 - DIM CC_WHITE
]

color_table = [  # color assignments per button
  1, 1, 1, 1, 5, 5, 5, 5,
  1, 1, 1, 1, 5, 5, 5, 5,
  1, 1, 1, 1, 5, 5, 5, 5,
  1, 1, 1, 1, 5, 5, 5, 5,
  3, 3, 3, 3, 2, 2, 2, 2,
  3, 3, 3, 3, 2, 2, 2, 2,
  3, 3, 3, 3, 2, 2, 2, 2,
  3, 3, 3, 3, 2, 2, 2, 2
]


# convert an x,y (0-7,0-7) to 0-63 to grab from color_table
def xy_to_pos(x,y):
    return x+(y*8)

# convert 0-63 to x,y
def pos_to_xy(pos):
    return (pos%8, pos//8)

def playback_led_colors():
    """Set all LEDs to their bright color at startup"""
    for i in range(num_switches):
        xy_pos = pos_to_xy(i)
        trellis.color(xy_pos[0], xy_pos[1], colors[color_table[i]])
    time.sleep(0.5)
    ''' then dim them '''
    for i in range(num_switches):
        xy_pos = pos_to_xy(i)
        trellis.color(xy_pos[0], xy_pos[1], dim_colors[color_table[i]])

def fill_between(x1, y1, x2, y2, color, is_bright):
    """Fill LEDs between two points if they share row or column"""
    # Same row
    if y1 == y2:
        start_x = min(x1, x2)  # figure out which is left and which is right
        end_x = max(x1, x2)
        for x in range(start_x, end_x + 1):
            pos = xy_to_pos(x, y1)
            trellis.color(x, y1, color)
            button_states[pos] = is_bright
    # Same column
    elif x1 == x2:
        start_y = min(y1, y2)
        end_y = max(y1, y2)
        for y in range(start_y, end_y + 1):
            pos = xy_to_pos(x1, y)
            trellis.color(x1, y, color)
            button_states[pos] = is_bright

# callback when buttons are pressed
def handle_button(x, y, edge):
    global pressed_buttons, button_states
    pos = xy_to_pos(x, y)

    if edge == NeoTrellis.EDGE_RISING:
        # Add to pressed buttons with timestamp
        pressed_buttons.append((x, y, time.monotonic()))

        # Check if we have 2 buttons pressed
        if len(pressed_buttons) >= 2:
            # Get the two most recent presses
            x1, y1, t1 = pressed_buttons[-2]
            x2, y2, t2 = pressed_buttons[-1]

            # Check if pressed within 0.n seconds of each other (simultaneous)
            if abs(t2 - t1) < 0.2:
                # Check if same row or column
                if x1 == x2 or y1 == y2:
                    # Use the color of the FIRST button pressed
                    first_pos = xy_to_pos(x1, y1)
                    fill_color = colors[color_table[first_pos]]
                    # Set all buttons in the range to bright
                    fill_between(x1, y1, x2, y2, fill_color, True)
                    return

        # Toggle behavior - flip current state
        button_states[pos] = not button_states[pos]

        if button_states[pos]:
            # Toggle to bright
            trellis.color(x, y, colors[color_table[pos]])
        else:
            # Toggle to dim
            trellis.color(x, y, dim_colors[color_table[pos]])

    elif edge == NeoTrellis.EDGE_FALLING:
        # Remove from pressed buttons
        pressed_buttons = [(px, py, pt) for px, py, pt in pressed_buttons if not (px == x and py == y)]
        # Don't change color on release - state persists

playback_led_colors()

for i in range(num_switches):
    xy_pos = pos_to_xy(i)
    # activate rising edge events on all keys
    trellis.activate_key(xy_pos[0], xy_pos[1], NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(xy_pos[0], xy_pos[1], NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the callback
    trellis.set_callback(xy_pos[0], xy_pos[1], handle_button)
    time.sleep(0.02)

while True:
    # call the sync function call any triggered callbacks
    trellis.sync()
    time.sleep(0.02)
