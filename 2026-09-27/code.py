# Fruit Jam IR Decoder
# generic pulse reading/decoding (protocol agnostic)
# general info: https://learn.adafruit.com/ir-sensor/circuitpython
import pulseio
import adafruit_irremote
import board1
import neopixel


ir_pin = board.IR
pulsein = pulseio.PulseIn(ir_pin, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()


pixels = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=0.3, auto_write=False)
pixels.fill(0x000000)
pixels.show()


# NEC command bytes are: (address, ~address, command, ~command)
remote = {
    (0, 255, 58, 197): "44-key Brighter",
    (0, 255, 186, 69): "44-key Dimmer",
    (0, 255, 2, 253): "44-key Power",
    (0, 255, 130, 125): "44-key Play",
    (0, 255, 26, 229): "44-key Red",
    (0, 255, 154, 101): "44-key Green",
    (0, 255, 162, 93): "44-key Blue",
    (0, 255, 34, 221): "44-key White",
    (169, 0): "Sony Power",
    (165, 0): "Sony TV/Video",
    ( 73, 0): "Sony Vol +",
    (201, 0): "Sony Vol -",
    (  9, 0): "Sony CH +",
    (137, 0): "Sony CH -",
    ( 89, 10): "Sony Play",
    ( 25, 10): "Sony Stop",
    (217, 10): "Sony REW",
    ( 57, 10): "Sony FF",
}

# Map specific button names to NeoPixel fill colors
color_buttons = {
    "44-key Red": 0xFF0000,
    "44-key Green": 0x00FF00,
    "44-key Blue": 0x0000FF,
    "44-key White": 0xFFFFFF,
    "Sony Play": 0x00AAFF,
    "Sony Stop": 0xFF00FF,
}


while True:
    pulses = decoder.read_pulses(pulsein)
    try:
        code = decoder.decode_bits(pulses)
        print(pulses)
        print("Received pulses:", len(pulses))
        print("Decoded:", code)
        if code in remote:
            name = remote[code]
            print("Button:", name)
            if name in color_buttons:
                pixels.fill(color_buttons[name])
                pixels.show()
        else:
            print("Unknown Button")
    except adafruit_irremote.IRNECRepeatException:
        print("NEC repeat!")
    except adafruit_irremote.IRDecodeException as e:
        print("Failed to decode:", e.args)
    print("----------------------------")
