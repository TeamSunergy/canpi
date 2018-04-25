# https://docs.python.org/2/library/socket.html
# Unix Sockets example Client
import socket
import os
import sys

server_address = "/tmp/mySocket"
def main():
    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print ('connecting to %s' % server_address, file=sys.stderr)
    try:
        sock.connect(server_address)
    except socket.error as msg:
        print (msg)
        sys.exit(1)

    try:

        # Send data
        #message = b'This is the message.  It will be repeated.'
        #print ('sending "%s"' % message, file=sys.stderr)
        #sock.sendall(message)

        amount_received = 0
        #amount_expected = len(message)

        #while amount_received < amount_expected:
        while True:
            data = sock.recv(64)
            #amount_received += len(data)
            print ('received "%s"' % data)

    finally:
        #print ('closing socket', file=sys.stderr)
        sock.close()
        #pass

if __name__ == '__main__':
    main()
