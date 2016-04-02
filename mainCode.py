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
command = ['AUTORange','?'] 
isquery = 0
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
#'?'-all settings, 'FUNCtion HBArs/OFF/VBArs' - can add ':DELTA/:POSITION/:UNIts?'
# <value> should start with a space unless '?'
def cursor():
	s = 'CURSor:' + command[1] + command[2] + '\r'
	ser.write(s)
#get waveform data, command = ['curve',{' <Block>',' <asc curve','?'}]
def curve():
	s = 'CURVe' + command[1] + '\r'
	ser.write(s)
#display settings, command = ['display',<option>,<value>]
#'?', 'BRIGHTness <num>', CONTRast <num>, FORMat XY/YT, INVert ON/OFF, STYle DOTs/VECtors
#<value< should start with a space unless '?'
def display():
	s = 'DISplay:' + command[1] + command[2] + '\r'
	ser.write(s)
#harmonics settings and analysis, command = ['harmonics',<option>,<value>]
#'?', ENABle ON/OFF, SELect <num>, SHOW ALL/ODD/EVEN, SOUrce CH<x>
#query only: FREquency, HRMS, PERCent, PHAse, RMS, THDF
#<value> should start with a space unless '?'
def harmonics():
	s = 'HARmonics:' + command[1] + command[2] + '\r'
	ser.write(s)
#horizontal settings (assumes main), command = ['horizontal',<option>,<value>]
#'?', POSition <num>, SCAle <num>, VIEW MAIn/WINDOW/ZONE
#<value> should start with a space unless '?'
def horizontal():
	s = 'HORizontal:' + command[1] + command[2] + '\r'
	ser.write(s)
#measurements, command = ['measurement',<meas numb>,<option>,<value>]
#<meas numb> specifies the measurement 1 through 5
#'?',SOUrce CH<y>, TYPE FREQuency/MEAN/PERIod/PK2pk/CRMs/MINImum/MAXImum/RISe/FALL/PWIdth/NWIdth/NONe
#query only: UNIts, VALue
#<value> should start with a space unless '?'
def measurements():
	s = 'MEASUrement:MEAS' + command[1] +':' + command[2] + '\r'
	ser.write(s)

switcher = {
	'copy': copy,
	'AUTORange': AUTORange,
	'AUTOSet': AUTOSet,
	'CH': CH,
	'cursor': cursor,
	'curve': curve,
	'display': display,
	'harmonics': harmonics,
	'horizontal': horizontal,
	'measurement': measurement
}
func = switcher.get(command[0], lambda: "not valid")
func()

if isquery:
	result = ser.readline()
	isquery = 0

#change scale
#ser.write('CH1:SCAle 10e-2\r')
