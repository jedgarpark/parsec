#fancyLED Hues

import time
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import adafruit_fancyled.adafruit_fancyled as fancy


# enable external power pin
# provides power to the external components
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True

# external neopixels
num_pixels = 94
pixels = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, num_pixels)

color = fancy.CHSV(0.0, 1.0, 0.01)
packed = color.pack()
pixels.fill(packed)

# user settings
STEPS = 36  # smoothness  try 3, 6, 12, 360
CYCLE_TIME = 3.0  # duration to complete the hue cycle in seconds

step = 1.0 / STEPS
rate =  CYCLE_TIME / STEPS
my_hue = 0.0
my_sat = 1.0
my_val = 0.35


while True:

    while my_hue < 1.0:
        color = fancy.CHSV( my_hue, my_sat, my_val )
        packed = color.pack()
        pixels.fill(packed)
        my_hue += step
        time.sleep(rate)
        print(f"hue: {my_hue:1.3f}")
    time.sleep(1.0)

    while my_hue > 0.0:
        color = fancy.CHSV( my_hue, my_sat, my_val )
        packed = color.pack()
        pixels.fill(packed)
        my_hue -= step
        time.sleep(rate)
        print(f"hue: {my_hue:1.3f}")
    time.sleep(1.0)
