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

#authorize
import authorizeAndGetParameter

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

# Create the laser object
laser0=laserClass_ext.laserClass(0)
laser1=laserClass_ext.laserClass(1)

# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()
results = phidgets.initConnection()
if results > 0:
	phidgets.cleanConnection()
	sys.exit(0)

############################
# Start Modbus communication
############################

phidgets.startModbus()


####################
# Log data
####################

# Create a new main directory to save data
expDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
expPath = "data/" + expDateTime + "/"
os.makedirs(expPath)

# Log file
logPath = "data/" + expDateTime + "/log.txt"
f = open(logPath, 'w')
f.write('Log file: ' + expDateTime + '\n')

# Start the timestamp
start = time.time()


 
####################
# RUN THE EXPERIMENT
####################

####################
# 0 - Init the stepper motor
f.write(str(time.time() - start) + ': Initialization of the stepper motor\n')
phidgets.initStepper()
f.write(str(time.time() - start) + ': End of initialization of the stepper motor\n')


####################
# 1 - Move the stepper motor (Wait for the motor to reach its final position)
print "Move the stepper"
f.write(str(time.time() - start) + ': Change gap\n')
phidgets.moveStepper(rollerGapP1)
f.write(str(time.time() - start) + ': Gap changed\n')


####################
# 2 - Start laser
print "Start lasers"
# Setup the filename to save the current data
laser0.set_fileName(expPath + "outH_P1.csv")
laser1.set_fileName(expPath + "inH_P1.csv")
# Setup the parameters to save the data
laser0.set_save()
laser1.set_save()
# Create a thread for the laser
thread_l0 = Thread(target=laser0.grabAndSave, args=(0,))
thread_l1 = Thread(target=laser1.grabAndSave, args=(0,))
# Start the thread
thread_l0.start()
thread_l1.start()

####################
# 2.1 - Start load cells
phidgets.set_lcFileName(expPath + "VF.csv")

thread_lc = Thread(target=phidgets.loadCells, args=())
thread_lc.start()

#######################
# 3 - Start the rollers
print "Start the rollers"
phidgets.set_rsFileName(expPath + "rollers_0.txt")
#Movement in direction of Belt 11 to Belt 10
thread_r = Thread(target=phidgets.runMotorsLoop, args=(-1,rollerSpeedP1,))
thread_r.start()
f.write(str(time.time() - start) + ': Rollers started\n')

#########################
# 4 - Start the conveyors 
print "Start the conveyors"
phidgets.set_csFileName(expPath + "conveyor_0.txt")
# Direc 2,1 Movement from 11 to 10. 
# Arguments are Belt 0, Belt 1
thread_c = Thread(target=phidgets.runConveyors, args=(2,belt0P1,1,belt1P1))
thread_c.start()
f.write(str(time.time() - start) + ': Conveyors started\n')

#########################
# WAIT !!!!!!!!!!!
# Data acquisition
# Laser 0 is the output and stops automatically
while laser0.get_acquisition() == True:
	dumb = 1
print "End of acquisition 1"
# Laser is input and has to be stopped in the code
laser1.stopAcquisition()

if laser0.get_error() > 0:
	phidgets.cleanConnection()
        phidgets.stopLoadCells()
        phidgets.stopMotorsLoop()
	phidgets.stopConveyors()
	phidgets.stopStepper()
	sys.exit(0)
if laser1.get_error() > 0:
	phidgets.cleanConnection()
        phidgets.stopLoadCells()
        phidgets.stopMotorsLoop()
	phidgets.stopConveyors()
	phidgets.stopStepper()
	sys.exit(0)

#########################
# 5 - Stop the conveyors
print "Stop conveyors"
phidgets.stopConveyors()
f.write(str(time.time() - start) + ': Conveyors stopped\n')

#########################
# 6 - Stop load cells
#phidgets.stopLoadCells()

#########################
# 7 - Stop the rollers
print "Stop motors"
phidgets.stopMotorsLoop()
f.write(str(time.time() - start) + ': Rollers stopped\n')

