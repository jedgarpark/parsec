'''
Parsec battery voltage monitor
'''
import time
import board
from analogio import AnalogIn

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

while True:
    battery_voltage = get_voltage(vbat_voltage)
    if battery_voltage > 3.7:
        print("{:.2f}V is good!".format(battery_voltage))
    else:
        print("{:.2f}V is low, time to charge".format(battery_voltage))
    time.sleep(1.5)
