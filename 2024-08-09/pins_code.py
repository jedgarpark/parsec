# nice pin printout
# https://forums.adafruit.com/viewtopic.php?t=210926
import board
import microcontroller

if True: # show Pin Assignments
    print("\t\tMicrocontroller Pin Assignments:")
    board_pins = []
    for pin in dir(microcontroller.pin):
        if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
            pins = []
            for alias in dir(board):
                if getattr(board, alias) is getattr(microcontroller.pin, pin):
                    pins.append("board.{}".format(alias))
            if len(pins) > 0:
                board_pins.append(" ".join(pins))
    for pins in sorted(board_pins):
        print(pins)
