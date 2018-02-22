# VIRTUAL RECV.py

import can
import time
import os

print('\n\rVCAN RECV test')
print('Bring up vcan0...')
os.system("sudo ip link set vcan0 up")
time.sleep(0.1)

try:
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan_native')

except OSError:
    print('Cannot find PiCAN board.')
    exit()

print('Ready.')

try:
    while True:
        print('Receiving...')
        message = bus.recv()
        if message is None:
            print('Timeout: no message')
        
        c = '{0:f} {1:x} {2:x}'.format(message.timestamp, message.arbitration_id, message.dlc)
        s = ''
        
        for i in range(message.dlc ):
            s += '{0:x}'.format(message.data[i])

        print('MSG: {}\n'.format(c + s))


except KeyboardInterrupt:
    os.system("sudo ip link set vcan0 down")
    print('\n\rKeyboard interrupt')

