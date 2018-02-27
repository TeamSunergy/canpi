#!/usr/bin/python3
# RECV.py

import can
import time
import datetime
import os
import csv
import binascii

# network settings
channel = "vcan0"
bitrate = 128000

print("\n\rCAN RECV test")

try:
	bus = can.interface.Bus(channel=channel, bustype="socketcan_native")

except OSError:
	print("Cannot find PiCAN board.")
	exit()

now = datetime.datetime.now()
logger = csv.writer(open(datetime.datetime.now().strftime("%Y%m%d%H%M") + ".csv", "w"), delimiter=",",
	quotechar="|", quoting=csv.QUOTE_MINIMAL)

logger.writerow(["timestamp"] + ["arbitration id"] + ["extended"] + ["remote"] + ["error"]
	+ ["dlc"] + ["data"])

print("Ready")

try:
	while True:
		message = bus.recv()
		logger.writerow([message.timestamp] + [message.arbitration_id]
			+ [message.is_extended_id] + [message.is_remote_frame]
			+ [message.is_error_frame] + [message.dlc]
			+[message.data.hex()])
			#[binascii.hexlify(message.data).decode("utf8")])
		#time = message.timestamp

	#message.timestamp == float
	#message.is_remote_frame == bool (if message is a remote frame or a data frame)
	#message.extended_id == bool (if true arbitration id is 29 bits otherwise 11 bits)
	#message.is_error_frame == bool
	#message.arbitration_id = int 11 or 29 bits (extended)
	#message.dlc = int (message length between 0 and 8)
	#message.data = bytearray (a byte arrry containing the can bus message number of bytes is equal to dlc)
	#message.__str__() == string (string representation of message timestamp, arbitration_id,
	#	flags, dlc, data)
		#aid = message.arbitration_id
        #for i in range(message.dlc ):
        #    s += '{0:x}'.format(message.data[i])
        #
        #print(' {}'.format(c + s))
		print(message.data.hex())

except KeyboardInterrupt:
	print("\n\rKeyboard interrupt")
