

####################
# 1 - Move the stepper motor (Wait for the motor to reach its fianl position)
print "Move the stepper"
phidgets.moveStepper(4)

####################
# 2 - Start laser #1
print "Start laser 1"
# Setup the filename to save the current data
laser1.set_fileName(expPath + "data1.xyz")
# Setup the parameters to save the data
laser1.set_save()
# Create a thread for the laser
thread_l = Thread(target=laser1.grabAndSave, args=(0,))
# Start the thread
thread_l.start()

####################
# 2.1 - Start load cells
phidgets.set_lc0FileName(expPath + "lc0_s1.txt")
phidgets.set_lc1FileName(expPath + "lc1_s1.txt")

thread_lc = Thread(target=phidgets.loadCells, args=())
thread_lc.start()

#######################
# 3 - Start the rollers
print "Start the rollers"
thread_r = Thread(target=phidgets.runMotorsLoop, args=(1,60,))
thread_r.start()

#########################
# 4 - Start the conveyors
print "Start the conveyors"
phidgets.runConveyors(1,100,0,100)


#########################
# WAIT !!!!!!!!!!!
# Data acquisition

#print("Before: ", laser1.get_dough_end())

while laser1.get_dough_end() == False:
	dumb = 1 
        #print "Acquisition"
print "End of acquisition 2"

#########################
# 5 - Stop laser #1
print "Stop laser"
laser1.stopAcquisition()

#########################
# 5.1 - Stop load cells
phidgets.stopLoadCells()

#########################
# 6 - Stop the rollers
print "Stop motors"
phidgets.stopMotorsLoop()

#########################
# 7 - Stop the conveyors
print "Stop conveyors"
phidgets.stopConveyors()

#########################
# Change direction !!!!!!!!!!!!!
time.sleep(1)
print "Change direction"
#########################





#########################
# 1 - Move the stepper motor
phidgets.moveStepper(6)

#########################
# 2 - Start laser #0
laser0.set_fileName(expPath + "data2.xyz")
laser0.set_save()
thread_l = Thread(target=laser0.grabAndSave, args=())
thread_l.start()

####################
# 2.1 - Start load cells
phidgets.set_lc0FileName(expPath + "lc0_s2.txt")
phidgets.set_lc1FileName(expPath + "lc1_s2.txt")

thread_lc = Thread(target=phidgets.loadCells, args=(0,))
thread_lc.start()

#########################
# 3 - Start the rollers
thread_r = Thread(target=phidgets.runMotorsLoop, args=(-1,100,))
thread_r.start()

#########################
# 4 - Start the conveyors
phidgets.runConveyors(0,100,1,100)

#########################
# WAIT !!!!!!!!!!!
# Data acquisition
while laser0.get_dough_end() == False:
	dumb = 1 
        print "Acquisition"
print "End of acquisition 3"

#########################
# 5 - Stop laser #1
laser0.stopAcquisition()

#########################
# 5.1 - Stop load cells
phidgets.stopLoadCells()

#########################
# 6 - Stop the rollers
phidgets.stopMotorsLoop()

#########################
# 7 - Stop the conveyors
phidgets.stopConveyors()
