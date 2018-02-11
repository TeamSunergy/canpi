# https://docs.python.org/2/library/socket.html
# Socket module provides access to the BSD socket interface
import socket


def main():
    host = '127.0.0.1'
    port = 5120

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    conn, address = s.accept()
    print ("Connection from: %s" % str(address))
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        print ("From client: %s" % str(data))
        data = str(data).upper()
        conn.send(data)
        print("Sending: %s" % str(data))

if __name__ == '__main__':
    main()
    
