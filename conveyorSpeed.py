# Give the path to find the python wrapper
import sys
sys.path.append('phidgetsClass/')
sys.path.append('laserClass/')

# Import modules
from threading import Thread
from datetime import datetime
import time
import os

# Import the wrapped API
import phidgetsClass_ext
import laserClass_ext

#######################################
# Create the lasers and phidgets objects
#######################################

# Create the laser object
laser0=laserClass_ext.laserClass(0)

# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()

# Create a new main directory
expDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
expPath = "data/" + expDateTime + "/"
os.makedirs(expPath)

####################
# 2 - Start laser #0
print "Start laser 0"
# Setup the filename to save the current data
laser0.set_fileName(expPath + "0_20.xyz")
# Setup the parameters to save the data
laser0.set_save()
# Create a thread for the laser
thread_l = Thread(target=laser0.grabAndSave, args=(0,))
# Start the thread
thread_l.start()

#########################
# 4 - Start the conveyors
print "Start the conveyors"
phidgets.runConveyors(0,60,0,0)

#########################
# WAIT !!!!!!!!!!!
# Data acquisition
while laser0.get_acquisition() == True:
        dumb =1
	#print("Acq {}".format(laser0.get_acquisition()))
#print("Acq out {}".format(laser0.get_acquisition()))
print "End of acquisition 1"

#########################
# 5 - Stop laser #0
print "Stop laser"
laser0.stopAcquisition()


#########################
# 7 - Stop the conveyors
print "Stop conveyors"
phidgets.stopConveyors()





