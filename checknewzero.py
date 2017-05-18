import sys
import scansupport as ss
import scanconfig
from time import sleep

print 'Moving motor to LsX, LsY (in motor units), LsComp will be automatically calculated'
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) > 2:
    lsx = float(sys.argv[1])
    lsy = float(sys.argv[2])
else:
    lsx = 500.0
    lsy = 500.0

# We use this command to freely move the window in 2D (in meters) while compensation is calculated
print 'lsx (in motor units) is ', lsx
print 'lsy (in motor units) is ', lsy

import checkpos

# We use this commmand to calculate the compensated position for a 2D window position
# this is very useful to calculate the new "compensation zero" value for cte_lscomp_zero
ss.commandMotorUnits2D(lsx, lsy)

sleep(scanconfig.cte_step_delay_time)
import checkpos
