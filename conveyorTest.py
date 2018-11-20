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

# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()

# Create a new main directory
expDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
expPath = "data/" + expDateTime + "/"
os.makedirs(expPath)

phidgets.startModbus()
phidgets.set_csFileName(expPath + "conveyor_0.txt")

#########################
# 4 - Start the conveyors
print "Start the conveyors"
thread_c = Thread(target=phidgets.runConveyors, args=(1,180,2,180))
thread_c.start()

time.sleep(5)

#########################
# 7 - Stop the conveyors
print "Stop conveyors"
phidgets.stopConveyors()

