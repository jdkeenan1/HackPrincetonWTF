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
glist = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') + glob.glob('/dev/tty.u*')
ser = serial.Serial(glist[0], 9600)
#case statement
command = ['AUTORange','?'] #get from lambda function
#get copy of screen as BMP image, command = ['copy']
def copy():
	ser.write('HARDCopy STARt\r')
#turn on or off auto range, command = ['AUTORange',{' OFF',' ON','?'}]
def AUTORange():
	s = 'AUTORange:STATE' + command[1] + '\r'
	ser.write(s)
#AUTOSET to display a stable waveform, command = ['AUTOSet']
def AUTOSet():
	ser.write('AUTOSet EXECute\r')
#channel settings, command = ['CH',<numb>,<option>,<value>]
#'?'-all settings, 'BANdwidth ON/OFF', 'COUPling AC/DC/GND', 'INVert ON/OFF',
#'POSition <val>', 'SCALe <val>', 'YUNit "V"/"A"'
#<value> must have a space first unless '?'
def CH():
	s = 'CH' + command[1] + ':' + command[2] + command[3] + '\r'
	ser.write(s)
#cursor settings, command = ['cursor',<option>,<value>]
#'?'-all settings, 'FUNCtion HBArs/OFF/VBArs' - can add ':DELTA/:POSITION/:UNIts?', 

switcher = {
	'copy': copy,
	'AUTORange': AUTORange,
	'AUTOSet': AUTOSet,
	'CH': CH,
	'cursor': cursor
}
func = switcher.get(command[0], lambda: "not valid")
func()

#result = ser.readline()
#change scale
#ser.write('CH1:SCAle 10e-2\r')
