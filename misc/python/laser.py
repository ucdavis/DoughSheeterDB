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

# Create a new main directory
expDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
expPath = "data/" + expDateTime + "/"
os.makedirs(expPath)

# Create the laser object
laser0=laserClass_ext.laserClass(0)
laser1=laserClass_ext.laserClass(1)

print "Start laser 0"
# Setup the filename to save the current data
laser1.set_fileName(expPath + "data1.xyz")
# Create a thread for the laser
thread_l = Thread(target=laser1.grabAndSave, args=())
# Start the thread
thread_l.start()

time.sleep(3)

# 5 - Stop laser #0
print "Stop laser"
laser1.stopAcquisition()
