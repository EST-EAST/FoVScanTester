import sys
import scansupport as ss

print 'Moving motor to LsX, LsY, LsComp (in motor units)'
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) > 3:
    lsx = float(sys.argv[1])
    lsy = float(sys.argv[2])
    lscomp = float(sys.argv[3])
else:
    lsx = 500.0
    lsy = 500.0
    lscomp = 500.0

# We use this command to freely move the window in 2D (in meters) while compensation is calculated
print 'lsx (in motor units) is ', lsx
print 'lsy (in motor units) is ', lsy
print 'lscomp (in motor units) is ', lscomp

import checkpos

# We use this command to move the motors freely in 3D in motor units
# (in motor units)
ss.commandMotorUnits3D(lsx, lsy, lscomp)
