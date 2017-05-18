import sys
import scansupport as ss

print 'Moving motor to X, Y (in mm)'
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) > 2:
    x = float(sys.argv[1])/1000.0
    y = float(sys.argv[2])/1000.0
else:
    x = 0.0 / 1000.0
    y = 0.050 / 1000.0

# We use this command to freely move the window in 2D (in meters) while compensation is calculated
print 'x (in meters) is ', x
print 'y (in meters) is ', y
import checkpos

ss.commandMotor(x, y)
