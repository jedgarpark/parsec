# displayio buttons on PyPortal
import time
import board
import terminalio
import displayio
from adafruit_button import Button
import adafruit_touchscreen
from adafruit_bitmap_font import bitmap_font

# displayio.release_displays()
display=board.DISPLAY

my_display_group = displayio.Group()
display.root_group = my_display_group

font = bitmap_font.load_font("/fonts/GothamBlack-25.bdf")

# Setup touchscreen (PyPortal)
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(display.width, display.height),
)

button1 = Button(
    x=10,
    y=10,
    width=display.width//2,
    height=display.height//3,
    style=Button.ROUNDRECT,
    fill_color=0x330040,
    outline_color=0xFF00FF,
    label="John",
    label_font=bitmap_font.load_font("/fonts/Lato-Bold-ltd-25.bdf"),
    label_color=0xFF00FF,
    selected_fill=0x220022,
    selected_outline=0xFF0000,
    selected_label=0xFF0000
)

button2 = Button(
    x=10,
    y=display.height//3 + 20,
    width=display.width//2,
    height=display.height//3,
    style=Button.ROUNDRECT,
    fill_color=0x330040,
    outline_color=0xFF00FF,
    label="Lars",
    label_font=bitmap_font.load_font("/fonts/Lato-Bold-ltd-25.bdf"),  # terminalio.FONT,
    label_color=0xFF00FF,
    selected_fill=0x220022,
    selected_outline=0xFF0000,
    selected_label=0xFF0000
)

my_display_group.append(button1)
my_display_group.append(button2)

b1_state = False
b2_state = False

while True:
    p = ts.touch_point
    if p:
        if button1.contains(p):
            button1.selected = True
            if not b1_state:
                print("A pressed")
                b1_state=True
        else:
            button1.selected = False  # if touch is dragged outside of button
            if b1_state:
                print("A released")
                b1_state=False

        if button2.contains(p):
            button2.selected = True
            if not b2_state:
                print("B pressed")
                b2_state=True
        else:
            button2.selected = False
            if b2_state:
                print("B released")
                b2_state=False
    else:
        button1.selected = False  # if touch is released
        if b1_state:
            print("A released")
            b1_state=False
        button2.selected = False
        if b2_state:
            print("B released")
            b2_state=False
