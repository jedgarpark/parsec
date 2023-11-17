# NVM non-volatile memory example on MacroPad

import board
import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import terminalio
import keypad
import neopixel
from microcontroller import nvm


# Define the display
display = board.DISPLAY

# Load the stored number from NVM
stored_number = nvm[0]

# Define the number of NeoPixels and their pin
num_pixels = 12  # Change this according to your setup
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.25, auto_write=False)
pixels.fill((0, 0, 0))  # Turn off all NeoPixels
if stored_number < 12:
    pixels[stored_number] = (0xff0000)  # Turn on the selected NeoPixel (green)
pixels.show()

# Create display group
group = displayio.Group()
# Create background rectangle
bg_rect = Rect(0, 0, display.width, display.height, fill=0xFFFFFF)
group.append(bg_rect)
# Set the font for the text label
font = terminalio.FONT
# Create text label to display the number
text = label.Label(font, text=str(stored_number), color=0x000000)
text.x = display.width // 2
text.y = display.height // 2
text.anchor_point = (0.5, 0.5)
text.scale = 4
group.append(text)
# Show the display group
display.show(group)

# Define keypad
key_pins = (board.KEY1, board.KEY2, board.KEY3, board.KEY4, board.KEY5, board.KEY6,
            board.KEY7, board.KEY8, board.KEY9, board.KEY10, board.KEY11, board.KEY12)
keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True)


while True:
    event = keys.events.get()
    if event:
        if event.pressed:
            stored_number = event.key_number
            text.text = str(stored_number)
            pixels.fill((0, 0, 0))  # Turn off all NeoPixels
            pixels[stored_number] = (0xff0000)  # Turn on the selected NeoPixel (green)
            pixels.show()

        # Save the number to NVM
        nvm[0] = stored_number
