#!/usr/bin/python3
# RECV.py

import can
import os
import binascii
import interpret_CAN as interpret
import struct

import socketserver

from socket import *
from datetime import datetime
import json
import asyncio
import multiprocessing

# network settings
channel = "vcan0"
bitrate = 128000 # 128000 if useing can0
socketFile = "/tmp/mySocket"


async def echo_server(address, loop, sleep_seconds):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print("Server started. Host: %s Port: %s " % (address[0],address[1]))
    # client is a new socket object usable to send and receive data on the connection,
    # address is the address bound to the socket on the other end of the connection
    sock.setblocking(False)
    while True:
        client, address = await loop.sock_accept(sock)
        print('Connection from: ', address)
        loop.create_task(echo_handler(client,loop,sleep_seconds))


async def echo_handler(client, loop, sleep_seconds):
while True:
	socket2 = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
	socket2.connect("/tmp/mySocket")
	await asyncio.sleep(sleep_seconds)
	string = ""
	for line in socket2.makefile('r'):
		string += line
	await loop.sock_sendall(client,json.dumps(string).encode())
	#print("Send user JSON @", datetime.now())


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


if os.path.exists(socketFile):
	os.remove(socketFile)

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.bind(socketFile)

dictionary = {}
#dict = multiprocessing.Value("dict", "")

loop = asyncio.get_event_loop()
loop.run_until_complete(echo_server(('127.0.0.1',25000), loop, 4))

print("Ready")


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
			#dict.value = str(dictionary)
			print(dictionary)
			sock.sendall(str(dictionary).encode("utf-8"))
except KeyboardInterrupt:
	# Closes the notifer which closes the Listeners as well
	notifier.stop()
	print("Keyboard interrupt")
	print(dictionary)




