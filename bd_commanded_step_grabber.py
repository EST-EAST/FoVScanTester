# -*- coding: utf-8 -*-
"""
Frame Grabber done in OpenCv
Open a camera source, do some pre-process, and save frames under a trigger
"""

import cv2
import sqlite3

####### Functions ################

### Commands the motor to the position of that step
def motorPos(x,y):
    print "Sweep step X: " + str(x) + " Y: " + str(y)

### Computes new step index
def nextStep(x,y,c):
    # Step sequence index determination 
    c+=1
    x+=1
    if (x>=cte_stepXsize):
        x=0
        y+=1
    return x,y,c

### Investigate if the current step has been executed
def stepDone():
    # Wait for command or step time
    # it returns True if nobody presses the ESC
    key = cv2.waitKey(cte_stepTime)
    if (key==27):
        ## Someone presses the key, should return
        ret=-1
    else:
        if (key==-1):
            ## Time expired
            ret=1
        else:
            ## Another key presssed
            ret=0
    return ret

### Set the initial step index
def initialStep():
    return 0,0,0

### Investigate if the steps have been finished
def endStep(x,y,c):
    return (y>=cte_stepXsize)

###### END Functions ############

#### Parameters
cte_stepXsize=10
cte_stepYsize=10
cte_stepTime=300
cte_framePath="./00_acquired/"
cte_database="./db.sqlite3"

#### Variable initialization
key = 0
colorMode=True

#### START EXECUTION ######

# Open de sqlite file
db=sqlite3.connect(cte_database)

cur = db.cursor()
cur.execute('SELECT SQLITE_VERSION()')
dbdata = cur.fetchone()
print "SQLite version: %s" % dbdata

# Cam has the video source
cam = cv2.VideoCapture(0)

print "Horizontal: " + str(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
print "Vertical: "+ str(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Command the initial step position
stepX,stepY,stepCounter=initialStep()
motorPos(stepX,stepY)
# Wait command to end
done=0
while (done==0):
    done=stepDone();
# END Command initial position

# Steps loop
# until ESC key is pressed
# or steps have finished
while (done!=-1):
    # Acquire image
    ret, frame = cam.read()
    #save to disk
    strg='frame%03d_%03d.png' % (stepX, stepY)
    cv2.imwrite(cte_framePath + strg, frame)
    #show the image
    cv2.imshow('Single Frame', frame)    
    stepX,stepY,stepCounter=nextStep(stepX,stepY,stepCounter)
    if (not(endStep(stepX,stepY,stepCounter))):
        # Command next position
        motorPos(stepX,stepY)
        # Wait command to end
        done=0
        while (done==0):
            done=stepDone();
        # END Command next position
    else:
        # End step was done, no next step needed
        done=-1
        
# End of program, ESC key was pressed or steps have finished
cam.release()
cv2.destroyAllWindows()
