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
#import pynmea2
import serial
import RPi.GPIO as gpio
import smbus

#import cProfile
#import pstats
#import io

def GPIOHelper(pinNum):
	prev = dictionary["gpio" + str(pinNum)]
	curr = gpio.input(pinNum)
	if prev != curr:
		dictionary["gpio" + str(pinNum)] = curr

# GPIO
# Reads the voltage from the GPIO pins and puts
#  their state (high = 1 and low = 0) into the dictionary.
def GPIO():
    dictionary["gpio5"] = gpio.input(5)
    dictionary["gpio6"] = gpio.input(6)
    dictionary["gpio12"] = gpio.input(12)
    dictionary["gpio13"] = gpio.input(13)
    dictionary["gpio19"] = gpio.input(19)
    dictionary["gpio26"] = gpio.input(26)

    while True: #TODO: Change this to use pin change interupts instead of polling
        GPIOHelper(5)
        GPIOHelper(6)
        GPIOHelper(12)
        GPIOHelper(13)
        GPIOHelper(19)
        GPIOHelper(26)

# toDash
# Sends the dictionary to the Dash UI.
#
def toDash(server_address, refresh_rate):
    try:
                os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise
    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Bind the socket to the port
    print('starting up on %s' % server_address, file=sys.stderr)
    sock.bind(server_address)
    sock.setblocking(False)
    # Listen for incoming connections
    sock.listen(1)
    while True:
        # Wait for a connection
        print('waiting for a connection',  file=sys.stderr)
        ready = select.select([sock], [], [], 5)[0]
        if not ready:
            continue
        connection, client_address = sock.accept()
        try:
            print('connection from', server_address,
                  file=sys.stderr)  # server_address is hacky
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

