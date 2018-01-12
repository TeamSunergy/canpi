# VIRTUAL SEND.py

#!/usr/sbin/python3.5
import time
import can
import os


print('\n\rVCAN SEND test')
print('Bring up vcan0...')
os.system("sudo modprobe vcan")
os.system("sudo ip link add dev vcan0 type vcan")
os.system("sudo ip link set vcan0 up")
time.sleep(0.1)

def producer(id):	
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan_native')
    for i in range(10):
        print('Sending message ' + str(i))
        msg = can.Message(arbitration_id=0xc0ffee, data=[id,0,1,2,3,4,5], extended_id=False)
        bus.send(msg)
    print('Done.\n')
    
    #Need to keep running to ensure the writing threads stay alive (?)
    time.sleep(1)

producer(10)

