# vectorio triangle drawing tool

import time
import board
import displayio
import vectorio
import math
import adafruit_touchscreen

display = board.DISPLAY
main_group = displayio.Group()
board.DISPLAY.root_group

print("\n\n\n\n\n\n\n\n--Touch screen 3x to draw triangle\n\n\n\n\n\n\n")
time.sleep(1)

palette1 = displayio.Palette(1)
palette1[0] = 0xff0000
palette2 = displayio.Palette(1)
palette2[0] = 0x00ff00
palette3 = displayio.Palette(1)
palette3[0] = 0x0000ff
palette4 = displayio.Palette(1)
palette4[0] = 0xff00ff

first_pt = vectorio.Circle(pixel_shader=palette1, radius=2, x=4, y=0)
second_pt = vectorio.Circle(pixel_shader=palette2, radius=2, x=4, y=32)
third_pt = vectorio.Circle(pixel_shader=palette3, radius=2, x=4, y=64)

my_points = [(1,1), (2,2), (3,3) ]
my_tri = vectorio.Polygon(pixel_shader=palette4, points=my_points)

main_group.append(my_tri)
main_group.append(first_pt)
main_group.append(second_pt)
main_group.append(third_pt)

display.root_group = main_group

# Initialize the touch overlay
touchscreen = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL, board.TOUCH_XR, board.TOUCH_YD, board.TOUCH_YU,
    calibration=((6584, 59861), (9505, 57492)),
    size=(board.DISPLAY.width, board.DISPLAY.height),
)

pt1 = None
pt2 = None
pt3 = None


while True:
    pt = touchscreen.touch_point
    if pt:
        if pt1 == None:  # first point
            pt1 = pt
            # hide stuff
            my_tri.x=-400
            second_pt.x=-400
            third_pt.x=-400
            # draw start point
            first_pt.x=pt1[0]
            first_pt.y=pt1[1]
            time.sleep(0.5)

        else:
            if pt2 == None:
                pt2 = pt  # second point 
                second_pt.x=pt2[0]
                second_pt.y=pt2[1]
                time.sleep(0.5)

            else:
                pt3 = pt  # third point 
                third_pt.x = pt3[0]
                third_pt.y = pt3[1]
                time.sleep(0.1)
                my_tri.x=0
                my_tri.y=0
                my_tri.points=[(pt1[0], pt1[1]), (pt2[0], pt2[1]), (pt3[0], pt3[1])]

                pt1 = None
                pt2 = None
                pt3 = None
                time.sleep(1)

