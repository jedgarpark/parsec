import time
import board
import adafruit_vcnl4040

PLUGGED = True

i2c = board.STEMMA_I2C()
sensor = adafruit_vcnl4040.VCNL4040(i2c)

while PLUGGED:
    try:
        print("Proximity:", sensor.proximity)
        print("Light: %d lux" % sensor.lux)
        time.sleep(1.0)
        PLUGGED = True
    except OSError:
        print("plug in the sensor and reset")
        PLUGGED = False

while not PLUGGED:
    pass
