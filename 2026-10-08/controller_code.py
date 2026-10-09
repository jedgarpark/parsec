# Raspberry Pi Pico as Controller: poll the QT Py's button
import time
import board
import busio
import digitalio

power_led = digitalio.DigitalInOut(board.LED)
power_led.switch_to_output(value=True)

led = digitalio.DigitalInOut(board.GP15)
led.switch_to_output()

ADDRESS = 0x42
i2c = busio.I2C(board.GP1, board.GP0)  # scl, sda

buf = bytearray(1)
last = None

while True:
    while not i2c.try_lock():
        pass
    try:
        i2c.readfrom_into(ADDRESS, buf)
        pressed = bool(buf[0])
        led.value = pressed
        if pressed != last:
            print("BOOT pressed" if pressed else "BOOT released")
            last = pressed
    except OSError:
        pass
    finally:
        i2c.unlock()

    time.sleep(0.05)
