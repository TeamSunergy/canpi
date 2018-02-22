# asyncio-recv.py

import can
import asyncio
import concurrent.futures
import time
import datetime
import os
import csv
import binascii
channel = "vcan0"
bitrate = 128000
""" Recives and logs data from canbus.

Recives data and uses Asyncio to handle logging asynchronous
also uses concurrent.futres to make logging concurrent
"""

class canPI:

	def __init__(self, channel = "vcan0", bitrate = 128000):
		self.channel = channel
		self.bitrate = bitrate
		# generates a pool of a a maximum of three proccesses to handle any
		# jobs that need to be run.
		self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3,)
		self.eventloop = asyncio.get_event_loop()

		print("\n\rCAN RECV test")
		print("Bring up " + channel + "...")

		if (channel == "can0"):
			os.system("sudo ip link set " + self.channel + " up type can bitrate " + str(self.bitrate)
			+ " restart-ms 100")

		else:
			os.system("sudo modprobe vcan")
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

#		self.eventloop.run_until_complete(self.getMessage())
		self.eventloop.close()


	def writeLog(self, message):
		self.logger.writerow([message.timestamp] + [message.arbitration_id]
			+ [message.is_extended_id] + [message.is_remote_frame]
			+ [message.is_error_frame] + [message.dlc]
			+ [message.data.hex()])

	async def getMessage(self):
		self.message = self.bus.recv()
		if (self.message is not None):
			job = self.eventloop.run_in_executor(self.executor, self.writeLog, self.message)
			self.eventloop.run_until_complete(job)
		self.printMessage()

	def printMessage(self):
		print(self.message.data.hex())

	def destroy(self):
		self.job.close
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

except KeyboardInterrupt:
	test.destroy()
