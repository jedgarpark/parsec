import time
import board
import displayio
import vectorio
import math
import adafruit_touchscreen

display = board.DISPLAY
main_group = displayio.Group()
board.DISPLAY.root_group

palette1 = displayio.Palette(2)
palette1[0] = 0x006699
palette1[1] = 0x440022

circle1 = vectorio.Circle(pixel_shader=palette1, color_index=0, radius=15, x=70, y=40)
circle2 = vectorio.Circle(pixel_shader=palette1, color_index=1, radius=15, x=120, y=80)

main_group.append(circle1)
main_group.append(circle2)

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

p1 = None
p2 = None
distance = None

print("\n\n--Touch screen 2x to find distance between points\n\n\n")

while True:
    p = touchscreen.touch_point
    if p:
        if p1 == None:
            p1 = p
            circle1.x = p1[0]
            circle1.y = p1[1]
            print("point 1:", p1[0], ",", p1[1],"\n")
            time.sleep(0.4)
        else:
            p2 = p
            circle2.x = p2[0]
            circle2.y = p2[1]
            print("point 2:", p2[0], ",", p2[1],"\n")
            time.sleep(0.4)

            distance = dist(p1, p2)
            print("distance:","."*int(distance/10), distance, "\n\n\n")
            p1 = None
            p2 = None
