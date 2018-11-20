import time
from threading import Thread
import phidgetsClass_ext

#def sleeper(i):
#    print "thread %d sleeps for 5 seconds" % i
#    time.sleep(5)
#    print "thread %d woke up" % i

def sleeper(i):
   obj.testThread(i)

obj=phidgetsClass_ext.phidgetsClass()
for i in range(3):
    print "Threads started"
    t = Thread(target=sleeper, args=(i,))
    t.start()
    print "End Threads started"


print "Threads started"
time.sleep(1)
print "Sleep done"
obj.set_stopThread()
print "Threads stoped"
