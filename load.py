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

#######################################
# Create the lasers and phidgets objects
#######################################


# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()
results = phidgets.initConnection()
if results > 0:
	phidgets.cleanConnection()
	sys.exit(0)




####################
# Log data
####################

# Create a new main directory to save data
expDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
expPath = "data/" + expDateTime + "/"
os.makedirs(expPath)


####################
# 2.1 - Start load cells
phidgets.set_lcFileName(expPath + "lc_0.txt")

thread_lc = Thread(target=phidgets.loadCells, args=())
thread_lc.start()

#########################
# Change direction !!!!!!!!!!!!!
time.sleep(0.5)

#########################

#########################
# 6 - Stop load cells
phidgets.stopLoadCells()




















