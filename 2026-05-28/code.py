# SPDX-FileCopyrightText: Copyright (c) 2026 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# CircuitPython Parsec: RGB Character LCD Shield 3 - Custom Characters
# HD44780 CGRAM has 8 slots of 8 bytes each (one byte per row of the 5x8 grid)
# only the lower 5 bits per byte are used since each slot is 5 columns wide

import time
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

lcd_columns = 16
lcd_rows = 2

i2c = board.I2C()
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

# 8 custom glyphs the CGRAM uses as raw byte arrays
lcd.create_char(0, [0b11111,
                    0b10001,
                    0b10001,
                    0b10001,
                    0b10001,
                    0b10001,
                    0b11111,
                    0b11111])  # rectangle/phone

lcd.create_char(1, [0b01110,
                    0b10101,
                    0b11111,
                    0b01110,
                    0b01110,
                    0b00000,
                    0b00000,
                    0b0000])  # skull

lcd.create_char(2, [0b00100,
                    0b01110,
                    0b11111,
                    0b00100,
                    0b00100,
                    0b00000,
                    0b00000,
                    0b00000])  # up arrow

lcd.create_char(3, [0b00000,
                    0b00000,
                    0b00100,
                    0b00100,
                    0b11111,
                    0b01110,
                    0b00100,
                    0b00000])  # down arrow

lcd.create_char(4, [0b00000,
                    0b00100,
                    0b01100,
                    0b11111,
                    0b01100,
                    0b00100,
                    0b00000,
                    0b00000])  # left arrow

lcd.create_char(5, [0b00000,
                    0b00100,
                    0b00110,
                    0b11111,
                    0b00110,
                    0b00100,
                    0b00000,
                    0b00000])  # right arrow

lcd.create_char(6, [0b00000,
                    0b01010,
                    0b11111,
                    0b11111,
                    0b01110,
                    0b00100,
                    0b00000,
                    0b00000])  # heart

lcd.create_char(7, [0b10101,
                    0b01110,
                    0b01110,
                    0b01110,
                    0b01110,
                    0b01010,
                    0b01010,
                    0b11011])  # dude



lcd.clear()
lcd.color = [50, 100, 0]
lcd.message = "custom chars"
lcd.cursor_position(0, 1)
lcd.message = "\x00 \x01 \x02 \x03 \x04 \x05 \x06 \x07"
time.sleep(2)

lcd.cursor_position(0, 1)
lcd.message = "                "

while True:
    chars = "\x00 \x01 \x02 \x03 \x04 \x05 \x06 \x07"
    for i, ch in enumerate(chars):
        lcd.cursor_position(i, 1)
        lcd.message = ch
        time.sleep(0.1)
    time.sleep(4)
    lcd.cursor_position(0, 1)
    lcd.message = "                "
    time.sleep(0.5)
