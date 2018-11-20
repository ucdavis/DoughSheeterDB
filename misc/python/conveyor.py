# Give the path to find the python wrapper
import sys
sys.path.append('phidgetsClass/')
sys.path.append('laserClass/')

# Import modules
from threading import Thread
import time

# Import the wrapped API
import phidgetsClass_ext
import laserClass_ext

# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()

phidgets.runConveyor_0(1,100)
phidgets.runConveyor_1(1,100)

time.sleep(15)

phidgets.stopConveyor_0()
phidgets.stopConveyor_1()
