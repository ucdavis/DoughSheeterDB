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

# To manage interruption
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        phidgets.stopMotorsLoop()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()
results = phidgets.initConnection()
if results > 0:
	phidgets.cleanConnection()
	sys.exit(0)

#######################
# 3 - Start the rollers
print "Start the rollers"
thread_r = Thread(target=phidgets.runMotorsLoop, args=(1,80,))
thread_r.start()

time.sleep(4)

#########################
# 6 - Stop the rollers
print "Stop motors"
phidgets.stopMotorsLoop()

time.sleep(1)
