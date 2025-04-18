import time
import ssl
import os
from random import randint
import microcontroller
import socketpool
import wifi
import board
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_max1704x

# Create sensor objects, using the board's default I2C bus.
bme280 = adafruit_bme280.Adafruit_BME280_I2C(board.I2C())
batt_monitor = adafruit_max1704x.MAX17048(board.I2C())

# change this to match your location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1014.25

# WiFi
try:
    print("Connecting to %s" % os.getenv("CIRCUITPY_WIFI_SSID"))
    wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
    print("Connected to %s!" % os.getenv("CIRCUITPY_WIFI_SSID"))
# Wi-Fi connectivity fails with error messages, not specific errors, so this except is broad.
except Exception as e:  # pylint: disable=broad-except
    print("Failed to connect to WiFi. Error:", e, "\nBoard will hard reset in 30 seconds.")
    time.sleep(30)
    microcontroller.reset()

# Define callback functions which will be called when certain events happen.
def connected(client):
    print("Connected to Adafruit IO...")

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Initialize a new MQTT Client object
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    username=os.getenv("ADAFRUIT_AIO_USERNAME"),
    password=os.getenv("ADAFRUIT_AIO_KEY"),
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

# Initialize Adafruit IO MQTT "helper"
io = IO_MQTT(mqtt_client)

# Set up the callback methods above
io.on_connect = connected

timestamp = 0


while True:
    try:
        # If Adafruit IO is not connected...
        if not io.is_connected:
            # Connect the client to the MQTT broker.
            print("Connecting to Adafruit IO...")
            io.connect()

        # Explicitly pump the message loop.
        io.loop()
        # Obtain the "random" value, print it and publish it to Adafruit IO every 10 seconds.
        if (time.monotonic() - timestamp) >= 10:
            print("\nTemperature: {:.1f} C".format(bme280.temperature))
            io.publish("f-bme-temp", bme280.temperature)
            print("Humidity: {:.1f} %".format(bme280.relative_humidity))
            io.publish("f-bme-humidity", bme280.humidity)
            timestamp = time.monotonic()

        # Adafruit IO fails with internal error types and WiFi fails with specific messages.
        # This except is broad to handle any possible failure.
    except Exception as e:
        print("Failed to get or send data, or connect. Error:", e,
                "\nBoard will hard reset in 30 seconds.")
        time.sleep(30)
        microcontroller.reset()
