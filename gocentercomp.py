#!/usr/bin/python
# -*- coding: utf-8 -*-

# Forces ONLY the Comp motor to go to the position corresponding to the window center location.

import scanconfig
import scansupport as sws

#### START EXECUTION ######

if (scanconfig.cte_disable_motors_first):
    sws.disableMotors()

print("Check initial motor positions")
sws.motorPositions()

if (scanconfig.cte_enable_motors_first):
    sws.enableMotors()

# Calculate the center position of the window over the FoV
lsx = 0.0
lsy = 0.0

print("lsx: "+str(lsx))
print("lsy: "+str(lsy))

sws.commandMotorComp(lsx, lsy)

print("Check motor positions after resets")
sws.motorPositions()

sws.motorClose()

