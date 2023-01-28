import serial

#open up the ACM0 USB port because it's where the Feather is connected
port = serial.Serial('/dev/ttyACM1')
print(port.name) # check port name to make sure it's opened correctly

while 1:
    line = port.read(100) #read size of buffer
    print(line) #print response