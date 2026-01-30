# CircuitPython Parsec
# N-hop Cardinal Neighbors

import time

import adafruit_trellism4

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels.brightness = 0.1

# Button grid is 8x4
WIDTH = 8
HEIGHT = 4

DISTANCE = 3  # change this to demonstrate


def light_at_distance(x, y, distance, color=(0, 255, 100)):
    """Light up all pixels at exactly the specified hop in straight lines"""
    # Clear all pixels first
    for px in range(WIDTH):
        for py in range(HEIGHT):
            trellis.pixels[px, py] = (0, 0, 0)

    # Light the pressed button in magenta
    trellis.pixels[x, y] = (255, 0, 255)
    print(x, y, ":")

    if distance == 0:
        return

    # Light pixels in straight horizontal line
    if x + distance < WIDTH:  # Check right boundary
        trellis.pixels[x + distance, y] = color
        print("    ", x + distance, y)

    if x - distance >= 0:  # Check left boundary
        trellis.pixels[x - distance, y] = color
        print("    ", x - distance, y)

    # Light pixels in straight vertical line
    if y + distance < HEIGHT:  # Check bottom boundary
        trellis.pixels[x, y + distance] = color
        print("    ", x, y + distance)

    if y - distance >= 0:  # Check top boundary
        trellis.pixels[x, y - distance] = color
        print("    ", x, y - distance)


# Track previous button state with emtpy set named 'last_pressed'
last_pressed = set()


# Main loop
while True:
    pressed = set(trellis.pressed_keys)  # 'pressed' set for current button

    # Detect newly pressed buttons
    newly_pressed = pressed - last_pressed  # compare the sets

    if newly_pressed:
        x, y = list(newly_pressed)[0]
        light_at_distance(x, y, DISTANCE)

    last_pressed = pressed  # update set
    time.sleep(0.01)
