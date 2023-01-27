"""
Tracking algorithm code for the 2022-2023 Mars Rover RDF Capstone Project
Author: K. Kopcho
Date Revised: 1/25/2023

"""

import gps
import math
import numpy
import serial

#below code adapted from the GPSD Example python client. Checks if lat/long of base are finite and then saves them as floats
#print statements are for bug testing- in actuality these coordinates will get sent over PyQt to the groundstation

session = gps.gps(mode=gps.WATCH_ENABLE) #connect to the gps daemon
port = serial.Serial('/dev/ttyACM0') #open up the ACM0 USB port because it's where the Feather is connected

#the following function is based on the equations found here: https://www.movable-type.co.uk/scripts/latlong.html
def forward_bearing(base_lat, base_long, rover_lat, rover_long): 
    diff_long = (rover_long - base_long)

    #convert to radians before doing calculations
    base_lat = math.radians(base_lat)
    base_long = math.radians(base_long)
    rover_lat = math.radians(rover_lat)
    rover_long = math.radians(rover_long)
    diff_long = math.radians(diff_long)

    #do the actual math now, again this is based on the equations on the moveable-type site
    y = math.sin(diff_long) * math.cos(rover_lat)
    x = math.cos(base_lat) * math.sin(rover_lat) - math.sin(base_lat) * math.cos(rover_lat) * math.cos(diff_long)
    theta = numpy.atan2(y, x)
    bearing = (theta * 180/numpy.pi + 360) % 360 #gets degrees from 0 to 360

    return bearing

def base_read():
        if ((gps.isfinite(session.fix.latitude) and
             gps.isfinite(session.fix.longitude))): #makes sure we have a finite lat/lon
        
            #save lat/long as floats
            blat = session.fix.latitude
            blon = session.fix.longitude
        else:
            #set error values
            blat = -1;
            blon = -1;

        return blat, blon

def rover_read():
    line = port.read(100) #read size of buffer

#start try/catch for keyboard interrupt (ctrl-c)
try:
    while 1:
        if session.read() == 0:
                if not (gps.MODE_SET & session.valid): #ensure we have a TPV Packet from read
                    continue
    
        b_lat, b_lon = base_read() #get values from the base gps
        if(b_lat == -1 and b_lon == -1): #if we're not connected or lat/lon isn't finite
            print(" Lat n/a Lon n/a")
        else:
            print("base lat: %.6f, base lon: %.6f" % (b_lat, b_lon))

              
except KeyboardInterrupt:
    # got a ^C.  Say bye, bye
    print('')

# Got ^C, or fell out of the loop.  Cleanup, and leave.
session.close()
exit(0)