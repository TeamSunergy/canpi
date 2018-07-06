import csv
import time
import datetime
import os

def log_data(data):
	# This will create a new file based on the datetime. If the datetime is the same, it would overwrite
	# We can use this to our advantage if we want to create a new file every minute,
	# we should just take the seconds out of the filename format stringself.
	# We could keep the full datetime in the file header (which would be last write)

	current_date = datetime.datetime.now()
	logger = csv.writer(open('./log/' + current_date.strftime("%b_%d_%Y_%H:%M:%S") + ".csv", "w"), delimiter=",",
		quotechar="|", quoting=csv.QUOTE_MINIMAL)

	# Log Header
	logger.writerow(["# APPTEL LOG"])
	logger.writerow(["# Device: " + "CANPi"])
	logger.writerow(["# Date: " + current_date.strftime("%b %d %Y %r")])
	logger.writerow("#")
	logger.writerow(["data_name"] + ["value"])

	# Log each variable name and value as a row
	for key in data:
	       logger.writerow([key] + [data[key]])


data = {'bpsInfo':0, 'arrayInfo':1, 'motorInfo':2 }
log_data(data)
