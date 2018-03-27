#!/usr/bin/python3
# Replay

import can
import time
import os
import csv
import binascii
import base64
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
    with open("2018-03-18 15:25:12.319795.csv", newline = "\n") as file:
        reader = csv.reader(file, delimiter = ",", quoting = csv.QUOTE_NONE)
        for row in reader:
            if row[1][0] != "0":
                continue
            print(row)
            # [0x00, 0x95, 0x60, 0x64, 0x00, 0x0f, 0xef, 0x57]
            msg = can.Message(arbitration_id=int(row[1], 0),data=base64.b64decode(row[6]),extended_id=False)
            bus.send(msg)
            count += 1
            print(count)

except KeyboardInterrupt:
    # Catch keyboard interrupt
    print("\n\rKeyboard interrupt")
    exit()
