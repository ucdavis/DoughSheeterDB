# Give the path to find the python wrapper
import sys
sys.path.append('phidgetsClass/')
sys.path.append('laserClass/')

from threading import Thread
import time

# Import the wrapped API
import phidgetsClass_ext
import laserClass_ext

# Create the phidget object
phidgets=phidgetsClass_ext.phidgetsClass()

time.sleep(1)

thread_r = Thread(target=phidgets.runMotorsLoop, args=(1,20,))
print "Start the rollers"
thread_r.start()
print "Rollers started"
time.sleep(3)
print "End of sleep"
phidgets.stopMotorsLoop()
print "Rollers stopped"
#print "Start the rollers"
#phidgets.runMotors(1, 0.6)




#time.sleep(10)
