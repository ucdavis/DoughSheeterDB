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
laser1=laserClass_ext.laserClass(1)

# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()


#######################
# 3 - Start the rollers
print "Start the rollers"
thread_r = Thread(target=phidgets.runMotorsLoop, args=(-1,80,))
thread_r.start()

#########################
# WAIT !!!!!!!!!!!
# Data acquisition
time.sleep(5)
print "End of acquisition 1"

#########################
# 6 - Stop the rollers
print "Stop motors"
phidgets.stopMotorsLoop()
