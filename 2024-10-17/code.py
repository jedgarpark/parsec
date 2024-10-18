import time
import board
import math
import adafruit_touchscreen

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

p1 = None
p2 = None
distance = None

print("\n\n--Touch screen 2x to find distance between points\n\n\n")

while True:
    p = touchscreen.touch_point
    if p:
        if p1 == None:
            p1 = p
            print("point 1:", p1[0], ",", p1[1],"\n")
            time.sleep(0.2)
        else:
            p2 = p
            print("point 2:", p2[0], ",", p2[1],"\n")
            time.sleep(0.2)

            distance = dist(p1, p2)
            print("distance:","."*int(distance/10), distance, "\n\n\n")
            p1 = None
            p2 = None
