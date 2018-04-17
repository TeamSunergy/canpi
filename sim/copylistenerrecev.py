#!/usr/bin/python3
from socket import *
import datetime
import json
import can
import os
import binascii
import interpret_CAN as interpret
import struct
import time
import base64
import faulthandler
import sys
import signal
import multiprocessing
import socket
import select
exitTime = multiprocessing.Value("B", False, lock=False)

def handleSIGINT(signum, frame):
    print("RECEIVED SIGINT!!!")

    exitTime.value = True
    print(dictionary)
    print("AGHHHHHHHHHHHHH!!!")
    exit()

def toDash(server_address, refresh_rate):
    signal.signal(signal.SIGINT, handleSIGINT)
    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise
    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Bind the socket to the port
    print ('starting up on %s' % server_address, file=sys.stderr)
    sock.bind(server_address)
    sock.setblocking(False)
    # Listen for incoming connections
    sock.listen(1)
    while not exitTime.value:
        # Wait for a connection
            print ('waiting for a connection',  file=sys.stderr)
            ready = select.select([sock], [], [], 5)[0]
            print(ready)
            if not ready:
                continue
            connection, client_address = sock.accept()
            connection.settimeout(1)
            try:
                print ('connection from', client_address,  file=sys.stderr)
                # Receive the data in small chunks and retransmit it
                while not exitTime.value:
                    #data = connection.recv(1024)
                    #print ('received "%s"' % data,  file=sys.stderr)
                    #if data:
                    #    print ('sending data back to the client',  file=sys.stderr)
                        # connection.sendall(data)
                    #    break
                    #else:
                    dict_data = json.dumps(dict(dictionary))
                    connection.sendall(dict_data.encode())
                    time.sleep(refresh_rate)
                        # print ('no more data from', client_address,  file=sys.stderr)
                        #break
            except:
                print("connection closed")

            finally:
                # Clean up the connection
                connection.close()

def echo_server(address, sleep_seconds):
    signal.signal(signal.SIGINT, handleSIGINT)
    sock = socket.socket(AF_INET, SOCK_STREAM)
    #sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print("Server started. Host: %s Port: %s " % (address[0],address[1]))
    #sock.setblocking(False)
    count = 0
    while not exitTime.value:
        #while True:
            #if count > 200:
            #    print("==--------------------------------------------------------------------------------------")
            #    time.sleep(2)
            #    print("==2-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            #    count = 100 / 0
            #count +=
        client, address = sock.accept()
        print('Connection from: ', address)
        #loop.create_task(echo_handler(client,sleep_seconds))
        multiprocessing.Process(target=echo_handler, args=(client, sleep_seconds)).start()
        time.sleep(1)

