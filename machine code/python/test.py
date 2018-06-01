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
#laser0=laserClass_ext.laserClass(0)
#laser1=laserClass_ext.laserClass(1)

# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()

####################
# INIT
####################

# Init the stepper motor
phidgets.initStepper()

time.sleep(1)

print "Move the stepper"
phidgets.moveStepper(40000)





