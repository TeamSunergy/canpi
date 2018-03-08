#!/usr/bin/python3
# SEND
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

count = 0

# network settings
channel = "vcan0"
bitrate = 128000

print("\n\rCAN Tx test")
#print("Bring up " + channel + "...")

# Bring up $channel interface at $bitrate
#if(channel == "can0"):
#	os.system("sudo /sbin/ip link set can0 up type can bitrate " + str(bitrate))
#else:
#	os.system("sudo /sbin/ip link set " + channel + " up type vcan")

time.sleep(0.1) # from simple_tx_test.py, ensures interface is up before trying to use it.
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
                arbitration_id=0x1,
                data=[0x41, 0x42, 0x43, 0x44, 0x41, 0x42, 0x43, 0x44],
                extended_id=False)
        bus.send(msg)
        count += 1
        #time.sleep(0.1)
        GPIO.output(led, False)
        #time.sleep(0.1)
        print(count)

except KeyboardInterrupt:
    # Catch keyboard interrupt
    GPIO.output(led, False)
    #os.system("sudo /sbin/ip link set " + channel + " down")
    print("\n\rKeyboard interrupt")
