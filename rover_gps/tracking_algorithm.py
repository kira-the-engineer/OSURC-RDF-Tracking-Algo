"""
Tracking algorithm code for the 2022-2023 Mars Rover RDF Capstone Project
Author: K. Kopcho
Date Revised: 1/17/2023

"""

import gps
from math import radians, cos, sin, asin, sqrt, atan2, degrees

#below code adapted from the GPSD Example python client. Checks if lat/long of base are finite and then saves them as floats
#print statements are for bug testing- in actuality these coordinates will get sent over PyQt to the groundstation

session = gps.gps(mode=gps.WATCH_ENABLE) #connect to the gps daemon

#start try/catch for keyboard interrupt (ctrl-c)
try:
    while 1:
        if session.read() == 0:
                if not (gps.MODE_SET & session.valid): #ensure we have a TPV Packet from read
                    continue;
                
        if ((gps.isfinite(session.fix.latitude) and
             gps.isfinite(session.fix.longitude))): #makes sure we have a finite lat/lon
        
            #save lat/long as floats
            base_lat = session.fix.latitude
            base_lon = session.fix.longitude

            #print for debug purposes
            print(" Lat %.6f Lon %.6f" %
                  (base_lat, base_lon))
        else:
            print(" Lat n/a Lon n/a")
except KeyboardInterrupt:
    # got a ^C.  Say bye, bye
    print('')

# Got ^C, or fell out of the loop.  Cleanup, and leave.
session.close()
exit(0)