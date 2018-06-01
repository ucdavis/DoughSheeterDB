# Give the path to find the python wrapper
import sys
sys.path.append('phidgetsClass/')
sys.path.append('laserClass/')

from datetime import datetime
from threading import Thread
import time
import os

# Import the wrapped API
import phidgetsClass_ext
import laserClass_ext

# Create a new directory
expDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
expPath = "data/" + expDateTime + "/"
os.makedirs(expPath)

# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()
time.sleep(1)
phidgets.set_lc0FileName(expPath + "lc0.txt")
phidgets.set_lc1FileName(expPath + "lc1.txt")
thread_lc = Thread(target=phidgets.loadCells, args=())
thread_lc.start()
time.sleep(2)
phidgets.stopLoadCells()
