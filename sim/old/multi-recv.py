# RECV.py

import can
import multiprocessing
import time
import datetime
import os
import csv
import binascii
channel = "vcan0"
bitrate = 128000

class canPI:

	def __init__(self, channel = "vcan0", bitrate = 128000):
		self.channel = channel
		self.bitrate = bitrate

		print("\n\rCAN RECV test")
		print("Bring up " + channel + "...")

		if (channel == "can0"):
			os.system("sudo ip link set " + self.channel + " up type can bitrate " + str(self.bitrate)
			+ " restart-ms 100")

		else:
			os.system("modprobe vcan")
			os.system("sudo ip link add dev " + self.channel + " type vcan")
			os.system("sudo ip link set " + self.channel + " up type vcan")

		time.sleep(0.1)

		try:
			self.bus = can.interface.Bus(channel=self.channel, bustype="socketcan_native")

		except OSError:
			print("Cannot find PiCAN board.")
			exit()

		now = datetime.datetime.now()
		self.logger = csv.writer(open(datetime.datetime.now().strftime("%Y%m%d%H%M") + ".csv", "w"), delimiter=",",
			quotechar="|", quoting=csv.QUOTE_MINIMAL)

		self.logger.writerow(["timestamp"] + ["arbitration id"] + ["extended"] + ["remote"] + ["error"]
			+ ["dlc"] + ["data"])

		print("Ready")


	def writeLog(self):
		self.logger.writerow([self.message.timestamp] + [self.message.arbitration_id]
			+ [self.message.is_extended_id] + [self.message.is_remote_frame]
			+ [self.message.is_error_frame] + [self.message.dlc]
			+[self.message.data.hex()])

	def getMessage(self):
		self.message = self.bus.recv()
		job = multiprocessing.Process(target=self.writeLog)
		job.start()
		self.printMessage()

	def printMessage(self):
		print(self.message.data.hex())

	def destroy(self):
		os.system("sudo ip link set " + channel + " down")
		print("\n\rKeyboard interrupt")

# network settings


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
try:
	test = canPI(channel, bitrate)
	while True:
		test.getMessage()
		test.writeLog()

except KeyboardInterrupt:
	test.destroy()
