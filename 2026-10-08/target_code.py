# QT Py RP2040 as Target: report BOOT button state at 0x42
import board
import digitalio
import neopixel

from i2ctarget import I2CTarget

ADDRESS = 0x42

pixel_power = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
pixel_power.switch_to_output(value=True)

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.05)
pixel.fill((0, 255, 0))

button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

with I2CTarget(board.SCL1, board.SDA1, (ADDRESS,)) as device:
    print(f"target live at 0x{ADDRESS:02x}")
    while True:
        req = device.request()
        if not req:
            continue
        with req:
            if req.is_read:
                req.write(bytes([0 if button.value else 1]))
