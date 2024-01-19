import os
import time
import wifi
import ipaddress

ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

print("connecting to WiFi", ssid)
wifi.radio.connect(ssid, password)

print("my ip address:", wifi.radio.ipv4_address)

IP_TO_PING = "1.1.1.1"
TIMEOUT = 1.0

ipv4 = ipaddress.ip_address(IP_TO_PING)

while True:
    ping_results = wifi.radio.ping(ipv4, timeout=TIMEOUT)
    print("ping: %s %.d ms" % (ipv4, ping_results * 1000) )
    time.sleep(10.0)