def echo_handler(client, sleep_seconds):
    signal.signal(signal.SIGINT, handleSIGINT)
    while not exitTime.value:
        #print(json.dumps(dictionary, indent = 4))
        print(dictionary)
        time.sleep(sleep_seconds)
        dict_data = json.dumps(dict(dictionary))

        client.sendall(dict_data.encode())
        print("Sent user JSON @", datetime.datetime.now())
        print("-=-=-=-=-==-=-==-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

def message():
    try:
        # Initalizes can bus
        bus = can.interface.Bus(channel=channel, bustype="socketcan_native")
        # Creates a device that can be used to get messages from the canbus
        buffRead = can.BufferedReader()
        # Creates a device that logs all canbus messages to a csv file
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

    initDictionary()
    while not exitTime.value:
        try:
            message = buffRead.get_message()
            #print("lolololololo")
            if (message is not None):
                newData = base64.b64encode(message.data) #This is a hack,
                newData = base64.b64decode(newData)      #convert byte array to bytes
                #print(hex(message.arbitration_id) + "||" + str(newData))
                lst = interpret.interpret(message.arbitration_id, newData)

                if (lst == ""):
                    print("255 sucks")
                    continue
                for x in lst:
                    m = None
                    if x[2] == "float":
                        m = struct.unpack('f', x[1].to_bytes(4, byteorder="little"))[0]
                    elif x[2] == "boolean":
                        if x[1] == 1:
                            m = True
                        else:
                            m = False
                    elif x[2] == "int":
                        m = x[1]
                    else:
                        raise RuntimeError("Unknown type received from interpret: " + x[2])
                    dictionary[x[0]] = m
                dictionary["netPower"] = dictionary["batteryPackCurrent"] * dictionary["batteryPackInstantaneousVoltage"]  #TODO - Compute net power
                dictionary["timeSent"] = str(datetime.datetime.now())
                time.sleep(0)
        except KeyboardInterrupt:
            # Closes the notifer which closes the Listeners as well
            notifier.stop()
            print("Keyboard interrupt")
            print(dictionary)
            exit()

def initDictionary():
    dictionary["bpsHighVoltage"] = 0.0
    dictionary["bpsLowVoltage"] = 0.0
    dictionary["packAmpHours"] = 0.0
    dictionary["packTotalCycles"] = int(0)
    dictionary["packHealth"] = int(0)
    dictionary["highestCellTemperature"] = int(0)
    dictionary["lowestCellTemperature"] = int(0)
    dictionary["averageCellTemperature"] = int(0)
    dictionary["internalBPSTemperature"] = int(0)
    dictionary["batteryPackCurrent"] = 0.0
    dictionary["batteryPackInstantaneousVoltage"] = 0.0
    dictionary["batteryPackSummedVoltage"] = 0.0
    dictionary["motConSerialNumber"] = 0
    dictionary["motConTritiumID"] = int(0)
    dictionary["motConReceiveErrorCount"] = int(0)
    dictionary["motConTransmitErrorCount"] = int(0)
    dictionary["motConActiveMotor"] = int(0)
    dictionary["motConErrorMotorOverSpeed"] = False
    dictionary["motConErrorDesaturation"] = False
    dictionary["motConErrorUVLO"] = False
    dictionary["motConErrorConfigReadError"] = False
    dictionary["motConErrorWatchdog"] = False
    dictionary["motConErrorBadMotorPosition"] = False
    dictionary["motConErrorDCBusOverVoltage"] = False
    dictionary["motConErrorSoftwareOverCurrent"] = False
    dictionary["motConLimitTemperature"] = False
    dictionary["motConLimitBusVoltageLower"] = False
    dictionary["motConLimitBusVoltageUpper"] = False
    dictionary["motConLimitCurrent"] = False
    dictionary["motConLimitVelocity"] = False
    dictionary["motConLimitMotorCurrent"] = False
    dictionary["motConLimitOutputVoltagePWM"] = False
    dictionary["motConBusCurrent"] = 0.0
    dictionary["motConBusVoltage"] = 0.0
    dictionary["motConVehicleVelocity"] = 0.0
    dictionary["motConMotorVelocity"] = 0.0
    dictionary["motConPhaseCCurrent"] = 0.0
    dictionary["motConPhaseBCurrent"] = 0.0
    dictionary["motConVd"] = 0.0
    dictionary["motConVq"] = 0.0
    dictionary["motConId"] = 0.0
    dictionary["motConIq"] = 0.0
    dictionary["motConBEMFd"] = 0.0
    dictionary["motConBEMFq"] = 0.0
    dictionary["motConFifteenVSupply"] = 0.0
    dictionary["motConThreePointThreeVSupply"] = 0.0
    dictionary["motConOnePointNineVSupply"] = 0.0
    dictionary["motConHeatSinkTemp"] = 0.0
    dictionary["motConMotorTemp"] = 0.0
    dictionary["motConDSPBoardTemp"] = 0.0
    dictionary["motConDCBusAmpHours"] = 0.0
    dictionary["motConOdometer"] = 0.0
    dictionary["motConSlipSpeed"] = 0.0
    dictionary["InvalidCanMessage"] = int(0)
    dictionary["netPower"] = 0.0


signal.signal(signal.SIGINT, handleSIGINT)

#faulthandler.enable()
# network settings
channel = "vcan0"
#bitrate = 128000  # 128000 if useing can0
manager = multiprocessing.Manager()
dictionary = manager.dict()
print(str(dict(dictionary)))
print("CAN RECV test")

jobs = []
#while True:
print("==1")
#loop = asyncio.get_event_loop()
p = multiprocessing.Process(target=message)
jobs.append(p)
p.start()
print("==2")
p = multiprocessing.Process(target=echo_server, args=(('0.0.0.0',25000), 0.2))
jobs.append(p)
p.start()
p = multiprocessing.Process(target=toDash, args=("/tmp/mySocket", 0.5))
jobs.append(p)
p.start()
print("==3")
#loop.run_in_executor(None, echo_server(('0.0.0.0',25000),loop,.2))
#print("==4" + asyncio.all_tasks())
#time.sleep(5)
print("==5")
i = 0
while True:
    #time.sleep(1)
    if i % 100000 == 0:
    	print(jobs)
    i += 1
    time.sleep(1)