#########################
# Change direction !!!!!!!!!!!!!
time.sleep(1)
print "Change direction"
#########################

#PASS 2

###################
# 1 - Move the stepper motor (Wait for the motor to reach its fianl position)
print "Move the stepper"
phidgets.moveStepper(rollerGapP2)

####################
# 2 - Start laser
print "Start laser"
# Setup the filename to save the current data
laser0.set_fileName(expPath + "inH_P2.csv")
laser1.set_fileName(expPath + "outH_P2.csv")
# Setup the parameters to save the data
laser0.set_save()
laser1.set_save()
# Create a thread for the laser
thread_l0 = Thread(target=laser0.grabAndSave, args=(0,))
thread_l1 = Thread(target=laser1.grabAndSave, args=(0,))
# Start the thread
thread_l0.start()
thread_l1.start()

####################
# 2.1 - Start load cells
#phidgets.set_lcFileName(expPath + "lc1.txt")

#thread_lc = Thread(target=phidgets.loadCells, args=())
#thread_lc.start()

#######################
# 3 - Start the rollers
print "Start the rollers"
phidgets.set_rsFileName(expPath + "rollers_1.txt")
thread_r = Thread(target=phidgets.runMotorsLoop, args=(1,rollerSpeedP2,))
thread_r.start()

#########################
# 4 - Start the conveyors
print "Start the conveyors"
phidgets.set_csFileName(expPath + "conveyor_1.txt")
# Direc 1,2 Movement from 10(In) to 11(Out). 
# Arguments are Belt 0, Belt 1
thread_c = Thread(target=phidgets.runConveyors, args=(1,belt0P2,2,belt1P2))
thread_c.start()


#########################
# WAIT !!!!!!!!!!!
# Data acquisition
#time.sleep(2)
# Laser 1 is the output and stops automatically
while laser1.get_acquisition() == True:
	dumb = 1
print "End of acquisition 2"
laser0.stopAcquisition()

if laser0.get_error() > 0:
	phidgets.cleanConnection()
        phidgets.stopLoadCells()
        phidgets.stopMotorsLoop()
	phidgets.stopConveyors()
	phidgets.stopStepper()
	sys.exit(0)
if laser1.get_error() > 0:
	phidgets.cleanConnection()
        phidgets.stopLoadCells()
        phidgets.stopMotorsLoop()
	phidgets.stopConveyors()
	phidgets.stopStepper()
	sys.exit(0)

#########################
# 5 - Stop the conveyors
print "Stop conveyors"
phidgets.stopConveyors()

#########################
# 6 - Stop load cells
#phidgets.stopLoadCells()

#########################
# 7 - Stop the rollers
print "Stop motors"
phidgets.stopMotorsLoop()
f.write(str(time.time() - start) + ': Rollers stopped\n')

#########################
# Change direction !!!!!!!!!!!!!
time.sleep(1)
print "Change direction"
#########################


#PASS 3

###################
# 1 - Move the stepper motor (Wait for the motor to reach its fianl position)
print "Move the stepper"
phidgets.moveStepper(rollerGapP3)

####################
# 2 - Start laser
print "Start laser"
# Setup the filename to save the current data
laser0.set_fileName(expPath + "outH_P3.csv")
laser1.set_fileName(expPath + "inH_P3.csv")
# Setup the parameters to save the data
laser0.set_save()
laser1.set_save()
# Create a thread for the laser
thread_l0 = Thread(target=laser0.grabAndSave, args=(0,))
thread_l1 = Thread(target=laser1.grabAndSave, args=(0,))
# Start the thread
thread_l0.start()
thread_l1.start()

####################
# 2.1 - Start load cells
#phidgets.set_lcFileName(expPath + "lc1P3.txt")

#thread_lc = Thread(target=phidgets.loadCells, args=())
#thread_lc.start()

#######################
# 3 - Start the rollers
print "Start the rollers"
phidgets.set_rsFileName(expPath + "rollers_1.txt")
thread_r = Thread(target=phidgets.runMotorsLoop, args=(-1,rollerSpeedP3,))
thread_r.start()

