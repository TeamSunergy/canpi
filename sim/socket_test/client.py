# https://docs.python.org/2/library/socket.html
# Socket module provides access to the BSD socket interface
import socket


def main():
    host = '127.0.0.1'
    port = 5120

    s = socket.socket()
    s.connect((host, port))

    message = raw_input("Enter Input -> ")

    while message != 'q':
        s.send(message)
        data = s.recv(1024)
        print("Received from Server: %s" % data)
        message = raw_input("Enter Input -> ")
    s.close()
if __name__ == '__main__':
    main()
