
import time
import board
import pulseio
import adafruit_irremote
import board
import displayio
import terminalio
import vectorio
from adafruit_display_text import label
import adafruit_st7789

display=board.DISPLAY

# Load font
font = terminalio.FONT

# Create a group for the display elements
group = displayio.Group()

# Create a text area
text_area = label.Label(font, text="ir recv", color=0x00ff00, scale=9)
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (display.width // 2, display.height // 2)
group.append(text_area)

palette = displayio.Palette(3)
palette[0] = 0xff0000
palette[1] = 0x00ff00
palette[2] = 0x0

circ1=vectorio.Circle(pixel_shader=palette, radius=12, x=44, y=44, color_index=2)
group.append(circ1)

# Show the group
display.root_group=group

# IR receiver setup
ir_receiver = pulseio.PulseIn(board.D4, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

def decode_ir_signals(p):
    codes = decoder.decode_bits(p)
    return codes

# Define IR remote codes and corresponding messages for a Vizio remote
REMOTE_CODES = { 
    "20DFF40B": "INPUT", "20DF10EF": "ON/OFF",
    "20DFF609": "LarsTV", "20DFD728": "NETFLIX", "20DF7788": "RADIO",
    "20DFAC53": "REWIND", "20DFCC33": "PAUSE/PLAY", "20DF6C93": "FAST FWD",
    "20DF9C63": "CC", "20DF2CD3": "REC", "20DF0CF3": "STOP", "20DFF20D": "MENU",
    "20DF926D": "EXIT", "20DFD827": "INFO", "20DF52AD": "BACK", "20DF38C7": "GUIDE",
    "20DFA25D": "UP", "20DF629D": "DOWN", "20DFE21D": "LEFT", "20DF12ED": "RIGHT",
    "20DF22DD": "OK",
    "20DF40BF": "VOL +", "20DFC03F": "VOL -",
    "20DFB44B": "Adafruit",
    "20DF00FF": "CH +", "20DF807F": "CH -",
    "20DF906F": "MUTE", "20DFEE11": "WIDE", "20DFE619": "PIC", "20DF58A7": "TALK",
    "20DF8877": "1", "20DF48B7": "2", "20DFC837": "3",
    "20DF28D7": "4", "20DFA857": "5", "20DF6897": "6",
    "20DFE817": "7", "20DF18E7": "8", "20DF9867": "9",
    "20DF5CA3": "ENTER", "20DF08F7": "0", "20DFFF00": "DASH",
}

while True:
    pulses = decoder.read_pulses(ir_receiver)
    circ1.color_index=0
    try:
        # Attempt to decode the received pulses
        received_code = decode_ir_signals(pulses)
        print("length of pulses:", len(pulses), "\nPulses:", pulses)
        circ1.color_index = 0
        print(received_code)
        if received_code:
            hex_code = ''.join(["%02X" % x for x in received_code])
            if hex_code in REMOTE_CODES:  # matched one of the known codes
                message = REMOTE_CODES[hex_code]
                text_area.text=message
                circ1.color_index = 1
            else:
                text_area.text=hex_code  # no match, just print the hex code

        print(f"Received: {hex_code}\n")
    except adafruit_irremote.IRNECRepeatException:  # Signal was repeated, ignore
        print("repeat")
        circ1.color_index=0
        pass
    except adafruit_irremote.IRDecodeException:  # Failed to decode signal
        circ1.color_index=0
        print("Error decoding")
