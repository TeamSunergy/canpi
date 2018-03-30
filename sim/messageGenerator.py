#!/usr/bin/python3
# Replay

import can
import time
import os
import csv
import binascii
import base64
count = 0

# network settings
channel = "vcan0"
bitrate = 128000

#os.system("sudo /sbin/ip link set " + channel + " up type vcan")
print("Press CTRL-C to exit")

try:
    bus = can.interface.Bus(
            channel = channel,
            bustype = "socketcan_native")
except OSError:
    print("Interface " + channel + " is down.")
    exit()


# Main loop
try :
    #with open("2018-03-18 15:25:12.319795.csv", newline = "\n") as file:
    while True:
        with open("2018-03-18 13:57:22.211799.csv", newline = "\n") as file:
            reader = csv.reader(file, delimiter = ",", quoting = csv.QUOTE_NONE)
            for row in reader:
                if row[1][0] != "0":
                    continue
                # [0x00, 0x95, 0x60, 0x64, 0x00, 0x0f, 0xef, 0x57]
                msg = can.Message(arbitration_id=int(row[1], 0),data=base64.b64decode(row[6]),extended_id=row[2] == 1)
                bus.send(msg)
                count += 1
                print(count)

except KeyboardInterrupt:
    # Catch keyboard interrupt
    print("\n\rKeyboard interrupt")
    exit()
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

