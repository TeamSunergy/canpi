import csv
import time
import datetime
import os

# This only makes a new file every minute, and otherwise overwrites the same file.
logger = csv.writer(open('./log/' + datetime.datetime.now().strftime("%Y%m%d%H%M") + ".csv", "w"), delimiter=",",
	quotechar="|", quoting=csv.QUOTE_MINIMAL)

logger.writerow(["dataName"] + ["data"])

data = {'bpsInfo':0, 'arrayInfo':1, 'motorInfo':2 }
print(data)

def log_data():
    for key in data:
	       logger.writerow([key] + [data[key]])


log_data()
