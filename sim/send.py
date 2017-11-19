#!/usr/sbin/python3.5
import subprocess
import can
# Setup VCAN
#subprocess.call(['modprobe vcan'])
# Create a vcan network interface with a specific name
#subprocess.call(['ip link add dev vcan0 type vcan'])
#subprocess.call(['ip link set vcan0 up'])

#can.rc('socketcan', 'vcan0', 128000)
#bus = can.interface.Bus('socketcan', 'vcan0', 128000)
bus = can.interface.Bus('vcan0', bustype='virtual')

# Send Messages
msg = can.Message(arbitration_id=0xc0ffee,
	data=[0, 25, 0, 1, 3, 1, 4, 1],
	extended_id=False)

try:
	bus.send(msg)
	print("Message sent on {}".format(bus.channel_info))
except can.CanError:
	print("ERROR")
