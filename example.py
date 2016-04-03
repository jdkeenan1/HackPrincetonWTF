import visa
import time
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)
#import usbtmc
rm = visa.ResourceManager('@py')
inst = rm.open_resource('USB0::0x0957::0x0407::SG44000971::INSTR')
for i in xrange(0,5):
	inst.write("APPLy:SQUare 20000, 1, 0")
	time.sleep(1)
	time.sleep(.5)
	inst.write("APPLy?")
	time.sleep(.5)
	print(inst.read())
	inst.write("*RST")
	time.sleep(1)
	inst.write("APPLy:SQUare 10000, 1, 0")
	time.sleep(1)
inst.close()
rm.close()
