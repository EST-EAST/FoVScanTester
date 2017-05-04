#!/usr/bin/python
# -*- coding: utf-8 -*-
# Script to checks the current position of the motors

import scanconfig
import scansupport as sws

#### START EXECUTION ######

if (scanconfig.cte_disable_motors_first):
    sws.disableMotors()

if (scanconfig.cte_enable_motors_first):
    sws.enableMotors()

print("Check motor positions")

if not scanconfig.cte_use_motorsim:
    # TODO: INCORPORATE 'OST' COMMAND HANDLING TO MOTORSIM
    sws.stepFinishedXPoll()
    sws.stepFinishedYPoll()
    sws.stepFinishedCompPoll()

sws.motorPositions()
sws.motorClose()

