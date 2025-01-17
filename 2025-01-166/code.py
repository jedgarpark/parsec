# SPDX-FileCopyrightText: 2024 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
'''
LED fade attenuation
see this guide for hardware: https://learn.adafruit.com/neotrellis-midi-feedback-controller
'''

import time
import board
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis
import math  # For logarithmic and exponential fade

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the trellis array
trelli = [
    [NeoTrellis(i2c, False, addr=0x2E), NeoTrellis(i2c, False, addr=0x2F)],
    [NeoTrellis(i2c, False, addr=0x30), NeoTrellis(i2c, False, addr=0x31)]
]
trellis = MultiTrellis(trelli)
trellis.brightness = 1.0  # Set the initial brightness to 0.7

# Define dimensions (4x4 per board, 2x2 grid of boards = 8x8 total)
width = 8   # 2 boards x 4 pixels
height = 8  # 2 boards x 4 pixels

# Set the initial color to green (0x00FF00)
COLOR = 0xffff00

# Function to convert hex color to RGB tuple
def hex_to_rgb(hex_color):
    r = (hex_color >> 16) & 0xFF
    g = (hex_color >> 8) & 0xFF
    b = hex_color & 0xFF
    return (r, g, b)

# Function to cycle through  different fade methods
def apply_fade_method(xcoord, ycoord, color, delay=0.005, min_brightness=0.015):
    # Define the different fade methods
    fade_methods = [
        ("Linear Fade", linear_fade),         # 0: Linear Fade
        ("Logarithmic Fade", logarithmic_fade),    # 1: Logarithmic Fade
        ("Quadratic Fade", quadratic_fade),      # 2: Quadratic Fade
        ("Exponential Fade", exponential_fade),    # 3: Exponential Fade
        ("Linear Fade", linear_fade),         # 4: Linear Fade (repeat)
        ("Logarithmic Fade", logarithmic_fade),    # 5: Logarithmic Fade (repeat)
        ("Quadratic Fade", quadratic_fade),      # 6: Quadratic Fade (repeat)
        ("Exponential Fade", exponential_fade),    # 7: Exponential Fade (repeat)
    ]

    # Get the fade method based on the row (ycoord)
    fade_name, fade_method = fade_methods[ycoord]

    # Print the name of the fade method
    print(f"Applying {fade_name} for row {ycoord}...")

    # Apply the selected fade method
    fade_method(xcoord, ycoord, color, delay, min_brightness)

# Fade methods (Linear, Logarithmic, Quadratic, Exponential)

def linear_fade(xcoord, ycoord, color, delay, min_brightness):
    # Linear fade from full brightness to dim
    for offset in range(1, width - xcoord):
        brightness = max(1.0 - offset * 0.2, min_brightness)
        trellis.color(xcoord + offset, ycoord, adjust_brightness(color, brightness))
        time.sleep(delay)

def logarithmic_fade(xcoord, ycoord, color, delay, min_brightness):
    # Logarithmic fade (logarithmic decay of brightness)
    for offset in range(1, width - xcoord):
        brightness = max(1.0 - math.log(offset + 1) / math.log(width), min_brightness)
        trellis.color(xcoord + offset, ycoord, adjust_brightness(color, brightness))
        time.sleep(delay)

def quadratic_fade(xcoord, ycoord, color, delay, min_brightness):
    # Quadratic fade (brightness decreases as square of offset)
    for offset in range(1, width - xcoord):
        brightness = max(1.0 - (offset / width) ** 2, min_brightness)
        trellis.color(xcoord + offset, ycoord, adjust_brightness(color, brightness))
        time.sleep(delay)

def exponential_fade(xcoord, ycoord, color, delay, min_brightness):
    # Exponential fade (faster decay of brightness)
    for offset in range(1, width - xcoord):
        brightness = max(1.0 * (0.5 ** offset), min_brightness)  # Exponential decay
        trellis.color(xcoord + offset, ycoord, adjust_brightness(color, brightness))
        time.sleep(delay)

# Adjust color brightness (this scales the RGB components based on the brightness)
def adjust_brightness(color, brightness):
    r, g, b = color
    # Scale each RGB component by the brightness factor
    r = int(r * brightness)
    g = int(g * brightness)
    b = int(b * brightness)
    # Return the new RGB value
    return (r, g, b)

# Flash all pixels green and then turn them off
def flash_green():
    # Turn all pixels green
    for y in range(height):
        for x in range(width):
            trellis.color(x, y, (0, 55, 0))  # RGB for green

    # Hold for a brief moment
    time.sleep(0.5)

    # Turn all pixels off
    for y in range(height):
        for x in range(width):
            trellis.color(x, y, (0, 0, 0))  # RGB for off

# Function to clear the row (turn off all LEDs in the row)
def clear_row(ycoord):
    for x in range(width):
        trellis.color(x, ycoord, (0, 0, 0))  # Turn off all LEDs in the row

# Callback function for button press
def blink(xcoord, ycoord, edge):
    # Only handle button down events
    if edge == NeoTrellis.EDGE_RISING:
        if xcoord == 0:
            # If the first button in the row is pressed, apply the starburst effect
            print(f"Button {ycoord} pressed (Row {ycoord})")
            color = hex_to_rgb(COLOR)  # Use the set color
            trellis.color(xcoord, ycoord, color)  # Keep the pressed button lit
            apply_fade_method(xcoord, ycoord, color)
        else:
            # If any other button in the row is pressed, clear the row
            print(f"Clearing row {ycoord} due to button {xcoord} press")
            clear_row(ycoord)

# Set up the callbacks and activate all keys
for y in range(height):
    for x in range(width):
        # Activate key with callback
        trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
        trellis.set_callback(x, y, blink)
        # Turn off all LEDs
        trellis.color(x, y, (0, 0, 0))

print("Ready!")

# Flash all pixels green and then off
flash_green()

while True:
    # Call sync to handle the button presses
    trellis.sync()
    time.sleep(0.02)  # Small delay to prevent overwhelming the I2C bus
