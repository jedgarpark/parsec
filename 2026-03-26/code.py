# SPDX-FileCopyrightText: 2026 JG for Cedar Grove Maker Studios & John Park for Adafruit
# SPDX-License-Identifier: MIT
"""
modulo_example/code.py

Examples of using the modulo numeric operator for a cyclic function,
eliminating the need for complex if expressions.

The modulo operation returns the remainder of a division, as in x mod y. In
this example, it replaces if statements to cycle through a NeoPixel ring array,
lighting pixels before and after a primary pixel.

"""

import time
import board
import neopixel
import random
from digitalio import DigitalInOut, Direction, Pull

PIXEL_COUNT = 16  # Pixels
SPEED = 30  # RPM
PAUSE = 0.0

delay = 60 / SPEED / PIXEL_COUNT


class Color:
    # Some pure RGBW colors
    RED = (0xFF, 0x00, 0x00, 0x00)
    GRN = (0x00, 0xFF, 0x00, 0x00)
    BLU = (0x00, 0x00, 0xFF, 0x00)
    BLK = (0x00, 0x00, 0x00, 0x00)

# enable external power pin on Prop-Maker RP2040
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True

# Define NeoPixel ring; set startup brightness
pixel = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, PIXEL_COUNT, pixel_order=neopixel.GRBW,
                          auto_write=True)
pixel.brightness = 0.1  # Set ring brightness
pixel.fill(Color.BLK)  # Clear NeoPixel ring

pixel[0] = Color.GRN
time.sleep(PAUSE*2)
pixel.fill(Color.BLK)  # Clear NeoPixel ring



# # Use IF expressions
# while True:
#     for i in range (PIXEL_COUNT):
#         # Blank out trailing pixel
#         if i - 2 < 0:
#             pixel[i - 2 + PIXEL_COUNT] = Color.BLK
#             time.sleep(PAUSE)
#         else:
#             pixel[i - 2] = Color.BLK
#             time.sleep(PAUSE)

#         # Light up primary pixel
#         pixel[i] = Color.GRN
#         time.sleep(PAUSE)

#         # Light up adjacent pixels
#         if i - 1 < 0:
#             pixel[i - 1 + PIXEL_COUNT] = Color.RED
#             time.sleep(PAUSE)
#         else:
#             pixel[i - 1] = Color.RED
#             time.sleep(PAUSE)

#         if i + 1 >= PIXEL_COUNT:
#             pixel[i + 1 - PIXEL_COUNT] = Color.BLU
#             time.sleep(PAUSE)
#         else:
#             pixel[i + 1] = Color.BLU
#             time.sleep(PAUSE)

#         time.sleep(delay)



# # Use the MODULO numeric operator (%)
while True:
    for i in range(PIXEL_COUNT):
        # Blank out trailing pixel
        pixel[(i - 2) % PIXEL_COUNT] = Color.BLK
        time.sleep(PAUSE)

        # Light up primary pixel
        pixel[i] = Color.GRN
        time.sleep(PAUSE)

        # Light up adjacent pixels
        pixel[(i -1) % PIXEL_COUNT] = Color.RED
        time.sleep(PAUSE)
        pixel[(i +1) % PIXEL_COUNT] = Color.BLU

        time.sleep(PAUSE)
        time.sleep(delay)
