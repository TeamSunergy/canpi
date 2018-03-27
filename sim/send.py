#!/usr/bin/python3
# SEND
#github.com/skpang/PiCAN-Python-examples/blob/master/simple_tx_test.py

import can
import time
import os

count = 0

# network settings
channel = "vcan0"
bitrate = 128000

#os.system("sudo /sbin/ip link set " + channel + " up type vcan")
print("Press CTRL-C to exit")

try:
    bus = can.interface.Bus(
            channel = channel,
            bustype = "socketcan_native")
except OSError:
    print("Interface " + channel + " is down.")
    exit()


# Main loop
try :
    while True:
    	msg = can.Message(arbitration_id=0x0A,
    	data=[0x8F, 0x3A, 0x8E, 0xA3, 0x13, 0x01, 0xE3, 0x00],extended_id=False)
    	bus.send(msg)
    	msg = can.Message(arbitration_id=0x0B,data=[0x00, 0x95, 0x60, 0x64, 0x00, 0x0f, 0xef, 0x57],extended_id=False)
    	bus.send(msg)
    	msg = can.Message(arbitration_id=0x0C,data=[0x00, 0x25, 0x10, 0x24, 0x00, 0x0f, 0xaf, 0x57],extended_id=False)
    	bus.send(msg)
    	msg = can.Message(arbitration_id=0x0D,data=[0x00, 0x15, 0x08, 0x04, 0x00, 0x0f, 0x1f, 0x57],extended_id=False)
    	bus.send(msg)
    	count += 2
    	print(count)

except KeyboardInterrupt:
    # Catch keyboard interrupt
    print("\n\rKeyboard interrupt")
    exit()
