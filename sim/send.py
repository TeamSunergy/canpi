#!/usr/bin/python3
# SEND
#github.com/skpang/PiCAN-Python-examples/blob/master/simple_tx_test.py

import can
import time
import os

count = 0

# network settings
channel = "can1"
bitrate = 125000

#os.system("sudo /sbin/ip link set " + channel + " up type vcan")
print("Press CTRL-C to exit")

try:
    bus = can.interface.Bus(channel = channel,bustype = "socketcan_native")
except OSError:
    print("Interface " + channel + " is down.")
    exit()


# Main loop
try :
    while True:
        time.sleep(1.1)
        logFrame0 = can.Message(arbitration_id=0x08f89540,data=[0x1],extended_id=True)
        logFrame01 = can.Message(arbitration_id=0x08f89540,data=[0x2],extended_id=True)
        logFrame02 = can.Message(arbitration_id=0x08f89540,data=[0x0],extended_id=True)

        logFrame1 = can.Message(arbitration_id=0x08f91540,data=[0x1],extended_id=True)
        logFrame11 = can.Message(arbitration_id=0x08f91540,data=[0x0],extended_id=True)
        logFrame12 = can.Message(arbitration_id=0x08f91540,data=[0x2],extended_id=True)
        #logFrame2 = can.Message(arbitration_id=0x08f99540,data=[0x2],extended_id=True)
        #logFrame3 = can.Message(arbitration_id=0x08fa1540,data=[0x0],extended_id=True)
        #bus.send(logFrame0)
        bus.send(logFrame01)
        #bus.send(logFrame02)
        #bus.send(logFrame1)
        #bus.send(logFrame12)
        #bus.send(logFrame11)
        #bus.send(logFrame2)
        #bus.send(logFrame3)
    	#print(count)
        #notifier = can.Notifier(bus, [can.Printer()])

except KeyboardInterrupt:
    # Catch keyboard interrupt
    print("\n\rKeyboard interrupt")
    exit()
