#!/usr/bin/env python
import redis
import glob
import serial
import json
glist = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') + glob.glob('/dev/tty.u*')
oScope = serial.Serial(glist[0], 9600)
import visa
rm = visa.ResourceManager('@py')
funcGen = rm.open_resource('USB0::0x0957::0x0407::SG44000971::INSTR')

r = redis.StrictRedis(host='104.236.205.31',port=6379,db=0)
r.publish("boss",json.dumps("boss", "hello"))
