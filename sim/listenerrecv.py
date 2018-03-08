#!/usr/bin/python3
# RECV.py

import can
import time
import datetime
import os
import csv
import binascii
import interpret_CAN as test

def convertDictionary(dictionary):
	return

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
	print("Cannot find PiCAN board.")
	exit()



print("Ready")

dictionary = {}

try:
	while True:
		message = buffRead.get_message()
  #Old example message atributes are still the same
  #logger.writerow([message.timestamp] + [message.arbitration_id]
  # + [message.is_extended_id] + [message.is_remote_frame]
  # + [message.is_error_frame] + [message.dlc]
  # +[message.data.hex()])

  #If buffered Read times out it returns an object of NoneType
  # otherwise it returns a message with above attributes

		if (message is not None):
			newData = "".join(map(chr,message.data))
			lst = test.interpret(message.arbitration_id,newData)
			print(lst)
			print(message)
			for x in lst:
				dictionary[x[0]] = x[1]

except KeyboardInterrupt:
	# Closes the notifer which closes the Listeners as well
	notifier.stop()
	print("Keyboard interrupt")
	print(dictionary)
