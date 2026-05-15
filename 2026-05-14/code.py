# SPDX-FileCopyrightText: Copyright (c) 2026 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# CircuitPython Parsec: RGB Character LCD Shield
# 40 column buffer width of the display ram


import time
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

lcd_columns = 16
lcd_rows = 2

i2c = board.I2C()
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.clear()  # clears the display
lcd.blink = True  # blinking cursor
lcd.color = [100, 100, 0]  # backlight color


lcd.cursor_position(0, 0)
time.sleep(3)
lcd.message = "Character LCD"


while True:
    if lcd.left_button:
        lcd.move_left()
    elif lcd.right_button:
        lcd.move_right()
    elif lcd.down_button:
        lcd.cursor_position(0,1)
        lcd.message="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@$^"
        lcd.blink = False

    time.sleep(0.125)
