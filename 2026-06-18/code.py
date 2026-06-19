# SPDX-FileCopyrightText: Copyright (c) 2026 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# CircuitPython Parsec: RGB Character LCD Shield 7 - Scrolling Marquee

import time
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

lcd_columns = 16
lcd_rows = 2

i2c = board.I2C()
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

lcd.clear()
lcd.color = [20, 30, 50]

message = "  CircuitPython Parsec "

while True:
    lcd.cursor_position(0, 0)
    lcd.message = message
    time.sleep(1)
    for i in range(len(message)):
        lcd.move_left()
        time.sleep(0.3)
    for i in range(len(message)):
            lcd.move_right()
            time.sleep(0.05)
    lcd.clear()
