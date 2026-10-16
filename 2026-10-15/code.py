# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
# QT Py M0: the STEMMA QT port used as plain GPIO

import time
import board
import digitalio

led = digitalio.DigitalInOut(board.SDA)      # blue wire
led.switch_to_output()

button = digitalio.DigitalInOut(board.SCL)   # yellow wire
button.switch_to_input(pull=digitalio.Pull.UP)

last = None

while True:
    pressed = not button.value
    led.value = pressed

    if pressed != last:
        print("pressed" if pressed else "released")
        last = pressed

    time.sleep(0.01)


## find alias names
# import board
# import microcontroller

# for name in dir(microcontroller.pin):
#     pin = getattr(microcontroller.pin, name)
#     if isinstance(pin, microcontroller.Pin):
#         aliases = [a for a in dir(board) if getattr(board, a) is pin]
#         if aliases:
#             print(name, "->", " ".join(aliases))
