# cpy parsec state toggle

import board
import keypad
import neopixel

# Define the display
display = board.DISPLAY

BLUE = 0x00ffff
PURPLE = 0xaa00bb

# neopixel setup
num_pixels = 12
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.25, auto_write=False)
pixels.fill(BLUE)
pixels.show()

# Define keypad
key_pins = (
            board.KEY1, board.KEY2, board.KEY3,
            board.KEY4, board.KEY5, board.KEY6,
            board.KEY7, board.KEY8, board.KEY9,
            board.KEY10, board.KEY11, board.KEY12
)
keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True)

leds_state = [True] * num_pixels

while True:
    event = keys.events.get()
    if event:
        key = event.key_number
        if event.pressed:
            if leds_state[key] == True:
                pixels[key] = (PURPLE)
                pixels.show()
                leds_state[key] = False
            else:
                pixels[key] = (BLUE)
                pixels.show()
                leds_state[key] = True
            print(' '.join([str(int(x)) for x in leds_state]))
