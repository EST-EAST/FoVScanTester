# -*- coding: utf-8 -*-
"""
Frame Grabber done in OpenCv
Open a camera source, do some pre-process, and save frames under a trigger
"""

import cv2
import numpy as np

#### Parameters
cte_stepXsize=100
cte_stepYsize=100
cte_stepTime=100
cte_framePath="./00_acquired/"

# Cam has the video source
cam = cv2.VideoCapture(0)

print "Horizontal: " + str(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
print "Vertical: "+ str(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#### Variable initialization
key = 0
stepX = 0
stepY = 0
colorMode=True


# Main loop, acquires, process and saves images
# until ESC key is pressed
while (key!=27):   #ESC key 

    # Acquire image
    ret, frame = cam.read()
    
    # Wait for command or step time
    key = cv2.waitKey(cte_stepTime)
    
    # Commands management
    if (key== ord('x')):
        colorMode=not(colorMode)
        print "colorMode: " + str(colorMode)

    saveImage=(key== ord('s'))
        
    # Apply preprocess commands        
    if (colorMode==False):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    # Step sequence index determination 
    stepX+=1
    if (stepX>cte_stepXsize):
        stepX=0
        stepY+=1
    if (stepY>cte_stepYsize):
        stepY=0        
    print "Sweep step X: " + str(stepX) + " Y: " + str(stepY)
    
    #save to disk if needed
    if (saveImage):
        cv2.imwrite(cte_framePath+"frameX{}_Y{}.png".format(stepX,stepY),frame)
    
    #show the image
    cv2.imshow('Single Frame', frame)    
        
# End of program, ESC key was pressed
cam.release()
cv2.destroyAllWindows()
