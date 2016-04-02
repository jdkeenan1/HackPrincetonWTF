#!/usr/bin/env python

# Something in lines of http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# Make sure you have IMAP enabled in your gmail settings.
# Right now it won't download same file name twice even if their contents are different.
import random 
import glob
import email
import getpass, imaplib
import os
import serial
glist = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
ser = serial.Serial(glist[0], 9600)
f = open('/home/pi/currentDEVICESET', 'r') 
DEVICE = f.read()
f.close()
import sys
import time
from boto import dynamodb2
from boto.dynamodb2.table import Table
from boto.s3.connection import S3Connection

TABLE_NAME = ""
REGION = "us-west-2"
conn = dynamodb2.connect_to_region(
	REGION,
	aws_access_key_id='AKIAICN44BGVRGEMGI3Q',
	aws_secret_access_key='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')

table = Table('aecdevice', connection=conn)
try:
	item = table.get_item(deviceName=DEVICE)
	print item
except:
	item = False
testfunction = True
while (item):
	print "yes, We have a match"
	timeStep = 0.005;
	item = table.get_item(deviceName=DEVICE)
	s = ser.readline()
	s = ser.readline()

	batteryNumber = int(item['Data']['BatteryPercentage']/20)
	if testfunction:
		battery = item['Data']['BatteryPercentage']
		testfunction = False
	print batteryNumber
	ser.write(str(batteryNumber))
	# we have a print
	# now we need to retrieve and download that print along with upadte that user that his print is currently being printed
	incomingFrequency = float(s.split(',')[0])
	incomingFrequency = (incomingFrequency-60.0)/35.0+60.0
	item['Data']['Frequency'] = incomingFrequency
	incomingSolarPower = int(s.split(',')[1])
	incomingSolarPower = (incomingSolarPower-37)/20*100/8
	if (incomingSolarPower < 0):
		incomingSolarPower = 0;
	
	if (incomingSolarPower > 100):
		incomingSolarPower = 100
	incomingSolarPower = incomingSolarPower
	battery = float(battery) + float(timeStep)*float(incomingSolarPower)/100;
	item['Data']['Intensity'] = incomingSolarPower
	appliance1 = int(s.split(',')[2])
	if (appliance1 == 1):
		battery = battery - (1.0*timeStep)
	
	item['Data']['Button1'] = appliance1
	appliance2 = int(s.split(',')[3])
	if (appliance2 == 1):
		battery = battery - (3.0*timeStep)
	
	item['Data']['Button2'] = appliance2
	print incomingFrequency
	if (incomingFrequency > 60.5):
		#we need to take power
		item['Data']['Grid'] = int(-3.3)
	else:
		if (incomingFrequency < 59.5):
			#supply Power
			item['Data']['Grid'] = int(3.3)
		else:
			item['Data']['Grid'] = 0
	print item['Data']['Grid']
	print battery
	battery = float(battery) + (-1*float(item['Data']['Grid']) * timeStep)
	print battery
	item['Data']['BatteryPercentage'] = round(battery,0)
	if battery > 100.0:
		item['Data']['BatteryPercentage'] = 100.0
		battery = 100.0
	
	item['Data']['Frequency'] = round(item['Data']['Frequency']*10,0)
	print item['Data']['Frequency']
	print item['Data']['Grid']
	print item['Data']['BatteryPercentage']
	item.save(overwrite=True)
	time.sleep(.5)
	ser.flushInput()
	
	# here we grab from the s3 bucket
	# conns3 = S3Connection('AKIAICN44BGVRGEMGI3Q', 'ugchXirJEneSZA0xfSFRCqUeLUZr7yERGTNkUEY0')
	# print item['queue'][0]
	# fileName = ''
	# emailAddress = ''
	# for x in item['queue'][0]:
	# 	print x
	# 	if (x[-1:] == 'l' or x[-1:] == 'L' or x[-1:] == 'e' or x[-1:] == 'E'):
	# 		fileName = x
	# 	elif (x[-1:] == 'm' or x[-1:] == 'u'):
	# 		emailAddress = x
	# print emailAddress, fileName		
			
	# for bucket in conns3.get_all_buckets():
	# 	#here we grab the file from the item queue
	# 	if (bucket.name == 'mobiumsprinter'):
	# 		filePath = '/'+PRINTER+'/prints/' + fileName
	# 		filePut = '/home/pi/Mobiumsv0.3RaspUltimaker/Prints/' + fileName
	# 		key = bucket.get_key(filePath)
	# 		print key
	# 		key.get_contents_to_filename(filePut)
	# # here we update the users account
	# tableuser = Table('mobiums', connection=conn)
	# itemUser = tableuser.get_item(
	# 		userID=emailAddress)
	# # we need to update the user by decresing the inQueue and increasing the printed.
	# #print itemUser['prints']
	# itemUser['prints']['inQueue'] = itemUser['prints']['inQueue'] - 1
	# itemUser['prints']['inProgress'] = itemUser['prints']['inProgress'] + 1
	# #print itemUser['prints']['inQueue'], itemUser['prints']['inProgress'] 
	# itemUser.save(overwrite=True)
	# # we can also send a notification to it's social data base here.
	# tablesocial = Table('mobiumssocial', connection=conn)
	# itemSocial = tablesocial.get_item(
	# 		userID=emailAddress)
	# notification = 'Print Started for ' + PRINTER
	# print itemSocial['notificationList'] 
	# try:
	# 	itemSocial['notificationList'] = itemSocial['notificationList'].append(notification)
	# except:
	# 	itemSocial['notificationList'] = [notification]
	# itemSocial['notifications'] = itemSocial['notifications'] + 1
	# itemSocial.save(overwrite=True)
	# f = open('/home/pi/Mobiumsv0.3RaspUltimaker/currentPrintFile', 'w')
	# f.write(fileName)
	# f.close()

	# here we email the user
	#still under dev.
	# var from = 'admin@mobiumsolutions.com';
  
#   var to1 = userID;
#   var body = "Your printer has indicated that it has started to print your file. Your file should be completed in approximately " + item.queue.L[0].SS[2] + " minutes. We'll notify you when it's ready for pickup!";
#   var subject = "New print has started on " + 'mobiumSolutions';
#   var mailOptions1 = {
#     to: to1,
#     from: from,
#     subject: subject,
#     text: body
#   };
#   transporter.sendMail(mailOptions1, function(err) {
#       # we emailed the user!
#   });
