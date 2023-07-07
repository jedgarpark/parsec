# CircuitPython Circuit Playground Library
from adafruit_circuitplayground import cp

# Example 1:
# cp.red_led = True
#
# while True:
#     pass

# Example 2:
cp.red_led = not cp.switch

switch_state = cp.switch
print("Circuit Playground red LED and switch demo")

while True:
    if cp.switch is True and switch_state is False:
        cp.red_led = False
        print("switch left")
        switch_state = cp.switch

    elif cp.switch is False and switch_state is True:
        cp.red_led = True
        print("switch right")
        switch_state = cp.switch
