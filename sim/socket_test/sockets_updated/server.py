from socket import *
from ex_json import json_ex
from datetime import datetime
import json
import asyncio


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
        json_ex["speed"] += 1
        json_ex["battery"] += 1
        await asyncio.sleep(sleep_seconds)
        await loop.sock_sendall(client,json.dumps(json_ex).encode())
        #print("Send user JSON @", datetime.now())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(echo_server(('127.0.0.1',25000), loop, 4))
