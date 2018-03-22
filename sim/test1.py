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

def message():
    while True:
        try:
            message = buffRead.get_message()
            if (message is not None):

                newData = base64.b64encode(message.data)
                newData = base64.b64decode(newData)

                lst = interpret.interpret(message.arbitration_id, newData)
                for x in lst:
                    m = None
                    if x[2] == "float":
                        m = struct.unpack('f', x[1].to_bytes(4, byteorder="little"))
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

                dictionary["timeSent"] = str(datetime.datetime.now())

        except KeyboardInterrupt:
            # Closes the notifer which closes the Listeners as well
            notifier.stop()
            print("Keyboard interrupt")
            print(dictionary)
            exit()

if __name__ == '__main__':
    # network settings
    channel = "vcan0"
    bitrate = 128000  # 128000 if useing can0
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

    message()
