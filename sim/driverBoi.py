#!/usr/bin/env python3
import subprocess
import multiprocessing
import signal
import sys

def handler(signum, frame):
    print("HEEEEELLLLLLLOOOOOO  " + str(signum))
    os.killpg(0, signal.SIGINT)
    print("HELLO2.0")
    sys.exit()

processes = {}

signal.signal(signal.SIGINT, handler)


proc  = subprocess.Popen(["python3", "copylistenerrecev.py"])

#processes["listenerrecv"] = proc.pid

proc.wait()
print("Wazzup")


