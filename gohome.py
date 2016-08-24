#!/usr/bin/python
# -*- coding: utf-8 -*-
# Forces the motors to go to their Home positions, and sets their zeroes

import scanconfig
import scansupport as sws

#### START EXECUTION ######

if (scanconfig.cte_disable_motors_first):
    sws.disableMotors()

print("Check initial motor positions")
sws.motorPositions()

if (scanconfig.cte_enable_motors_first):
    sws.enableMotors()

sws.goHomeMx()
sws.goHomeMy()
sws.goHomeMcomp()
print("Check motor positions after resets")
sws.motorPositions()

sws.motorClose()

