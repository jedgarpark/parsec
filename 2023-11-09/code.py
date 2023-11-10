import supervisor
import board
import keypad
# will wait for user to pick between different code files to run. automatically reloads.

key_pins = (board.BUTTON_A, board.BUTTON_B)  # pins vary by board
keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True)
print("Press A or B to run code1.py or code2.py")


while True:
    event = keys.events.get()
    if event:
        key_number = event.key_number
        if event.pressed:
            if key_number is 0:
                print("will run code1 ")
                supervisor.set_next_code_file('code1.py')

            else:
                print("will run code2")
                supervisor.set_next_code_file('code2.py')

        if event.released:
            supervisor.reload()
