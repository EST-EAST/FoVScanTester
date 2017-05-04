# Support script for repeatability tests
# Moves the system to the position to tare it

import scansupport as ss
from repeat_config import *

ss.motorPositions()
ss.commandMotor(0.0, repeat_tare_pos)
