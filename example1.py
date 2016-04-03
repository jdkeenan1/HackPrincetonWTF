#!/usr/bin/env python
import redis
import glob
import time
import serial

#from boto.s3.connection import S3Connection

#currentBucket = conn.get_bucket('hackprincetonee')
#from boto.s3.key import Key

glist = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') + glob.glob('/dev/tty.u*')
listBaud = [110,300,600,1200,2400,4800,9600,19200,115200]
print glist[0]
for i in listBaud:
	ser = serial.Serial(glist[0], i, timeout=2.0)
	ser.write("APPLy:SQUare 10, 1, 0")
	ser.write('*IDN?\r')
	ser.write('*IDN?\r')
	print(ser.readline())
