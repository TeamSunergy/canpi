#!/usr/bin/python3
# RECV.py

import can
import os
import binascii
import interpret_CAN as interpret
import struct

# network settings
channel = "vcan0"
bitrate = 128000 # 128000 if useing can0

print("CAN RECV test")

try:
 	#Initalizes can bus
	bus = can.interface.Bus(channel=channel, bustype="socketcan_native")
	#Creates a device that can be used to get messages from the canbus
	buffRead = can.BufferedReader()
	#Creates a device that logs all canbus messages to a csv file
	# NOTE: encodes data in base64
	logger = can.CSVWriter("test.csv")
	"""
	Creates a notifier object which accepts an array of objects of the can.Listener class
	Whenever it receves a message from bus it calls the Listeners in the array
	and lets them handle the message.
	"""
	notifier = can.Notifier(bus, [buffRead, logger], timeout=1)
except OSError:
	print("Interface " + channel + " Down.")
	exit()



print("Ready")

dictionary = {}

try:
	while True:
		message = buffRead.get_message()
		# message attributes
		# ([message.timestamp] + [message.arbitration_id]
		# + [message.is_extended_id] + [message.is_remote_frame]
		# + [message.is_error_frame] + [message.dlc]
		# +[message.data.hex()])
		#
		#If buffered Read times out it returns an object of NoneType
		# otherwise it returns a message with above attributes

		if (message is not None):
			newData = "".join(map(chr,message.data))
			lst = interpret.interpret(message.arbitration_id,newData)
			for x in lst:
				m = None
				if x[2] == "float":
					m = struct.unpack('f', x[1].to_bytes(4, byteorder="little"))
				elif  x[2] == "boolean":
					if x[1] == 1:
						m = True
					else:
						m = False
				elif x [2] == "int":
					m = x[1]
				else:
					raise RuntimeError("Unknown type received from interpret: " + x[2])
				dictionary[x[0]] = m
		print(dictionary)
except KeyboardInterrupt:
	# Closes the notifer which closes the Listeners as well
	notifier.stop()
	print("Keyboard interrupt")
	print(dictionary)