# gpsStuff
# Reads the position from the GPS receiver and
#  puts it into the dictionary.
def gpsStuff(server_address):
    while not os.path.exists(server_address):
        time.sleep(1)
    # If it errors out here make sure the GPS is plugged in.
    ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=5)
    # for i in range(5):
    ser.readline()
    map = {"N": 1, "S": -1, "E": 1, "W": -1}

    while True:
        try:
            data = pynmea2.parse(
                ser.readline().decode("ascii", errors='replace'))
        except:
            continue
        if str(data).startswith("$GPRMC") and data.data[2] != "" and data.data[4] != "":
            lat = float(data.data[2])
            lon = float(data.data[4])
            lat = map[data.data[3]] * \
                (lat // 10**2 + (lat - (lat // 10**2) * 100) / 60)
            lon = map[data.data[5]] * \
                (lon // 10**2 + (lon - (lon // 10**2) * 100) / 60)
            print(str(lat) + " " + str(lon))
            dictionary["coordinates"] = (lat, lon)
        elif str(data).startswith("$GPGST") and data.data[6] != "" and data.data[7] != "" and data.data[8] != "":
            latPrecision = float(data.data[6])
            lonPrecision = float(data.data[7])
            heightPrecision = float(data.data[8])
            print(str(latPrecision) + " " +
                  str(lonPrecision) + " " + str(heightPrecision))
            dictionary["coordinatesPrecision"] = (
                latPrecision, lonPrecision, heightPrecision)
        ser.close()

# echo_server
# Waits for a client to connect. When one does
#  spawn an echo_handler process for it.
def echo_server(address, sleep_seconds):
    sock = socket.socket(AF_INET, SOCK_STREAM)
    #sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.settimeout(5)
    sock.listen(3)
    print("Server started. Host: %s Port: %s " % (address[0], address[1]))
    # sock.setblocking(False)
    count = 0
    while True:
        try:
            client, address = sock.accept()
        except:
            continue
        print('Connection from: ', address)
        multiprocessing.Process(target=echo_handler, args=(
            client, sleep_seconds)).start()
        time.sleep(1)

# echo_handler
# Sends the client the dictionary every so many seconds.
#
def echo_handler(client, sleep_seconds):
    while True:
        print(dictionary)
        time.sleep(sleep_seconds)
        dict_data = json.dumps(dict(dictionary))

        client.sendall(dict_data.encode())
        print("Sent user JSON @", datetime.datetime.now())
        print("-=-=-=-=-==-=-==-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

# message
# Reads messages from the CAN bus, lets the c module
#  interpret them, then puts them into the dictionary.
def message():
    try:
        # Initalizes can bus
        bus = can.interface.Bus(channel=channel, bustype="socketcan_native")
        # Creates a device that can be used to get messages from the canbus
        buffRead = can.BufferedReader()
        # Creates a device that logs all canbus messages to a csv file
        # NOTE: encodes data in base64
        logger = can.CSVWriter("log.csv")
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
            newData = base64.b64encode(message.data)  # This is a hack,
            newData = base64.b64decode(newData)  # convert byte array to bytes.
            lst = interpret.interpret(message.arbitration_id, newData)

            if (lst == ""):
                continue
            for x in lst:
                m = None
                if x[2] == "float":
                    m = struct.unpack('f', x[1].to_bytes(
                        4, byteorder="little"))[0]
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
            dictionary["netPower"] = dictionary["batteryPackCurrent"] * dictionary["batteryPackInstantaneousVoltage"]  # TODO - Compute net power
            dictionary["timeSent"] = str(datetime.datetime.now())
    # Closes the notifer which closes the Listeners as well
    notifier.stop()

# log_data
# Log the dictionary data to CSV
# Takes in the current state of the dictionary as an arguemnt (data),
# prints a header to the file, and then a row for each dictionary key.
def log_data():
	while True:
		data = dict(dictionary)
		current_date = datetime.datetime.now()
		logger = csv.writer(open('./log/' + current_date.strftime("%b_%d_%Y_%H:%M:%S") + ".csv", "w"), delimiter=",",
			quotechar="|", quoting=csv.QUOTE_MINIMAL)

		# Log Header
		logger.writerow(["# APPTEL LOG"])
		logger.writerow(["# Device: CANPi"])
		logger.writerow(["# Date: " + current_date.strftime("%b %d %Y %r")])
		logger.writerow("#")
		logger.writerow(["data_name"] + ["value"])

		# Log each variable name and value as a row
		for key in data:
		       logger.writerow([key] + [data[key]])


# initDictionary
# Initialize the dictionary so clients
#  don't error out when a value has not been
#  put in yet.
def initDictionary():
    dictionary["bpsHighVoltage"] = 0.0
    dictionary["bpsLowVoltage"] = 0.0
    dictionary["packAmpHours"] = 0.0
    dictionary["packTotalCycles"] = 0
    dictionary["packHealth"] = 0
    dictionary["highestCellTemperature"] = 0
    dictionary["lowestCellTemperature"] = 0
    dictionary["averageCellTemperature"] = 0
    dictionary["internalBPSTemperature"] = 0
    dictionary["batteryPackCurrent"] = 0.0
    dictionary["batteryPackInstantaneousVoltage"] = 0.0
    dictionary["batteryPackSummedVoltage"] = 0.0
    dictionary["motConSerialNumber"] = 0
    dictionary["motConTritiumID"] = 0
    dictionary["motConReceiveErrorCount"] = 0
    dictionary["motConTransmitErrorCount"] = 0
    dictionary["motConActiveMotor"] = 0
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
    dictionary["InvalidCanMessage"] = 0
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
    dictionary["mpptTotalNetPower"] = 0.0
    dictionary["timeSent"] = 0.0
    dictionary["coordinates"] = (0.0, 0.0)
    dictionary["coordinatesPrecision"] = (0.0, 0.0, 0.0)
    dictionary["gpio5"] = 0
    dictionary["gpio6"] = 0
    dictionary["gpio12"] = 0
    dictionary["gpio13"] = 0
    dictionary["gpio19"] = 0
    dictionary["gpio26"] = 0
    dictionary["GPIORestarted"] = None
    dictionary["messageRestarted"] = None
    dictionary["echo_serverRestarted"] = None
    dictionary["toDashRestarted"] = None
    dictionary["gpsStuffRestarted"] = None

def spawnProcess(target, args, daemon):
    if args == None:
        process = multiprocessing.Process(target=eval(target))
    else:
        process = multiprocessing.Process(target=eval(target), args=args)

    process.daemon = daemon
    process.start()
    return process

def restartProcess(process, target, args, daemon):
    process.terminate()
    process.join()
    process = spawnProcess(target, args, daemon)
    dictionary[target + "Restarted"] = datetime.datetime.now()
    return process

#Set up GPIO
gpio.setmode(gpio.BCM)
gpio.setup(5, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(6, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(12, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(13, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(19, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_DOWN)

# network settings
channel = "can1"
# bitrate = 125000  # 125000 if using can0
server_address = "/tmp/mySocket"

# Set up multiprocessing and the dictionary
manager = multiprocessing.Manager()
dictionary = manager.dict()
initDictionary()
print(str(dict(dictionary)))

print("CAN RECV test")

try:
   # Spawn all of the processes

    print("GPIOProcess")
    GPIOProcess = spawnProcess("GPIO",None,True)

    print("messageProcess")
    messageProcess = spawnProcess("message",None,True)

    print("echoProcess")
    echoProcess = spawnProcess("echo_server",(('0.0.0.0', 25000), 0.5), False) # daemonized processes can't spawn child processes

    print("toDashProcess")
    toDashProcess = spawnProcess("toDash",(server_address, 0.5),True)

    #print("gpsStuffProcess")
    # The comma needs to be in the argument. If it is not, then Python will think it is not a tuple and instead complain that there are too many arguments.  #mySocket is still in /tmp even after the program closes. Is that correct behavior?
    #gpsStuffProcess = spawnProcess("gpsStuff",(server_address,),True)

    print("logDataProcess")
    logDataProcess = spawnProcess("log_data", None, True)


    # If a process dies, then respawn it.
    while True:

        if not GPIOProcess.is_alive():
            GPIOProcess = restartProcess(GPIOProcess,"GPIO",None,True)

        if not messageProcess.is_alive():
            messageProcess = restartProcess(messageProcess,"message",None,True)

        if not echoProcess.is_alive():
            echoProcess = restartProcess(echoProcess,"echo_server",(('0.0.0.0', 25000), 0.5), False)

        if not toDashProcess.is_alive():
            toDashProcess = restartProcess(toDashProcess,"toDash",(server_address, 0.5),True)

       # if not gpsStuffProcess.is_alive():
       #     gpsStuffProcess = restartProcess(gpsStuffProcess,"gpsStuff",(server_address,),True)

		if not gpsStuffProcess.is_alive():
            gpsStuffProcess = restartProcess(gpsStuffProcess,"gpsStuff",(server_address,),True)

        time.sleep(.1)

except KeyboardInterrupt:
    print("Keyboard interrupt")
    #print(dict(dictionary))
    # pr.disable()
    echoProcess.terminate()
    echoProcess.join()
    # s = io.StringIO()
    # ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    # ps.print_stats()
    # print(s.getvalue())
    print()
    exit()
