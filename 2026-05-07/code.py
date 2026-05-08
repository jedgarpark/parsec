# SPDX-FileCopyrightText: Copyright (c) 2026 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# CircuitPython Parsec: RGB LCD Shield basics
# Press the five buttons to change the backlight color
# shield handles button scanning, sends over I2C

import time
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

lcd_columns = 16
lcd_rows = 2

i2c = board.I2C()
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

# function to set the LCD color and the message
def show_color(name, color):
    lcd.color = color
    lcd.message = f"{name}           \n                "
    print(f"Color: {name} {color}")

# Startup
lcd.clear()
lcd.color = [100, 100, 100]
lcd.message = "Press a button"
print("Press a button")

while True:
    #  check all the buttons, call the show_color function with argument
    if lcd.select_button:
        show_color("Red", [100, 0, 0])
    elif lcd.up_button:
        show_color("Green", [0, 100, 0])
    elif lcd.down_button:
        show_color("Blue", [0, 0, 100])
    elif lcd.left_button:
        show_color("Yellow", [100, 100, 0])
    elif lcd.right_button:
        show_color("Cyan", [0, 100, 100])
    time.sleep(0.05)
