import board
from digitalio import DigitalInOut, Direction, Pull
import neopixel
from adafruit_led_animation.animation.rainbow import Rainbow

# # on board neopixel
# pix = neopixel.NeoPixel(board.NEOPIXEL, 1)
# pix.brightness = 0.1
# rainbow = Rainbow(pix, speed=0.05, period=2)


# external neopixels
num_pixels = 8
pixels = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, num_pixels)
pixels.brightness = 0.1
rainbow = Rainbow(pixels, speed=0.05, period=2)

enable external power pin

external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True


while True:
    rainbow.animate()
