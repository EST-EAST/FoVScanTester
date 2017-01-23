#!/usr/bin/python
# -*- coding: utf-8 -*-
# Script to checks the current position of the motors

import scanconfig
import scansupport as sws

#### START EXECUTION ######

sws.enableMotors()

print("Check initial motor positions")
sws.stepFinishedXPoll();
sws.stepFinishedYPoll();
sws.stepFinishedCompPoll();
sws.motorPositions()


sws.motorClose()

