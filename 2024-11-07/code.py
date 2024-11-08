# vectorio circle drawing tool

import time
import board
import displayio
import vectorio
import math
import adafruit_touchscreen

display = board.DISPLAY
main_group = displayio.Group()
board.DISPLAY.root_group

print("\n\n\n\n\n\n\n\n--Touch screen 2x to draw circle center and radius\n\n\n\n\n\n\n")
time.sleep(4)

palette1 = displayio.Palette(1)
palette1[0] = 0xff0000
palette2 = displayio.Palette(1)
palette2[0] = 0x00ff00
palette3 = displayio.Palette(1)
palette3[0] = 0x0000ff

center_pt = vectorio.Circle(pixel_shader=palette1, radius=4, x=4, y=4)
edge_pt = vectorio.Circle(pixel_shader=palette2, radius=4, x=4, y=64)
circle = vectorio.Circle(pixel_shader=palette3, radius=4, x=4, y=124)

main_group.append(circle)  # draw the circle first so dots appear on top
main_group.append(edge_pt)
main_group.append(center_pt)

display.root_group = main_group

# Initialize the touch overlay
touchscreen = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL, board.TOUCH_XR, board.TOUCH_YD, board.TOUCH_YU,
    calibration=((6584, 59861), (9505, 57492)),
    size=(board.DISPLAY.width, board.DISPLAY.height),
)

def dist(point_a, point_b):
      """
      Calculate the distance between two points.
      :param tuple point_a: x,y pair of the first point (plus touch pressure)
      :param point_b: x,y pair of the second point (plus touch pressure)
      :return: the distance between the two points
      """
      ax, ay, ap = point_a
      bx, by, bp = point_b
      return int( math.sqrt( (bx-ax) ** 2 + (by-ay) ** 2 ) )

pt1 = None
pt2 = None
distance = None
center = None
radius = None




while True:
    pt = touchscreen.touch_point
    if pt:
        if pt1 == None:  # first point it being set
            pt1 = pt
            # hide the circle and diameter point
            circle.x=-400
            edge_pt.x=-400

            # draw center point
            center_pt.x=pt1[0]
            center_pt.y=pt1[1]
            time.sleep(0.5)

        else:
            pt2 = pt  # second point is being set
            # draw edge point
            edge_pt.x=pt2[0]
            edge_pt.y=pt2[1]
            time.sleep(0.75)

            # draw full circle
            distance = dist(pt1, pt2)
            circle.x=pt1[0]
            circle.y=pt1[1]
            circle.radius= distance
            time.sleep(1)
            pt1 = None
            pt2 = None
