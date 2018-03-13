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
        msg = can.Message(
                arbitration_id=0xE2,
                data=[0x41, 0x42, 0x43, 0x44, 0x41, 0x42, 0x43, 0x44],
                extended_id=False)
        bus.send(msg)
        msg = can.Message(
                arbitration_id=0xA,
                data=[0x41, 0x42, 0x43, 0x44, 0x41, 0x42, 0x43, 0x44],
                extended_id=False)
        bus.send(msg)
        count += 2
        print(count)

except KeyboardInterrupt:
    # Catch keyboard interrupt
    print("\n\rKeyboard interrupt")
    exit()
