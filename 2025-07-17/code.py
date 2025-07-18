# random numbers from floating pins
# open pin acts like an antenna picking up voltage from environment

import analogio
import board
import time

pins = [
    analogio.AnalogIn(board.A0),
    analogio.AnalogIn(board.A1),
    analogio.AnalogIn(board.A2),
    analogio.AnalogIn(board.A3)
]

while True:
    # read the pins
    values = [pin.value for pin in pins]

    # add all the values together
    added = values[0] + values[1] + values[2] + values[3]

    print(f"Pins: {values}")
    print(f"Added: {added}")
    print("---")
    time.sleep(0.5)
