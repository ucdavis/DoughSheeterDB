
# Give the path to find the python wrapper
import sys
sys.path.append('phidgetsClass/')
sys.path.append('laserClass/')

# Import library modules
from threading import Thread
from datetime import datetime
import time
import os
import signal
import sys

# Import the wrapped API
import phidgetsClass_ext
import laserClass_ext

#read from csv
import csv

######################################################################################################
# FUNCTIONS
######################################################################################################

# To run each pass - read experiment parameters from parameter.csv, 
#which reads from the coverSheet of the experiment workbook
def runExperiment(listOfParam):
    # for the first pass, the stepper should be initialized by running phidgets.initStepper()
    passNumber = listOfParam[0]
    if passNumber =='1':
        # 0 - Init the stepper motor
        f.write(str(time.time() - start) + ': Initialization of the stepper motor\n')
        phidgets.initStepper()
        f.write(str(time.time() - start) + ': End of initialization of the stepper motor\n')
        # 1 - Move the stepper motor (Wait for the motor to reach its final position)
        print "Move the stepper"
        f.write(str(time.time() - start) + ': Change gap\n')
        phidgets.moveStepper(float(listOfParam[2]))
        f.write(str(time.time() - start) + ': Gap changed\n')
    else:
        # 1 - Move the stepper motor (Wait for the motor to reach its fianl position)
        print "Move the stepper"
        f.write(str(time.time() - start) + ': Change gap\n')
        phidgets.moveStepper(float(listOfParam[2]))
        f.write(str(time.time() - start) + ': Gap changed\n')

    # 2 - Start laser
    direction = int(listOfParam[1])
    if direction == 1:
        rollerDir= -1
        belt0Dir = 2
        belt1Dir = 1
    else: 
        rollerDir= 1
        belt0Dir = 1
        belt1Dir = 2
    print "Start lasers"
    # Setup the filename to save the current data
    if direction ==1:
        laser0.set_fileName(expPath + "outH_P" + passNumber + ".csv")
        laser1.set_fileName(expPath + "inH_P"+passNumber+".csv")
    else:
        laser0.set_fileName(expPath + "inH_P" + passNumber + ".csv")
        laser1.set_fileName(expPath + "outH_P" + passNumber + ".csv")
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
    # load cell only need to be started for the first pass(according to Adrien's code)
    if passNumber =='1':
        # 2.1 - Start load cells
        phidgets.set_lcFileName(expPath + "VF.csv")

        thread_lc = Thread(target=phidgets.loadCells, args=())
        thread_lc.start()

    #######################
    # 3 - Start the rollers
    print "Start the rollers"
    if passNumber =='1':
        phidgets.set_rsFileName(expPath + "rollers_0.txt")
        thread_r = Thread(target=phidgets.runMotorsLoop, args=(rollerDir,float(listOfParam[3]),))
        thread_r.start()
        f.write(str(time.time() - start) + ': Rollers started\n')
    else:
        phidgets.set_rsFileName(expPath + "rollers_1.txt")
        thread_r = Thread(target=phidgets.runMotorsLoop, args=(rollerDir,float(listOfParam[3]),))
        thread_r.start()
        f.write(str(time.time() - start) + ': Rollers started\n')

    #########################
    # 4 - Start the conveyors 
    print "Start the conveyors"
    if passNumber =='1':
        phidgets.set_csFileName(expPath + "conveyor_0.txt")
        thread_c = Thread(target=phidgets.runConveyors, args=(belt0Dir,int(listOfParam[4]),belt1Dir,int(listOfParam[5])))
        thread_c.start()
        f.write(str(time.time() - start) + ': Conveyors started\n')

    else:
        phidgets.set_csFileName(expPath + "conveyor_1.txt")
        thread_c = Thread(target=phidgets.runConveyors, args=(belt0Dir,int(listOfParam[4]),belt1Dir,int(listOfParam[5])))
        thread_c.start()
        f.write(str(time.time() - start) + ': Conveyors started\n')
    #########################
    # WAIT !!!!!!!!!!!
    # Data acquisition
    
    while laser0.get_acquisition() == True:
        dumb = 1
    print "End of acquisition " + passNumber
    
    if direction == 1:
	# Laser 0 is the output and stops automatically
        while laser0.get_acquisition() == True:
            dumb = 1
        print "End of acquisition " + passNumber
	# Laser 1 is input and has to be stopped in the code
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
    if direction == 2:
	# Laser 1 is the output and stops automatically
        while laser1.get_acquisition() == True:
	    dumb = 1
        print "End of acquisition " + passNumber
        laser0.stopAcquisition()
	# Laser 0 is input and has to be stopped in the code

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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN CODE
#######################################



# reading from parameter.csv by passing the table to a 2D list
with open('parameters.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    #para = list(csv_reader)
    #para[0]
    #print(para[0])
    param = [row for row in csv_reader]
    print (param)



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
expDateTime = param[0][0]
expPath = "data/" + expDateTime + "/"
os.makedirs(expPath)

# Log file
logPath = "data/" + expDateTime + "/log.txt"
f = open(logPath, 'w')
f.write('Log file: ' + expDateTime + '\n')

# Start the timestamp
start = time.time()


# run all the passes by calling runExperiment function
passNum =int(param[0][1])
i=1
for i in range(1,passNum+1):
    runExperiment(param[i])
    print ("completed pass " + str(i))
    if i== passNum:
	print ("stop the for loop")
        break

# closing open functions
f.close()
phidgets.stopLoadCells()
