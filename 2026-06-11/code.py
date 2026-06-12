# SPDX-FileCopyrightText: Copyright (c) 2026 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# CircuitPython Parsec: RGB Character LCD Shield 5 - Move a Character with Buttons

import time
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

lcd_columns = 16
lcd_rows = 2

i2c = board.I2C()
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

# the player glyph
lcd.create_char(0, [
    0b01111,
    0b01110,
    0b11100,
    0b11111,
    0b11100,
    0b01110,
    0b01111,
    0b00000])  # little ship

# player position
col = 0
row = 0

def draw_player():
    lcd.clear()
    lcd.cursor_position(col, row)
    lcd.message = "\x00"

lcd.clear()
lcd.color = [0, 100, 50]
draw_player()

while True:
    moved = False

    if lcd.left_button and col > 0:
        col -= 1
        moved = True
    elif lcd.right_button and col < lcd_columns - 1:
        col += 1
        moved = True
    elif lcd.up_button and row > 0:
        row -= 1
        moved = True
    elif lcd.down_button and row < lcd_rows - 1:
        row += 1
        moved = True

    if moved:
        draw_player()
        # wait for button release
        while (lcd.left_button or lcd.right_button or
               lcd.up_button or lcd.down_button):
            time.sleep(0.02)

    time.sleep(0.05)
