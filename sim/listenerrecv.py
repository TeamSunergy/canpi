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
print("Bring up " + channel + "...")

#if (channel == "can0"):
#	os.system("sudo ip link set " + channel + " up type can bitrate " + str(bitrate) + " restart-ms 100")

#else:
#	os.system("modprobe vcan")
#	os.system("sudo ip link add dev " + channel + " type vcan")
#	os.system("sudo ip link set " + channel + " up type vcan")

time.sleep(0.1)

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

try:
	while True:
		message = buffRead.get_message()
		#Old example message atributes are still the same
		#logger.writerow([message.timestamp] + [message.arbitration_id]
		#	+ [message.is_extended_id] + [message.is_remote_frame]
		#	+ [message.is_error_frame] + [message.dlc]
		#	+[message.data.hex()])

		#If buffered Read times out it returns an object of NoneType
		# otherwise it returns a message with above attributes
		if (message is not None):
			print(message.timestamp)
		print(message)



except KeyboardInterrupt:
	#os.system("sudo ip link set " + channel + " down")
	#Closes the notifer which closes the Listeners as well
	notifier.stop()
	print("\n\rKeyboard interrupt")
