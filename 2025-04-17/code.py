# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: Unlicense
"""
CircuitPython Simple Example for BME280
"""
import time
import board
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_max1704x

# Create sensor objects, using the board's default I2C bus.
bme280 = adafruit_bme280.Adafruit_BME280_I2C(board.I2C())
batt_monitor = adafruit_max1704x.MAX17048(board.I2C())

# change this to match your location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1014.25

while True:
    print("\nTemperature: {:.1f} C".format(bme280.temperature))
    print("Humidity: {:.1f} %".format(bme280.relative_humidity))
    print("Pressure: {:.1f} hPa".format(bme280.pressure))
    print("Altitude: {:.2f} meters".format(bme280.altitude))
    print(f"Battery voltage: {batt_monitor.cell_voltage:.2f} Volts")
    print(f"Battery percentage: {batt_monitor.cell_percent:.1f} %")
    time.sleep(5)
