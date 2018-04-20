#!/usr/bin/env python3
import pynmea2
import serial

ser =  serial.Serial('/dev/ttyUSB0', 4800, timeout=5)
for i in range(10):
    ser.readline()

map = {"N": 1, "S": -1, "E": 1, "W": -1}

while True:
    data = pynmea2.parse(ser.readline().decode("ascii", errors='replace'))
    if str(data).startswith("$GPRMC") and data.data[2] != "" and data.data[4] != "":
        print(data.data[2] + " " + data.data[4])
        lat = float(data.data[2])
        lon = float(data.data[4])
        print(data.fields[2][1] + " " + str(map[data.data[3]] * (lat // 10**2 + (lat - (lat // 10**2) * 100) / 60)))
        print(data.fields[4][1] + " " + str(map[data.data[5]] * (lon // 10**2 + (lon - (lon // 10**2) * 100) / 60)))
ser.close()
