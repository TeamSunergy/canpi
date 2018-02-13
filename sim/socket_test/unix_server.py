# unix_server.py
# https://docs.python.org/2/library/socket.html
# Unix Sockets example Server
import socket
import os

socketFile = "/tmp/mySocket"
def main():

    if os.path.exists(socketFile):
        os.remove(socketFile)

    s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    s.bind(socketFile)

    while 1:
        data = s.recv(1024)
        if not data:
            break
        data = data.decode("utf-8")
        #s.send(data.encode("utf-8"))
        print("From client: " + data)

    s.close()
    os.remove(socketFile)
    print("Done")
if __name__ == '__main__':
    main()
