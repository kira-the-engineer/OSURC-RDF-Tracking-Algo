"""
Tracking algorithm code for the 2022-2023 Mars Rover RDF Capstone Project
Author: K. Kopcho
Date Revised: 2/27/2023

"""

import gps
import math
import serial

class TrackingAlgorithm:


#define Class variables below here
    r_lat = -1;
    r_lon = -1;
    b_lat = -1;
    b_lon = -1;
    bearing = 0;    
    
#the following function is based on the equations found here: https://www.movable-type.co.uk/scripts/latlong.html
    def forward_bearing(self, base_lat, base_long, rover_lat, rover_long): 
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
        theta = math.atan2(y, x)
        fbearing = (theta * 180/math.pi + 360) % 360 #converts rads back to degrees from 0 to 360

        return fbearing

    #below code adapted from the GPSD Example python client. Checks if lat/long of base are finite and then saves them as floats
    def base_read(self, session):
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

    def rover_read(self, port):
        line = port.readline() #reads line ended by '\n'
        line = str(line.decode()) #converts line bytes into a string literal
        coords = line.split(',') #splits line data into a multiple index list using a delimiter
        lat = float(coords[0]) #save first index as latitude
        long = float(coords[1]) #save last index as longitude

        return lat, long

    def run_algo(self):
        session = gps.gps(mode=gps.WATCH_ENABLE) #connect to the gps daemon
        port = serial.Serial('/dev/ttyACM1') #open up the ACM USB port because it's where the Feather is connected
        try:
            while 1:
                if session.read() == 0:
                        if not (gps.MODE_SET & session.valid): #ensure we have a TPV Packet from read
                            continue
                            
                print("Base GPS Time %s" % session.fix.time)
            
                self.b_lat, self.b_lon = self.base_read(session) #get values from the base gps
                if(self.b_lat == -1 and self.b_lon == -1): #if we're not connected or lat/lon isn't finite
                    print(" Lat n/a Lon n/a")
                else:
                    print("base lat: %.6f, base lon: %.6f \n" % (self.b_lat, self.b_lon))
            
                self.r_lat, self.r_lon = self.rover_read(port)
                print("rover lat: %.6f, rover long %.6f \n" % (self.r_lat, self.r_lon))

                if(self.b_lat != -1 and self.b_lon != -1):
                    self.bearing = self.forward_bearing(self.b_lat, self.b_lon, self.r_lat, self.r_lon)
                    print("current bearing angle: %.1f degrees \n" % (self.bearing))
                else:
                    print("Cannot produce bearing angle, make sure GPS modules are getting a fix")

        except KeyboardInterrupt:
            print('')

        # Got ^C, or fell out of the loop.  Cleanup, and leave.
        session.close()
        exit(0)


def main():
    algo = TrackingAlgorithm()
    algo.run_algo()


if __name__ == "__main__":
    main()