#########################
# 4 - Start the conveyors
print "Start the conveyors"
phidgets.set_csFileName(expPath + "conveyor_1.txt")
thread_c = Thread(target=phidgets.runConveyors, args=(2,belt0P3,1,belt1P3))
thread_c.start()


#########################
# WAIT !!!!!!!!!!!
# Data acquisition
#time.sleep(2)
while laser0.get_acquisition() == True:
	dumb = 1
print "End of acquisition 3"
laser1.stopAcquisition()

if laser0.get_error() > 0:
	phidgets.cleanConnection()
        phidgets.stopLoadCells()
        phidgets.stopMotorsLoop()
	phidgets.stopConveyors()
	phidgets.stopStepper()
	sys.exit(0)
if laser1.get_error() > 0:
	phidgets.cleanConnection()
        phidgets.stopLoadCells()
        phidgets.stopMotorsLoop()
	phidgets.stopConveyors()
	phidgets.stopStepper()
	sys.exit(0)

#########################
# 5 - Stop the conveyors
print "Stop conveyors"
phidgets.stopConveyors()

#########################
# 6 - Stop load cells
#phidgets.stopLoadCells()

#########################
# 7 - Stop the rollers
print "Stop motors"
phidgets.stopMotorsLoop()
f.write(str(time.time() - start) + ': Rollers stopped\n')


#########################
# Change direction !!!!!!!!!!!!!
time.sleep(1)
print "Change direction"
#########################



#PASS 4

###################
# 1 - Move the stepper motor (Wait for the motor to reach its fianl position)
print "Move the stepper"
phidgets.moveStepper(rollerGapP4)

####################
# 2 - Start laser
print "Start laser"
# Setup the filename to save the current data
laser0.set_fileName(expPath + "inH_P4.csv")
laser1.set_fileName(expPath + "outH_P4.csv")
# Setup the parameters to save the data
laser0.set_save()
laser1.set_save()
# Create a thread for the laser
thread_l0 = Thread(target=laser0.grabAndSave, args=(0,))
thread_l1 = Thread(target=laser1.grabAndSave, args=(0,))
# Start the thread
thread_l0.start()
thread_l1.start()

####################
# 2.1 - Start load cells
#phidgets.set_lcFileName(expPath + "lcP4.txt")

#thread_lc = Thread(target=phidgets.loadCells, args=())
#thread_lc.start()

#######################
# 3 - Start the rollers
print "Start the rollers"
phidgets.set_rsFileName(expPath + "rollers_1.txt")
thread_r = Thread(target=phidgets.runMotorsLoop, args=(1,rollerSpeedP4,))
thread_r.start()

#########################
# 4 - Start the conveyors
print "Start the conveyors"
phidgets.set_csFileName(expPath + "conveyor_1.txt")
thread_c = Thread(target=phidgets.runConveyors, args=(1,belt0P4,2,belt1P4))
thread_c.start()


#########################
# WAIT !!!!!!!!!!!
# Data acquisition
#time.sleep(2)
while laser1.get_acquisition() == True:
	dumb = 1
print "End of acquisition 4"
laser0.stopAcquisition()

if laser0.get_error() > 0:
	phidgets.cleanConnection()
        phidgets.stopLoadCells()
        phidgets.stopMotorsLoop()
	phidgets.stopConveyors()
	phidgets.stopStepper()
	sys.exit(0)
if laser1.get_error() > 0:
	phidgets.cleanConnection()
        phidgets.stopLoadCells()
        phidgets.stopMotorsLoop()
	phidgets.stopConveyors()
	phidgets.stopStepper()
	sys.exit(0)

#########################
# 5 - Stop the conveyors
print "Stop conveyors"
phidgets.stopConveyors()

#########################
# 6 - Stop load cells
phidgets.stopLoadCells()

#########################
# 7 - Stop the rollers
print "Stop motors"
phidgets.stopMotorsLoop()
f.write(str(time.time() - start) + ': Rollers stopped\n')




#########################
#END

time.sleep(1)

f.close()













