# SEND

#!/usr/sbin/python3.5
#github.com/skpang/PiCAN-Python-examples/blob/master/simple_tx_test.py

import RPi.GPIO as GPIO
import can
import time
import os

led = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, True)

count = 1

channel = "can0"
bitrate = 10000

print("\n\rCAN Rx test")
print("Bring up CAN0...")

# Bring up can0 interface at 500kbps
if(channel == "can0"):
	os.system("sudo /sbin/ip link set can0 up type can bitrate " + str(bitrate))
else:
	os.system("sudo /sbin/ip link set " + channel + " up type vcan")

time.sleep(0.1) # from simple_tx_test.py, but I don't know why its there
print("Press CTRL-C to exit")

try:
    bus = can.interface.Bus(
            channel = channel,
            bustype = "socketcan_native")
except OSError:
    print("Cannot find PiCAN board.")
    GPIO.output(led, False)
    exit()


# Main loop
try :
    while True:
        GPIO.output(led, True)
        msg = can.Message(
                arbitration_id=0xc0ffee,
                data=[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07],
                extended_id=False)
        bus.send(msg)
        count += 1
        time.sleep(0.1)
        GPIO.output(led, False)
        time.sleep(0.1)
        print(count)

except KeyboardInterrupt:
    # Catch keyboard interrupt
    GPIO.output(led, False)
    os.system("sudo /sbin/ip link set " + channel + " down")
    print("\n\rKeyboard interrupt")
