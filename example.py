import visa
#import usbtmc
rm = visa.ResourceManager('@py')
inst = rm.open_resource('USB0::0x0957::0x0407::SG44000971::INSTR')

inst.write("APPLy:SQUare 10000, 1, 0")
inst.write("FREQuency?\r")
print(inst.read_to_file('session','outputString.txt',10))
#query


#inst = usbtmc.Instrument(2391,1031)
#print(inst.ask("*IDN?"))
