# VIRTUAL RECV.py

import can
import time
import os

print('\n\rVCAN RECV test')
print('Bring up vcan1...')
os.system("sudo modprobe vcan")
os.system("sudo ip link add dev vcan1 type vcan")
os.system("sudo ip link set vcan1 up")
time.sleep(0.1)

try:
    bus = can.interface.Bus(channel='vcan1', bustype='socketcan_native')

except OSError:
    print('Cannot find PiCAN board.')
    exit()

print('Ready.')

try:
    while True:
        print('Receiving...')
        message = bus.recv(1.0)
        if message is None:
            print('Timeout: no message')
            exit()
        c = '{0:f} {1:x} {2:x}'.format(message.timestamp, message.arbitration_id, message.dlc)
        s = ''
        for i in range(message.dlc ):
            s += '{0:x}'.format(message.data[i])

        print('MSG: {}'.format(c + s))

except KeyboardInterrupt:
    os.system("sudo ip link set vcan1 down")
    print('\n\rKeyboard interrupt')

