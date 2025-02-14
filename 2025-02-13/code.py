import board
import busio
from adafruit_ht16k33.matrix import Matrix8x8x2
import time
from matrix_chars import CHARS

# Initialize I2C and the matrix
i2c = board.STEMMA_I2C()
matrix = Matrix8x8x2(i2c)

def display_char(char, char_color=1, bg_color=0):
    """
    Display a character on the LED matrix with color options.

    Parameters:
    char (str): Single character to display
    char_color (int): Color for the character pixels (0-3)
        0 = off
        1 = green
        2 = red
        3 = yellow (both red and green)
    bg_color (int): Color for the background pixels (0-3)
        Uses same color codes as char_color
    """
    # Validate color inputs
    if not (0 <= char_color <= 3 and 0 <= bg_color <= 3):
        raise ValueError("Colors must be between 0 and 3")

    # Set background color first
    for x in range(8):
        for y in range(8):
            matrix[x, y] = bg_color

    # If character exists in our pattern dictionary
    if char in CHARS:  # Note: no more .upper() - we support both cases
        pattern = CHARS[char]
        # Set each row according to the pattern
        for row in range(8):
            for col in range(8):
                # Check if bit is set in pattern
                if pattern[row] & (1 << (7 - col)):
                    matrix[col, row] = char_color

    matrix.show()

# Test program to show all characters
def test_all_chars():
    # Test uppercase
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print(f"Displaying uppercase {c}")
        display_char(c, char_color=1)  # Green
        time.sleep(0.3)

    # Short pause between sets
    time.sleep(1)

    # Test lowercase
    for c in "abcdefghijklmnopqrstuvwxyz":
        print(f"Displaying lowercase {c}")
        display_char(c, char_color=2)  # Red
        time.sleep(0.3)

    time.sleep(1)

    for c in "0123456789":
        print(f"Displaying numbers {c}")
        display_char(c, char_color=3)
        time.sleep(0.3)

# test_all_chars()

while True:
    for c in "Hi, Lars? ":
        display_char(c, char_color=3)
        time.sleep(0.3)
    time.sleep(1)
