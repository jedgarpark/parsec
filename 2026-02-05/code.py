import time
import adafruit_trellism4

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels[0, 0] = (0, 50, 0)

# Button grid is 8x4
WIDTH = 8
HEIGHT = 4


def get_distance(x1, y1, x2, y2):
    """Return Manhattan distance between two points"""
    return abs(x1 - x2) + abs(y1 - y2)


def starburst(x, y, color=(255, 0, 0)):
    """Animate a starburst from the pressed button expanding to edges"""
    max_distance = WIDTH + HEIGHT  
    pixel_distances = {}

    # Expand in waves
    for distance in range(max_distance):
        for px in range(WIDTH):
            for py in range(HEIGHT):
                d = get_distance(x, y, px, py)

                # Light new pixels at this distance
                if d == distance:
                    pixel_distances[(px, py)] = distance
                    # time.sleep(0.4)

                # Dim all previously lit pixels
                if (px, py) in pixel_distances:
                    age = distance - pixel_distances[(px, py)]
                    brightness = max(0.0, 1.0 - (age / 3.0))  # fast fade
                    faded_color = tuple(int(c * brightness) for c in color)
                    trellis.pixels[px, py] = faded_color

        time.sleep(0.02)

    # Quick fade out
    for fade_x in range(WIDTH):
        for fade_y in range(HEIGHT):
            trellis.pixels[fade_x, fade_y] = (0, 0, 0)


# Track previous button state
last_pressed = set()

# Main loop
while True:
    pressed = set(trellis.pressed_keys)
    newly_pressed = pressed - last_pressed

    if newly_pressed:
        x, y = list(newly_pressed)[0]
        starburst(x, y, color=(200, 0, 100))

    last_pressed = pressed

    time.sleep(0.01)
