import cv2
import os
import serial

if (os.name == 'nt'):
    cte_serial_port = 'COM5:'
else:
    cte_serial_port = '/dev/ttyUSB0'

print "Chosen serial port: "+cte_serial_port

ser = serial.Serial(
    port=cte_serial_port,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    rtscts=False,
    dsrdtr=False,
    xonxoff=True
)

cte_camsource = 1
cte_verbose = True
cte_fileprefix = "frame"
cte_framePath = "./00_acquired/"

cte_stepTime=1000

# M2 = x
cte_lsx_min = 0         # End of LS travel in lower units
cte_lsx_max = +(2000)*18  # End of LS travel in upper units
cte_lsx_scale = 2000*1000     # LS units / mm * 1000 mm / 1 m
cte_lsx_zero = +(2000)*9      # LS units coincidence with 0 mm (center) 

# M1 = y
cte_lsy_min = 0      # End of LS travel in lower units
cte_lsy_max = +(2000)*18  # End of LS travel in upper units
cte_lsy_scale = 2000*1000     # LS units / mm * 1000 mm / 1 m
cte_lsy_zero = +(2000)*9      # LS units coincidence with 0 mm (center) 

# M3 = compensacion
cte_lscomp_min = 0      # End of LS travel in lower units
cte_lscomp_max = +(2000)*18  # End of LS travel in upper units
cte_lscomp_scale = 2000*1000     # LS units / mm * 1000 mm / 1 m
cte_lscomp_zero = +(2000)*9      # LS units coincidence with 0 mm (center) 

cte_timeout = 2000

# Home speeds
cte_vhx = 100
cte_vhy = 100
cte_vhcomp = 100

# Index speeds
cte_vix = 30
cte_viy = 30
cte_vicomp = 30

# Movement speeds
cte_vx = 100
cte_vy = 100
cte_vcomp = 100

lsx_pos = 0.0
lsy_pos = 0.0
lscomp_pos = 0.0

def getMotorResponse(response_lenght):
    charsread=0
    response = ""
    while (len(response)<response_lenght):
        response += ser.read(response_lenght-charsread)
    return response

# Commands home and puts the window at the central position.
def resetMotor():

    # Program the motor to warn when the command is done
    cmd_str = "NP"
    ser.write(cmd_str+'\0')
    print(cmd_str)
    print(getMotorResponse(3))

    # Programming the Home speeds
    cmdx_str = "2V%3d" % (cte_vhx)
    ser.write(cmdx_str+'\0')
    print(cmdx_str)
    print(getMotorResponse(3))
    
    cmdy_str = "1V%3d" % (cte_vhy)
    ser.write(cmdy_str+'\0')
    print(cmdy_str)
    print(getMotorResponse(3))
    
    cmdcomp_str = "3V%3d" % (cte_vhcomp)
    ser.write(cmdcomp_str+'\0')
    print(cmdcomp_str)
    print(getMotorResponse(3))
    
    #Execute the home sequence:
    cmdx_str = "2GOHOSEQ"
    ser.write(cmdx_str+'\0')
    print(cmdx_str)
    print(getMotorResponse(3))
    
    cmdy_str = "1GOHOSEQ"
    ser.write(cmdy_str+'\0')
    print(cmdy_str)
    print(getMotorResponse(3))
    
    cmdcomp_str = "3GOHOSEQ"
    ser.write(cmdcomp_str+'\0')
    print(cmdcomp_str)
    print(getMotorResponse(3))
    
    # Programming the Index speeds
    cmdx_str = "2V%03d" % (cte_vix)
    ser.write(cmdx_str+'\0')
    print(cmdx_str)
    print(getMotorResponse(3))
    
    cmdy_str = "1V%03d" % (cte_viy)
    ser.write(cmdy_str+'\0')
    print(cmdy_str)
    print(getMotorResponse(3))
    
    cmdcomp_str = "3V%03d" % (cte_vicomp)
    ser.write(cmdcomp_str+'\0')
    print(cmdcomp_str)
    print(getMotorResponse(3))
    
    # Find the indexes
    cmdx_str = "2GOIX"
    ser.write(cmdx_str+'\0')
    print(cmdx_str)
    print(getMotorResponse(3))
    
    cmdy_str = "1GOIX"
    ser.write(cmdy_str+'\0')
    print(cmdy_str)
    print(getMotorResponse(3))
    
    cmdcomp_str = "3GOIX"
    ser.write(cmdcomp_str+'\0')
    print(cmdcomp_str)
    print(getMotorResponse(3))
    
    # Calculate the center position of the window over the FoV
    lsx_pos = cte_lsx_zero
    lsy_pos = cte_lsy_zero
    lscomp_pos = cte_lscomp_zero
    
    # Set center position as target for the movement
    cmdx_str = "2LA%05d" % (lsx_pos)
    ser.write(cmdx_str+'\0')
    print(cmdx_str)
    print(getMotorResponse(3))
    
    cmdy_str = "1LA%05d" % (lsy_pos)
    ser.write(cmdy_str+'\0')
    print(cmdy_str)
    print(getMotorResponse(3))
    
    cmdcomp_str = "3LA%05d" % (lscomp_pos)
    ser.write(cmdcomp_str+'\0')
    print(cmdcomp_str)
    print(getMotorResponse(3))
    
    cmdx_str = "2V%03d" % (cte_vx)
    ser.write(cmdx_str+'\0')
    print(cmdx_str)
    print(getMotorResponse(3))
    
    cmdy_str = "1V%03d" % (cte_vy)
    ser.write(cmdy_str+'\0')
    print(cmdy_str)
    print(getMotorResponse(3))
    
    cmdcomp_str = "3V%03d" % (cte_vcomp)
    ser.write(cmdcomp_str+'\0')
    print(cmdcomp_str)
    print(getMotorResponse(3))
    
    # Move the motor
    cmdx_str = "2M"
    ser.write(cmdx_str+'\0')
    print(cmdx_str)
    print(getMotorResponse(3))
    
    cmdy_str = "1M"
    ser.write(cmdy_str+'\0')
    print(cmdy_str)
    print(getMotorResponse(3))
    
    cmdcomp_str = "3M"
    ser.write(cmdcomp_str+'\0')
    print(cmdcomp_str)
    print(getMotorResponse(3))
    

