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


async def echo_server(address, loop, sleep_seconds):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print("Server started. Host: %s Port: %s " % (address[0],address[1]))
    # client is a new socket object usable to send and receive data on the connection,
    # address is the address bound to the socket on the other end of the connection
    sock.setblocking(False)
    while True:
        client, address = await loop.sock_accept(sock)
        print('Connection from: ', address)
        loop.create_task(echo_handler(client,loop,sleep_seconds))


async def echo_handler(client, loop, sleep_seconds):
    while True: 
        await asyncio.sleep(sleep_seconds)
        await loop.sock_sendall(client,json.dumps(dictionary).encode())
        print("Sent user JSON @", datetime.datetime.now())

def message():
    count = 0;
    while True:
        try:
            message = buffRead.get_message()
            if (message is not None):
                newData = "".join(map(chr, message.data))
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
                count = count + 1
                print(count)
                dictionary["timeSent"] = str(datetime.datetime.now())
                #print(dictionary)
                #time.sleep(.1)
        except KeyboardInterrupt:
            # Closes the notifer which closes the Listeners as well
            notifier.stop()
            print("Keyboard interrupt")
            #print(dictionary)

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
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, message)
    loop.run_until_complete(echo_server(('192.168.0.116',25010), loop, 2))



