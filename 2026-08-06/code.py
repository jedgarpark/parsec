# circuit python parsec -- Fruit Jam Library: Buttons
#
#
# adafruit_fruitjam helper library based on Portal Base
# - initializes the Fruit Jam hardware built-in peripherals
# provides single interface to access:
#   - buttons
#   - neopixels
#   - DAC audio
#   - headphone out & speaker out
#   - SD card
#   - HSTX/DVI display config
# -also handles internet access

import time
from adafruit_fruitjam.peripherals import Peripherals

fruitjam = Peripherals()

# Clear screen once at start, hide cursor for a cleaner redraw
print("\x1b[2J", end="")
print("\x1b[?25l", end="")


while True:
    # Move cursor to top-left, then print status, clearing to end of line
    print("\x1b[H", end="")
    print("\x1b[2K" + "Button 3: " + ("PRESSED" if fruitjam.button3 else "released"))
    print("\x1b[2K" + "Button 2: " + ("PRESSED" if fruitjam.button2 else "released"))
    print("\x1b[2K" + "Button 1: " + ("PRESSED" if fruitjam.button1 else "released"))

    time.sleep(0.05)
