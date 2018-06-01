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
# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()

####################
# INIT
####################

 
####################
# RUN THE EXPERIMENT
####################









#########################
# 4 - Start the conveyors
print "Start the conveyors"
phidgets.runConveyors(0,160,1,160)

#########################
# WAIT !!!!!!!!!!!
# Data acquisition
time.sleep(2)





#########################
# 7 - Stop the conveyors
print "Stop conveyors"
phidgets.stopConveyors()

#########################
# Change direction !!!!!!!!!!!!!
time.sleep(1)
print "Change direction"
#########################







