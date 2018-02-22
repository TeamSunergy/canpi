#!/usr/sbin/python3.5
import time
import subprocess
import can
# Setup VCAN
#subprocess.call(['modprobe vcan'])
# Create a vcan network interface with a specific name
#subprocess.call(['ip link add dev vcan0 type vcan'])
#subprocess.call(['ip link set vcan0 up'])

#can.rc('socketcan', 'vcan0', 128000)
#bus = can.interface.Bus('socketcan', 'vcan0', 128000)
bustype = 'socketcan_native'
channel = 'vcan0'
#bus = can.interface.Bus('vcan0', bustype='virtual')

def sendMessage(size, id, message = "deadbeef"):
	bus = can.interface.Bus(channel=channel, bustype=bustype)
	output = bytearray.fromhex(message)
	size = size - len(message)
	#message += "0"*size
	print(size)
	print(output)
#    output = [12, 1, 1, 1, 1, 1, 1, 1]
	msg = can.Message(arbitration_id=0x00000020, data=output, extended_id=False)
	bus.send(msg)
	time.sleep(1)

class orion:
	def __init__(self):
		interface = 'vcan0'

	#def getTemp(self, max, min):
	#	sendMessage(8, 



sendMessage(8, 0x10, "0000000000000000")

