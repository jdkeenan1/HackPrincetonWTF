#!/usr/bin/env python

# Something in lines of http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# Make sure you have IMAP enabled in your gmail settings.
# Right now it won't download same file name twice even if their contents are different.
# import random 
import glob
# import email
# import getpass, imaplib
# import os
import serial
import visa
rm = visa.ResourceManager('@py')
inst = rm.open_resource('USB0::0x0957::0x0407::SG44000971::INSTR')
#query
#case statement
#command = ['AUTORange','?'] #get from lambda function
#example of applying a command
outputString = []

def applyFunction():
	outputString = ['APPLy']
	
	def SINusoid():
		outputString.append(':SINusoid')
	def SQUare():
		outputString.append(':SQUare')
	def RAMP():
		outputString.append(':RAMP')
	def PULSe():
		outputString.append(':PULSe')
	def NOISe():
		outputString.append(':NOISe')
	def DC():
		outputString.append(':DC')
	def USER():
		outputString.append(':USER')
	switcher1 = {
		'sin': SINusoid,
		'square': SQUare,
		'ramp': RAMP,
		'pulse': PULSe,
		'noise': NOISe,
		'dc': DC,
		'user': USER
	}
	func1 = switcher1.get(command[1], lambda: "not valid")
	func1()
	for i, item in enumerate(command):
		if i > 1:
			outputString.append(" "+item+",")
	output = ''.join(outputString)
	print output
	inst.write(output)
while 1:
	var = raw_input("Please enter something: ")
	command = var.split()
	switcher = {
		'apply': applyFunction
		#'AUTORange': AUTORange,
		#'AUTOSet': AUTOSet,
		#'CH': CH,
		#'cursor': cursor
	}
	func = switcher.get(command[0], lambda: "not valid")
	func()

#result = ser.readline()
#change scale
#ser.write('CH1:SCAle 10e-2\r')