def commandMotor(x,y):
    ret = 0
    # Compute compensation
    lscomp = -(x+y)/2
    # Compute LSX and LSY
    lsx_temp=cte_lsx_zero+(x*cte_lsx_scale)
    lsx_pos = max(min(lsx_temp,cte_lsx_max),cte_lsx_min)
    lsy_temp =cte_lsy_zero+(y*cte_lsy_scale)
    lsy_pos = max(min(lsy_temp,cte_lsx_max),cte_lsx_min)
    lscomp_temp = cte_lscomp_zero+(lscomp*cte_lscomp_scale)
    lscomp_pos = max(min(lscomp_temp,cte_lscomp_max),cte_lscomp_min)
    
    if (lsx_temp!=lsx_pos or 
    lsy_temp!=lsy_pos or 
    lscomp_temp!=lscomp_pos):
        print "Error on calculating position: out of range of LS motors"
        print "X: %f Y: %f" % (x,y)
        print "LSX_TEMP: %.2f LSY_TEMP: %.2f LSCOMP_TEMP: %.2f" % (lsx_temp,lsy_temp,lscomp_temp)
        print "LSX_POS: %.2f LSY_POS: %.2f LSCOMP_POS: %.2f" % (lsx_pos,lsy_pos,lscomp_pos)
        ret=-1
    else:
        # send the commands
        cmdx_str = "2LA%04d" % (lsx_pos)
        ser.write(cmdx_str+'\0')
        print(cmdx_str)
        print(getMotorResponse(3))

        cmdy_str = "1LA%04d" % (lsy_pos)
        ser.write(cmdy_str+'\0')
        print(cmdy_str)
        print(getMotorResponse(3))

        cmdcomp_str = "3LA%04d" % (lscomp_pos)
        ser.write(cmdcomp_str+'\0')
        print(cmdcomp_str)        
        print(getMotorResponse(3))

        # Move the motor
        cmdx_str = "2M"
        ser.write(cmdx_str+'\0')
        print(cmdx_str)
        print(getMotorResponse(3))

        cmdy_str = "1M"
        ser.write(cmdy_str+'\0')
        print(cmdy_str)
        print(getMotorResponse(3))

        cmdcomp_str = "3M"
        ser.write(cmdcomp_str+'\0')
        print(cmdcomp_str)
        print(getMotorResponse(3))

        ret = 0

    return ret,lsx_pos,lsy_pos,lscomp_pos

def stepDone():
    # Wait for command or step time
    # it returns True if nobody presses the ESC
    key = cv2.waitKey(cte_stepTime)
    if (key==27):
        ## Someone presses the key, should return
        ret=-1
    else:
        if (key==-1):
            ## Time expired
            ret=1
        else:
            ## Another key presssed
            ret=0

    return ret

def motorPositions():
  m1_fdback = lsy_pos
  m2_fdback = lsx_pos
  m3_fdback = lscomp_pos
  return m1_fdback, m2_fdback, m3_fdback

def motorClose():
    ser.close()             # close port
    
