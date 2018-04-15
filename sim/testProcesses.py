import time
import signal
import sys

def handleSIGINT(signum, frame):
    print("Recieved a SIGINT")
    sys.exit()

signal.signal(signal.SIGINT, handleSIGINT)

print("Hello...")
time.sleep(4)
print("World")
