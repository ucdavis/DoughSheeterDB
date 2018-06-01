import thread
import time
import phidgetsClass_ext

def runMotors(test):
   obj.runMotors(1, 0.6)
   time.sleep(3)
   obj.stopMotors()

def runConveyors(test):
   obj.runConveyor_0(0,2.5)
   obj.runConveyor_1(0,2.5)

   time.sleep(3)

   obj.stopConveyor_0()
   obj.stopConveyor_1()


# Create
obj=phidgetsClass_ext.phidgetsClass()

# Create two threads as follows
try:
   thread.start_new_thread( runMotors, (0, ))
   thread.start_new_thread( runConveyors, (0,))
except:
   print "Error: unable to start thread"


time.sleep(5)
#while 1:
#   pass

# test the conveyor
#obj.runConveyor_0(0,2.5)
#obj.runConveyor_1(0,2.5)

#time.sleep(2)

#obj.stopConveyor_0()
#obj.stopConveyor_1()

# Test the stepper
#obj.initStepper()
#obj.moveStepper(50000)

# Test the motor
#obj.runMotors(1, 0.6)
#time.sleep(3)
#obj.stopMotors()
