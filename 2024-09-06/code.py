#STEMMA QT port hack to use test clips as switches

import time
import board
import digitalio
import neopixel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

pin1 = digitalio.DigitalInOut(board.SCL)
pin2 = digitalio.DigitalInOut(board.SDA)

pin1.pull = digitalio.Pull.DOWN
pin2.pull = digitalio.Pull.DOWN

print("pin1", pin1.value)
print("pin2", pin2.value, "\n")

last_pin1 = pin1.value
last_pin2 = pin2.value

while True:
    if pin1.value is not last_pin1:
        if pin1.value:  # pull down resistor, so value True when released
            print("pin1 (SCL) released, value:", pin1.value)
            pixel.fill(0x0)
        else:
            print("pin1 (SCL) pressed, value:", pin1.value)
            pixel.fill(0x221100)
        last_pin1 = not last_pin1

    if pin2.value is not last_pin2:
        if pin2.value:
            print("pin2 (SDA) released, value:", pin2.value)
            pixel.fill(0x0)
        else:
            print("pin2 (SDA) pressed, value:", pin2.value)
            pixel.fill(0x001122)
        last_pin2 = not last_pin2

    time.sleep(0.1)
