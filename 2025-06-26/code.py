# SPDX-FileCopyrightText: 2025 john park for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
how to scale a displayio object with .scale property
"""
import time
import board
import displayio
import math
import terminalio
from adafruit_display_text import label
from i2cdisplaybus import I2CDisplayBus
import adafruit_displayio_ssd1306

displayio.release_displays()
oled_reset = board.D9
i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = I2CDisplayBus(i2c, device_address=0x3C, reset=oled_reset)

WIDTH = 128
HEIGHT = 32

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

screen = displayio.Group()
display.root_group = screen

# Draw a label
text_x = 28
text_y = 16
text = ":)"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=text_x, y=text_y)
screen.append(text_area)

speed = 0.03

text_area.scale = 1

while True:
    # Scale up, doing full sine cycles at each scale
    for scale in range(1, 6):
        text_area.scale = scale
        start_time = time.monotonic()
        # Do a complete sine cycle (adjust duration as needed)
        while time.monotonic() - start_time < 2.0:  # 2 seconds per scale level
            text_area.x = int(64 + 30*math.sin(time.monotonic()*5))
            text_area.y = int(16 + 8*math.sin(time.monotonic()*3))
            time.sleep(speed)

    # Scale down, doing full sine cycles at each scale
    for scale in range(6, 0, -1):
        text_area.scale = scale
        start_time = time.monotonic()
        # Do a complete sine cycle
        while time.monotonic() - start_time < 2.0:  # 2 seconds per scale level
            text_area.x = int(64 + 30*math.sin(time.monotonic()*5))
            text_area.y = int(16 + 8*math.sin(time.monotonic()*3))
            time.sleep(speed)
