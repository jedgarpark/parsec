# cpy parsec
# keypad events -- pressed & released
# for Adafruit MacroPad
import board
import displayio
from adafruit_display_text import label
import terminalio
import keypad
import neopixel

# Define the display
display = board.DISPLAY

# neopixel setup
num_pixels = 12  # Change this according to your setup
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.25, auto_write=False)
pixels.fill(0x0000ff)  # Turn off all NeoPixels
pixels.show()

# Create display group
group = displayio.Group()
text = label.Label(terminalio.FONT, text="__", color=0xFFFFFF)
text.x = 84
text.y = 42
text.scale = 4
group.append(text)
display.root_group=group

# Define keypad
key_pins = (
            board.KEY1, board.KEY2, board.KEY3,
            board.KEY4, board.KEY5, board.KEY6,
            board.KEY7, board.KEY8, board.KEY9,
            board.KEY10, board.KEY11, board.KEY12
)
keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True)


while True:
    event = keys.events.get()
    if event:
        # # simple event check
        # text.text = str(event.key_number)
        # pixels[event.key_number] = (0xff0000)
        # pixels.show()

        # press vs release event check
        if event.pressed:
            text.text = str(event.key_number)
            pixels[event.key_number] = (0xff0000)
            pixels.show()

        if event.released:
            text.text = "__"
            pixels[event.key_number] = (0x000ff)
            pixels.show()
