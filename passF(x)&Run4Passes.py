# read from csv
import csv

# reading from parameter.csv by passing the table to a 2D list
with open('parameters.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    #para = list(csv_reader)
    #para[0]
    #print(para[0])
    param = [row for row in csv_reader]
    print (param)

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
expDateTime = dateparam[0][0]
expPath = "data/" + expDateTime + "/"
os.makedirs(expPath)

# Log file
logPath = "data/" + expDateTime + "/log.txt"
f = open(logPath, 'w')
f.write('Log file: ' + expDateTime + '\n')

# Start the timestamp
start = time.time()


# for running one pass
def runExperiment(listOfParam):
    # 0 - Init the stepper motor
    f.write(str(time.time() - start) + ': Initialization of the stepper motor\n')
    phidgets.initStepper()
    f.write(str(time.time() - start) + ': End of initialization of the stepper motor\n')
    # 1 - Move the stepper motor (Wait for the motor to reach its final position)
    print "Move the stepper"
    f.write(str(time.time() - start) + ': Change gap\n')
    phidgets.moveStepper(listOfParam[1])
    f.write(str(time.time() - start) + ': Gap changed\n')
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
    
    direction = listOfParam[0]
    # direction is 1, belt1 in and belt0 out
    # otherwise, direction is 2, belt1 out and belt0 in
    if direction == 1:
        rollerDir= -1
        belt0Dir = 2
        belt1Dir = 1
    else: 
        rollerDir= 1
        belt0Dir = 1
        belt1Dir = 2
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
    thread_r = Thread(target=phidgets.runMotorsLoop, args=(rollerDir,listOfParam[2],))
    thread_r.start()
    f.write(str(time.time() - start) + ': Rollers started\n')

    #########################
    # 4 - Start the conveyors 
    print "Start the conveyors"
    phidgets.set_csFileName(expPath + "conveyor_0.txt")
    # Direc 2,1 Movement from 11 to 10. 
    # Arguments are Belt 0, Belt 1
    thread_c = Thread(target=phidgets.runConveyors, args=(belt0Dir,listOfParam[3],belt1Dir,listOfParam[4]))
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


# run all the passes by calling runExperiment function
passNum =dateparam[0][1] 
for i in np.arange(passNum):
    runExperiment(dataparam[i+1])
