# https://docs.python.org/2/library/socket.html
# Unix Sockets example Client
import socket
import os

socketFile = "/tmp/mySocket"
def main():
    if os.path.exists(socketFile):
        c = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        c.connect(socketFile)

        message = input("Enter Input -> ")

        while True:
            c.send(message.encode("utf-8"))
            message = input("Enter Input -> ")
        c.close()
if __name__ == '__main__':
    main()
