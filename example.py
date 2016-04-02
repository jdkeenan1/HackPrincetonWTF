import visa
rm = visa.ResourceManager('@py')
rm.list_resources('/dev/ttyUSB0')
