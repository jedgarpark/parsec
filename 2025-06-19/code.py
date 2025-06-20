# SPDX-FileCopyrightText: 2025 john park for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
how to move a displayio object with .x and .y properties
"""
import time
import board
import displayio


import terminalio
from adafruit_display_text import label
from i2cdisplaybus import I2CDisplayBus

import adafruit_displayio_ssd1306

displayio.release_displays()

oled_reset = board.D9

# Use for I2C
# i2c = board.I2C()  # uses board.SCL and board.SDA
i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = I2CDisplayBus(i2c, device_address=0x3C, reset=oled_reset)

WIDTH = 128
HEIGHT = 32
BORDER = 1

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
screen = displayio.Group()
display.root_group = screen

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
screen.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
screen.append(inner_sprite)

# Draw a label
text_x = 28
text_y = 16
text = "o"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=text_x, y=text_y)
screen.append(text_area)

speed = 0.01

while True:
    for y in range(8, 24, 4):  # range and step size
        text_area.y = y

        # Move right from 2 to 123
        for x in range(2, 123):
            text_area.x = x
            time.sleep(speed)  # Adjust speed as needed

        # Move left from 126 to 2
        for x in range(122, 1, -2):
            text_area.x = x
            time.sleep(speed)  # Adjust speed as needed
