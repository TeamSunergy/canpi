#!/usr/bin/python3
from socket import *
import datetime
import json
import asyncio
import can
import os
import binascii
import interpret_CAN as interpret
import struct
import time
import base64
import faulthandler
async def echo_server(address, loop, sleep_seconds):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print("Server started. Host: %s Port: %s " % (address[0],address[1]))
    sock.setblocking(False)
    while True:
        client, address = await loop.sock_accept(sock)
        print('Connection from: ', address)
        loop.create_task(echo_handler(client,sleep_seconds))

async def echo_handler(client, sleep_seconds):
    while True:
        #print(json.dumps(dictionary, indent = 4))
        await asyncio.sleep(sleep_seconds)
        dict_data = json.dumps(dictionary)
        await loop.sock_sendall(client,dict_data.encode())
        print("Sent user JSON @", datetime.datetime.now())

def message():
    count = 0;
    initDictionary()
    while True:
        try:
            message = buffRead.get_message()
            if (message is not None):
                count += 1
                print(count)
                newData = base64.b64encode(message.data) #This is a hack,
                newData = base64.b64decode(newData)      #convert byte array to bytes
                print(hex(message.arbitration_id) + "||" + str(newData))
                lst = interpret.interpret(message.arbitration_id, newData)
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

if __name__ == '__main__':
    faulthandler.enable()
    # network settings
    channel = "vcan0"
    #bitrate = 128000  # 128000 if useing can0
    dictionary = {}
    print("CAN RECV test")

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
    
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, message)
    loop.run_until_complete(echo_server(('192.168.0.116',25000),loop,.2))
