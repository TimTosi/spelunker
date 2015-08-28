"""@package helperfunc

This file contains debug functions.
"""
import os

def log(message):
	"""Writes a message into the log file.

	@param message String containing the message to write.
	"""
	if os.path.isfile("../log/log.txt") != True:
		print "Log file is missing."
		return False
	with open("../log/log.txt", 'w') as logFile:
		logFile.write(message)