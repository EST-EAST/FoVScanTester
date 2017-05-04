# Support script for repeatability tests
# Moves system to "prefix" position
import scansupport as ss
from repeat_config import *

ss.motorPositions()
ss.commandMotor(0.0, repeat_prefix_pos)
