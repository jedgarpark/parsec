# SPDX-FileCopyrightText: Copyright (c) 2026 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# CircuitPython Parsec: RGB Character LCD Shield 4 - Custom Character Animation

import time

import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import board

lcd_columns = 16
lcd_rows = 2

i2c = board.I2C()
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

frames = [
    [0b11111, 0b10000, 0b10000, 0b00000, 0b00000, 0b00000, 0b11101, 0b01111],
    [0b11111, 0b00001, 0b00001, 0b00000, 0b00000, 0b00000, 0b11101, 0b10111],
    [0b00111, 0b00001, 0b00001, 0b00001, 0b00001, 0b00000, 0b11011, 0b11011],
    [0b00001, 0b00001, 0b00001, 0b00001, 0b00111, 0b00000, 0b10111, 0b11101],
    [0b00000, 0b00000, 0b00001, 0b00001, 0b11111, 0b00000, 0b01111, 0b11110],
    [0b00000, 0b00000, 0b10000, 0b10000, 0b11111, 0b00000, 0b10111, 0b11101],
    [0b10000, 0b10000, 0b10000, 0b10000, 0b11100, 0b00000, 0b11011, 0b11011],
    [0b11100, 0b10000, 0b10000, 0b10000, 0b10000, 0b00000, 0b11111, 0b10111],
]

slots = ["\x00", "\x01", "\x02", "\x03", "\x04", "\x05", "\x06", "\x07"]

lcd.clear()
lcd.color = [50, 100, 0]
lcd.message = "char animation  "

while True:
    # load each frame into its own CGRAM slot and display across row 1
    for j in range(8):
        lcd.create_char(j, frames[j])
        lcd.cursor_position(j + 1, 1)
        lcd.message = slots[j]
        time.sleep(0.5)

    # hold
    time.sleep(2)

    # animate — write slot 0 once, then rewrite CGRAM in loop
    lcd.clear()
    lcd.message = "char animation  "
    lcd.cursor_position(0, 1)
    lcd.message = "\x00"

    for _ in range(10):
        for frame in frames:
            lcd.create_char(0, frame)
            time.sleep(0.02)

    time.sleep(0.5)
    lcd.clear()
    lcd.message = "char animation  "
    time.sleep(0.5)
