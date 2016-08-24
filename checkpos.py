#!/usr/bin/python
# -*- coding: utf-8 -*-
# Script to checks the current position of the motors

import sweepconfig
import sweepsupport as sws

#### START EXECUTION ######

if (sweepconfig.cte_disable_motors_first):
    sws.disableMotors()

if (sweepconfig.cte_enable_motors_first):
    sws.enableMotors()

print("Check initial motor positions")
sws.motorPositions()


sws.motorClose()

