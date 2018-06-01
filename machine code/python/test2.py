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

####################
# INIT
####################

# Init the stepper motor
phidgets.initStepper()

# Create a new main directory
expDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
expPath = "data/" + expDateTime + "/"
os.makedirs(expPath)
 
####################
# RUN THE EXPERIMENT
####################

####################
# 1 - Move the stepper motor (Wait for the motor to reach its fianl position)
print "Move the stepper"
phidgets.moveStepper(20000)

####################
# 2 - Start laser #0
print "Start laser 0"
# Setup the filename to save the current data
laser0.set_fileName(expPath + "data0.xyz")
# Create a thread for the laser
thread_l = Thread(target=laser0.grabAndSave, args=())
# Start the thread
thread_l.start()

####################
# 2.1 - Start load cells
phidgets.set_lc0FileName(expPath + "lc0_s0.txt")
phidgets.set_lc1FileName(expPath + "lc1_s0.txt")

thread_lc = Thread(target=phidgets.loadCells, args=())
thread_lc.start()

#######################
# 3 - Start the rollers
print "Start the rollers"
#phidgets.runMotors(-1, 0.6)
thread_r = Thread(target=phidgets.runMotorsLoop, args=(-1,80,))
thread_r.start()

#########################
# 4 - Start the conveyors
print "Start the conveyors"
phidgets.runConveyor_0(0,80)
phidgets.runConveyor_1(1,80)

#########################
# WAIT !!!!!!!!!!!
# Data acquisition
time.sleep(15)
print "End of acquisition 1"

#########################
# 5 - Stop laser #0
print "Stop laser"
laser0.stopAcquisition()

#########################
# 5.1 - Stop load cells
phidgets.stopLoadCells()

#########################
# 6 - Stop the rollers
print "Stop motors"
#phidgets.stopMotors()
phidgets.stopMotorsLoop()

#########################
# 7 - Stop the conveyors
print "Stop conveyors"
phidgets.stopConveyor_0()
phidgets.stopConveyor_1()

#########################
# Change direction !!!!!!!!!!!!!
time.sleep(1)
print "Change direction"
#########################

#########################
# 1 - Move the stepper motor
phidgets.moveStepper(0)

#########################
# 2 - Start laser #1
laser1.set_fileName(expPath + "data1.xyz")
thread_l = Thread(target=laser1.grabAndSave, args=())
thread_l.start()

####################
# 2.1 - Start load cells
phidgets.set_lc0FileName(expPath + "lc0_s1.txt")
phidgets.set_lc1FileName(expPath + "lc1_s1.txt")

thread_lc = Thread(target=phidgets.loadCells, args=())
thread_lc.start()

#########################
# 3 - Start the rollers

thread_r = Thread(target=phidgets.runMotorsLoop, args=(1,80,))
thread_r.start()

#########################
# 4 - Start the conveyors
phidgets.runConveyor_0(1,80)
phidgets.runConveyor_1(0,80)

#########################
# WAIT !!!!!!!!!!!
# Data acquisition
time.sleep(15)

#########################
# 5 - Stop laser #1
laser1.stopAcquisition()

#########################
# 5.1 - Stop load cells
phidgets.stopLoadCells()

#########################
# 6 - Stop the rollers
#phidgets.stopMotors()
phidgets.stopMotorsLoop()

#########################
# 7 - Stop the conveyors
phidgets.stopConveyor_0()
phidgets.stopConveyor_1()


