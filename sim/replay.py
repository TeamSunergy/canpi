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
channel = "can1"
bitrate = 125000

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
    #with open("2018-03-18 15:25:12.319795.csv", newline = "\n") as file:
    while True:
        count = 0
        with open("replayinput.csv", newline = "\n") as file:
            reader = csv.reader(file, delimiter = ",", quoting = csv.QUOTE_NONE)
            for row in reader:
                if row[1][0] != "0":
                    continue
                # [0x00, 0x95, 0x60, 0x64, 0x00, 0x0f, 0xef, 0x57]
                msg = can.Message(arbitration_id=int(row[1], 0),data=base64.b64decode(row[6]),extended_id=row[2] == 1, dlc=int(row[5]))
                bus.send(msg)
                count += 1
                if count % 200 == 0:
                    print(count)
                time.sleep(0.002)

except KeyboardInterrupt:
    # Catch keyboard interrupt
    print("\n\rKeyboard interrupt")
    exit()
