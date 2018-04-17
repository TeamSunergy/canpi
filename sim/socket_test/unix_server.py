# unix_server.py
# https://docs.python.org/2/library/socket.html
# Unix Sockets example Server
import socket
import os
import sys

server_address = "/tmp/mySocket"
def main():
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

    # Listen for incoming connections
    sock.listen(1)
    while True:
        # Wait for a connection
            print ('waiting for a connection',  file=sys.stderr)
            connection, client_address = sock.accept()
            try:
                print ('connection from', client_address,  file=sys.stderr)
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    print ('received "%s"' % data,  file=sys.stderr)
                    if data:
                        print ('sending data back to the client',  file=sys.stderr)
                        connection.sendall(data)
                    else:
                        print ('no more data from', client_address,  file=sys.stderr)
                        break

            finally:
                # Clean up the connection
                connection.close()
main()
