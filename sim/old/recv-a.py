import time
import subprocess
import can
import csv
# Setup VCAN
#subprocess.call(['modprobe vcan'])
# Create a vcan network interface with a specific name
#subprocess.call(['ip link add dev vcan0 type vcan'])
#subprocess.call(['ip link set vcan0 up'])

#can.rc('socketcan', 'vcan0', 128000)
#bus = can.interface.Bus('socketcan', 'vcan0', 128000)
bustype = 'socketcan_native'
channel = 'can0'
#bus = can.interface.Bus('vcan0', bustype='virtual')

class everything():

	def __init__(self):

		self.spamwriter = csv.writer(open("telemetry.csv", "w"), delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL)

	def getMessage(self):
		bus = can.interface.Bus(channel=channel, bustype=bustype)
		message = bus.recv()
		#self.spamwriter.writerow(message)
		#self.spamwriter.writerow([message.timestamp, message.arbitration_id, str(message.is_extended_frame_format), message.is_error_frame, message.dlc, message.data])
		return(message.timestamp)


thisThing = everything()

while (True):
	print(thisThing.getMessage())
