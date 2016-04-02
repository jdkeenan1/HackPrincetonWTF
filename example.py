import visa
rm = visa.ResourceManager('@py')
inst = rm.open_resource('USB0::0x0957::0x0407::SG44000971::INSTR')
inst.write("APPLy:SQUare 10000, 1, 0")
#query
