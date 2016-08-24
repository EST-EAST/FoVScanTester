#!/usr/bin/python
# -*- coding: utf-8 -*-
# Forces the motors to move the window to the center position of the FoV

import sweepconfig
import sweepsupport as sws

#### START EXECUTION ######

if (sweepconfig.cte_disable_motors_first):
    sws.disableMotors()

print("Check initial motor positions")
sws.motorPositions()

if (sweepconfig.cte_enable_motors_first):
    sws.enableMotors()

# Calculate the center position of the window over the FoV
lsx = 0.0
lsy = 0.0

print("lsx: "+str(lsx))
print("lsy: "+str(lsy))

sws.commandMotor(lsx, lsy)

print("Check motor positions after resets")
sws.motorPositions()

sws.motorClose()

