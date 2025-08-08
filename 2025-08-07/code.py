# Use a Wii Classic/NES Classic/SNES Classic controller in CircuitPython with the wiichuck library
import time
import board
from digitalio import DigitalInOut, Direction, Pull
import neopixel
from wiichuck.classic_controller import ClassicController

controller = ClassicController(board.STEMMA_I2C())

# on board neopixel
pix = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.4)
pix.fill(0x002222)

# external neopixels
num_pixels = 8
pixels = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, num_pixels, brightness=0.05)

# enable external power pin
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True

while True:
    # Get controller values
    _, buttons, dpad, _ = controller.values

    if buttons.A:
        pixels.fill(0xff0000)
        print("button A")
    if buttons.B:
        pixels.fill(0x00ff00)
        print("button B")
    if dpad.up:
        pixels.fill(0x0000ff)
        print("dpad up")
    if dpad.down:
        pixels.fill(0x880088)
        print("dpad down")
    if dpad.left:
        pixels.fill(0x888800)
        print("dpad left")
    if dpad.right:
        pixels.fill(0x008888)
        print("dpad right")
    if buttons.start:
        pixels.fill(0x220066)
        print("button start")
    if buttons.select:
        pixels.fill(0x006622)
        print("button select")

    time.sleep(0.2)
