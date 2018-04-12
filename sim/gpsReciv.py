#!/usr/bin/env python3
import pynmea2
import serial

#fileName = "/dev/ttyUSB0"
#stream = open(fileName)
#message = None
ser =  serial.Serial('/dev/ttyUSB0', 4800, timeout=5)
for i in range(10):
    ser.readline()

while True:
    data = pynmea2.parse(ser.readline().decode("ascii", errors='replace'))
    if str(data).startswith("$GPRMC"):
    	print(data.fields[2][1] + " " + data.data[3] + data.data[2][:3])
        print(data.fields[4][1] + " " + data.data[5] + data.data[4][:3])
ser.close()
