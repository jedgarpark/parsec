# parsec Button Sequence, using a button sequence for combination entry
# 
import board
import displayio
import terminalio
from adafruit_display_text import label
import time
import keypad

# Initialize display
display = board.DISPLAY

# Create display group
screen = displayio.Group()
display.root_group = screen

# Create text label
text_area = label.Label(
    terminalio.FONT,
    scale=3,
    text="Enter code:",
    color=0xFFFFFF,
    x=10,
    y=display.height // 2
)
screen.append(text_area)

# Initialize keypad with D1 and D2 (both pulled LOW by default)
keys = keypad.Keys(
    (board.D1, board.D2),
    value_when_pressed=True,  # D1 and D2 go HIGH when pressed
    pull=False  # D1 and D2 use pull-down resistors
)

# Define the correct sequence (can be changed here)
# Key indices: 0=D1, 1=D2
CORRECT_SEQUENCE = [0, 1, 1]  # D1, D2, D2

# Variable for tracking input states
current_sequence = []

def update_display(text):  # Update the display with new text
    text_area.text = text

def reset_sequence():  # Reset the current input sequence
    global current_sequence
    current_sequence = []
    update_display("Enter code:")
    print("Enter code:")


while True:
    event = keys.events.get()
    if event:
        if event.pressed:
            button_index = event.key_number
            current_sequence.append(button_index)  # add the index to sequence

            # Convert index to button name for printing
            button_name = f"D{button_index + 1}"  # string format the "Dx" name (+1 because we start with D1)
            print(f"Button pressed: {button_name}")
            print(f"Current sequence: {current_sequence}")

            # Update display to show progress
            progress = "*" * len(current_sequence)  # show asterisks on display
            update_display(f"Enter code:\n{progress}")

            # Check if we have 3 button presses
            if len(current_sequence) == 3:
                if current_sequence == CORRECT_SEQUENCE:  # compare the two lists
                    update_display("SUCCESS")
                    print("Correct sequence entered!")
                else:
                    update_display("WRONG CODE")
                    print(f"Wrong sequence. Expected: {CORRECT_SEQUENCE}, Got: {current_sequence}")

                # Wait 4 seconds then reset
                time.sleep(2)
                reset_sequence()

        # Small delay to prevent excessive polling
        time.sleep(0.01)
