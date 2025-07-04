# SPDX-FileCopyrightText: 2025 john park for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
bitmap indexed transparency with random circles
"""
import os
import time
import random
import board
import displayio
import fourwire
import adafruit_ili9341
import adafruit_imageload
import vectorio

# Release any resources currently in use for the displays
displayio.release_displays()

# Use Hardware SPI
spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10
display_width = 320
display_height = 240
display_bus = fourwire.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = adafruit_ili9341.ILI9341(display_bus, width=display_width, height=display_height)

# Get list of BMP files
images = []
for filename in os.listdir('/'):
    if filename.lower().endswith('.bmp') and not filename.startswith('.'):
        images.append("/"+filename)
print(images)

# Create screen with yellow background and layers
screen = displayio.Group()
display.root_group = screen

# Create yellow background
yellow_bitmap = displayio.Bitmap(display_width, display_height, 1)
yellow_palette = displayio.Palette(1)
yellow_palette[0] = 0x888800  # Yellow
yellow_background = displayio.TileGrid(yellow_bitmap, pixel_shader=yellow_palette, x=0, y=0)
screen.append(yellow_background)

# Create circles layer
circles_group = displayio.Group()
screen.append(circles_group)

# Create random circles
circle_colors = [0x990000, 0x009900, 0x000099, 0x660066, 0x007777, 0x777777]
for i in range(40):  # Create  random circles
    # Create palette for this circle
    circle_palette = displayio.Palette(1)
    circle_palette[0] = random.choice(circle_colors)

    # Random position and size
    x = random.randint(0, display_width - 40)
    y = random.randint(0, display_height - 40)
    radius = random.randint(5, 30)

    # Create circle
    circle = vectorio.Circle(pixel_shader=circle_palette, radius=radius, x=x, y=y)
    circles_group.append(circle)

# Add dummy groups for image layers
screen.append(displayio.Group())  # screen[2] - bottom image layer
screen.append(displayio.Group())  # screen[3] - top image layer

def load_image(img_num):
    print("loading image", img_num)
    t = screen[2]  # get bottom image
    image, palette = adafruit_imageload.load(images[img_num])
    bitmap = displayio.TileGrid(image, pixel_shader=palette)
    screen[2] = bitmap  # new image on bottom
    screen[3] = t       # move bottom image to top

img_num = 0
load_image(img_num)
palette = screen[2].pixel_shader

speed=1.6
transparent_index = 1

while True:

    time.sleep(speed)
    palette.make_transparent(transparent_index)
    # palette.make_transparent(transparent_index+1)
    time.sleep(speed)
    palette.make_opaque(transparent_index)
    # palette.make_opaque(transparent_index+1)
