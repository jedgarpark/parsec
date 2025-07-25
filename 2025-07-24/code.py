import digitalio
import board
import time


button = digitalio.DigitalInOut(board.A1)

# Set up button on A1 as input with pull-up - the long way:
#
# button.direction = digitalio.Direction.INPUT
# button.pull = digitalio.Pull.UP

# Set up button on A1 as input with pull-up - the concise way:
#
button.switch_to_input(pull=digitalio.Pull.UP)

# Set up LED on SCK as output
led = digitalio.DigitalInOut(board.SCK)
led.switch_to_output()

while True:
    # Button is pressed when it reads False (pulled to ground)
    if not button.value:
        led.value = True   # Turn on LED
        print("Button pressed - LED on")
    else:
        led.value = False  # Turn off LED
        print("Button released - LED off")

    time.sleep(0.1)  # Small delay
