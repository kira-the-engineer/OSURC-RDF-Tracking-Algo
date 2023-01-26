import serial

#open up the ACM0 USB port because it's where the Feather is connected
port = serial.Serial('/dev/ttyACM0')
print(port.name) # check port name to make sure it's opened correctly

while 1:
    line = port.read(100) #read size of buffer
    final = line.decode("utf-8")
    print(final) #print response