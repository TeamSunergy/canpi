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

def toDash(server_address, refresh_rate):
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
    while True:
        # Wait for a connection
        print ('waiting for a connection',  file=sys.stderr)
        ready = select.select([sock], [], [], 5)[0]
        print(ready)
        if not ready:
            continue
        connection, client_address = sock.accept()
        try:
            print ('connection from', server_address,  file=sys.stderr) # server_address is hacky
            # Receive the data in small chunks and retransmit it
            while True:
                connection.settimeout(5)
                dict_data = json.dumps(dict(dictionary))
                connection.sendall(dict_data.encode())
                time.sleep(refresh_rate)
        except:
            print("connection closed")

        finally:
            # Clean up the connection
            connection.close()
            os.unlink(server_address)

def echo_server(address, sleep_seconds):
    sock = socket.socket(AF_INET, SOCK_STREAM)
    #sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.settimeout(5)
    sock.listen(5)
    print("Server started. Host: %s Port: %s " % (address[0],address[1]))
    #sock.setblocking(False)
    count = 0
    while True:
        try:
            client, address = sock.accept()
        except:
            print("haha")
            continue
        print('Connection from: ', address)
        multiprocessing.Process(target=echo_handler, args=(client, sleep_seconds)).start()
        time.sleep(1)

def echo_handler(client, sleep_seconds):
    while True:
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
        
    while True:
        message = buffRead.get_message()
        if (message is not None):
            newData = base64.b64encode(message.data) #This is a hack,
            newData = base64.b64decode(newData)      #convert byte array to bytes
            lst = interpret.interpret(message.arbitration_id, newData)

            if (lst == ""):
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
    dictionary["mppt0ArrayVoltage"] = 0.0
    dictionary["mppt0ArrayCurrent"] = 0.0
    dictionary["mppt0BatteryVoltage"] = 0.0
    dictionary["mppt0UnitTemperature"] = 0.0
    dictionary["mppt1ArrayVoltage"] = 0.0
    dictionary["mppt1ArrayCurrent"] = 0.0
    dictionary["mppt1BatteryVoltage"] = 0.0
    dictionary["mppt1UnitTemperature"] = 0.0
    dictionary["mppt2ArrayVoltage"] = 0.0
    dictionary["mppt2ArrayCurrent"] = 0.0
    dictionary["mppt2BatteryVoltage"] = 0.0
    dictionary["mppt2UnitTemperature"] = 0.0
    dictionary["mppt3ArrayVoltage"] = 0.0
    dictionary["mppt3ArrayCurrent"] = 0.0
    dictionary["mppt3BatteryVoltage"] = 0.0
    dictionary["mppt3UnitTemperature"] = 0.0



# faulthandler.enable()
# network settings
channel = "vcan0"
# bitrate = 125000  # 125000 if using can0
manager = multiprocessing.Manager()
dictionary = manager.dict()

initDictionary()
print(str(dict(dictionary)))
print("CAN RECV test")

try:

    messageProcess = multiprocessing.Process(target=message)
    messageProcess.daemon = True
    messageProcess.start()

    echoProcess = multiprocessing.Process(target=echo_server, args=(('192.168.0.116',25000), 0.2))
    #echoProcess.daemon = True
    echoProcess.start()

    toDashProcess = multiprocessing.Process(target=toDash, args=("/tmp/mySocket", 0.5))
    toDashProcess.daemon = True
    toDashProcess.start()
    
    while True:
        if not messageProcess.is_alive():
            messageProcess.terminate()
            messageProcess.join()
            messageProcess = multiprocessing.Process(target=message)
            messageProcess.daemon = True
            messageProcess.start()
            print("Restarted messageProcess.")
        if not echoProcess.is_alive():
            echoProcess.terminate()
            echoProcess.join()
            echoProcess = multiprocessing.Process(target=echo_server, args=(('192.168.0.116',25000), 0.2))
            #echoProcess.daemon = True
            echoProcess.start()
            print("Restarted echoProcess.")
        if not toDashProcess.is_alive():
            toDashProcess.terminate()
            toDashProcess.join()
            toDashProcess = multiprocessing.Process(target=toDash, args=("/tmp/mySocket", 0.5))
            toDashProcess.daemon = True
            toDashProcess.start()
            print("Restarted toDashProcess.")
            
        time.sleep(.1)
        #print(str(dict(dictionary)))
	
except KeyboardInterrupt:
    # Closes the notifer which closes the Listeners as well
    #notifier.stop()
    print("Keyboard interrupt")
    #print(dict(dictionary))
    echoProcess.terminate()
    echoProcess.join()
    print()
    exit()
