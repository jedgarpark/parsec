# seesaw button bitmask
# how seesaw uses a bitmask for efficient button handling
#
import time
import board
from micropython import const
from adafruit_seesaw.seesaw import Seesaw

# GPIO pins on seesaw chip for each button
BUTTON_X = const(6)
BUTTON_Y = const(2)
BUTTON_A = const(5)
BUTTON_B = const(1)
BUTTON_SELECT = const(0)
BUTTON_START = const(16)

# create button bitmask where each bit corresponds to the GPIO pins defined above
button_mask = const(
    (1 << BUTTON_X)
    | (1 << BUTTON_Y)
    | (1 << BUTTON_A)
    | (1 << BUTTON_B)
    | (1 << BUTTON_SELECT)
    | (1 << BUTTON_START)
)

# Print the button_mask in both decimal and binary format
print("\nbutton_mask =", button_mask, "(decimal),", bin(button_mask), "(binary)")

i2c_bus = board.STEMMA_I2C()  # The built-in STEMMA QT connector on the microcontroller
seesaw = Seesaw(i2c_bus, addr=0x50)
seesaw.pin_mode_bulk(button_mask, seesaw.INPUT_PULLUP)

last_buttons = None  # Initialize to None to force first display

# Function to create fixed-width binary string
def format_binary(value, width=20):
    binary = bin(value)[2:]  # Remove '0b' prefix
    padding = '0' * (width - len(binary))  # Create padding
    return '0b' + padding + binary  # Add padding and prefix

print("\nBinary button bitmask operation\n\n")

while True:
    # read the pins and return the button_mask integer
    buttons = seesaw.digital_read_bulk(button_mask)

    # Only update display when button states change
    if buttons != last_buttons:
        # Create button display string
        x_display = "X" if not buttons & (1 << BUTTON_X) else "x"
        y_display = "Y" if not buttons & (1 << BUTTON_Y) else "y"
        a_display = "A" if not buttons & (1 << BUTTON_A) else "a"
        b_display = "B" if not buttons & (1 << BUTTON_B) else "b"
        select_display = "SELECT" if not buttons & (1 << BUTTON_SELECT) else "select"
        start_display = "START" if not buttons & (1 << BUTTON_START) else "start"

        # Create a fixed-width binary string
        binary_str = format_binary(buttons)

        # Print the fixed-width binary mask followed by the button display
        print(f"Buttons: {binary_str} {x_display} {y_display} {a_display} {b_display} {select_display} {start_display}        ", end="\r")

        last_buttons = buttons

    time.sleep(0.01)
