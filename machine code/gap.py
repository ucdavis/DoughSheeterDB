# Give the path to find the python wrapper
import sys
sys.path.append('phidgetsClass/')
sys.path.append('laserClass/')

# Import modules
from threading import Thread
from datetime import datetime
import time
import os
import signal
import sys

# Import the wrapped API
import phidgetsClass_ext
import laserClass_ext

#######################################
# To manage interruption
#######################################
def signal_handler(signal, frame):
        print('Stop the system!')
        phidgets.stopLoadCells()
        phidgets.stopMotorsLoop()
	phidgets.stopConveyors()
	phidgets.stopStepper()
	laser0.stopAcquisition()
	laser1.stopAcquisition()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()
results = phidgets.initConnection()
if results > 0:
	phidgets.cleanConnection()
	sys.exit(0)

# Init the stepper motor
phidgets.initStepper()

#print "Move the stepper"
phidgets.moveStepper(24)

time.sleep(1)

phidgets.moveStepper(18)

#time.sleep(3)

#phidgets.moveStepper(14)

#time.sleep(3)

#phidgets.moveStepper(16)

#time.sleep(3)

#phidgets.moveStepper(18)

#time.sleep(3)

#phidgets.moveStepper(20)

#time.sleep(1)
