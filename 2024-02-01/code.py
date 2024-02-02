# make a circular path with sin/cos

import board
import displayio
import math
import time


display = board.DISPLAY
group = displayio.Group()
bitmap = displayio.Bitmap(5, 5, 1)
palette = displayio.Palette(1)
palette[0] = 0x00FF00  # green color
tile = displayio.TileGrid(bitmap, pixel_shader=palette)
group.append(tile)
display.show(group)

# Set initial position and parameters for curved motion
center_x, center_y = display.width // 2, display.height // 2
angle = 0
radius = 50


fade_steps = 3

while True:
    # Calculate the new position using a sine function for curved motion
    x = center_x + int(radius * math.sin(math.radians(angle)))
    y = center_y + int(radius * math.cos(math.radians(angle)))

    # Update the box position
    tile.x = x
    tile.y = y

    # Update the display
    display.refresh()

    # Increment the angle for the next frame
    angle += 1  # Adjust the speed of the curved motion by changing the increment value

    # Pause for a short time to control the speed of the animation
    time.sleep(0.01)

