#!/usr/bin/python
# -*- coding: utf-8 -*-
# Forces ONLY the X and Y motors to move to their Home position and sets their zeroes.

import sweepconfig
import sweepsupport as sws

#### START EXECUTION ######

if (sweepconfig.cte_disable_motors_first):
    sws.disableMotors()

print("Check initial motor positions")
sws.motorPositions()

if (sweepconfig.cte_enable_motors_first):
    sws.enableMotors()

sws.goHomeMx()
sws.goHomeMy()
#sws.goHomeMcomp()
print("Check motor positions after resets")
sws.motorPositions()

sws.motorClose()

