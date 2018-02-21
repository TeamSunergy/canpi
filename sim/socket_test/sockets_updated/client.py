import socket


class Client:
    def __init__(self, host='127.0.0.1', port=25000):
        self.host = host
        self.port = port
        self.s = socket.socket()

    def connect(self):
        self.s.connect((self.host, self.port))
        while True:

            data = self.s.recv(1024)
            if not data:
                break
            print(data.decode())

    def __str__(self):
        return "Host: %s Port %s" % (self.host, self.port)

    def close(self):
        self.s.close()


def main():
    try:
        display = Client()
        print(display.__str__())
        display.connect()
    except ConnectionRefusedError as e:
        print ("%s \nErrorNo:[%s] \n%s" %
               ("Connection Refused Error", e.errno, "Solution: Ensure the server is listening"))

if __name__ == '__main__':
    main()