# RECV.py

import can
import time
import os

print('\n\rCAN RECV test')
print('Bring up can0...')
os.system("sudo ip link set can0 up type can bitrate 500000")
time.sleep(0.1)

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

except OSError:
    print('Cannot find PiCAN board.')
    exit()

print('Ready')

try:
    while True:
        message = bus.recv()
        c = '{0:f} {1:x} {2:x}'.format(message.timestamp, message.arbitration_id, message.dlc)
        s = ''
        for i in range(message.dlc ):
            s += '{0:x}'.format(message.data[i])

        print(' {}'.format(c + s))

except KeyboardInterrupt:
    os.system("sudo ip link set can0 down")
    print('\n\rKeyboard interrupt')

