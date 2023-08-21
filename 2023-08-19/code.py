import time
from adafruit_circuitplayground import cp

while True:
    temp = cp.temperature
    temp_f = temp * 1.8 +32
    print("Temperature C: %2.2f F: %3.2f" % (temp, temp_f))

    time.sleep(1)


#fancy temperature meter
# import time
# from adafruit_circuitplayground import cp
#
# cp.pixels.auto_write = False
# cp.pixels.brightness = 0.1
#
# # Set these based on your ambient temperature in Celsius for best results!
# minimum_temp = 23
# maximum_temp = 27
#
#
# def scale_range(value):
#     """Scale a value from the range of minimum_temp to maximum_temp (temperature range) to 0-10
#     (the number of NeoPixels). Allows remapping temperature value to pixel position."""
#     return int((value - minimum_temp) / (maximum_temp - minimum_temp) * 10)
#
#
# while True:
#     peak = scale_range(cp.temperature)
#     print(cp.temperature)
#     print(int(peak))
#
#     for i in range(10):
#         if i <= peak:
#             cp.pixels[i] = (0, 50, 50)
#         else:
#             cp.pixels[i] = (0, 0, 0)
#     cp.pixels.show()
#     time.sleep(0.05)
