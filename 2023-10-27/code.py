# Print debug for CircuitPython Parsec
# demo for PyBadge

import time
import board
from analogio import AnalogIn
import keypad
import neopixel

DEBUG = False

leds = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness = 0.1)
leds.fill(0x330000)

k = keypad.ShiftRegisterKeys(
    clock=board.BUTTON_CLOCK,
    data=board.BUTTON_OUT,
    latch=board.BUTTON_LATCH,
    key_count=8,
    value_when_pressed=True,
)

key_names = ("B", "A", "R Shoulder", "L Shoulder", "RIGHT", "DOWN", "UP", "LEFT")

light_sensor = AnalogIn(board.LIGHT)
last_light = 0

def printd(line):
    if DEBUG:
        print(line)


while True:
    event = k.events.get()
    if event:
        if event.pressed:
            leds[event.key_number%5]=0x0
            print("  ", key_names[event.key_number], "pressed")
        if event.released:
            leds[event.key_number%5]=0x330000
            printd(f"{key_names[event.key_number]} released")

    light = int(light_sensor.value//2048)
    if last_light is not light:
        leds.brightness = light/5
        printd(f"Light value: {light}")
        last_light = light
