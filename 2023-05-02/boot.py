# this will change the USB device identification
import supervisor

supervisor.set_usb_identification(
                                  manufacturer='LarsCo',
                                  product='My Cool USB Thingy',
                                  vid=0x2E9A, # Adafruit VID
                                  pid=0x1234 # fake PID

)
