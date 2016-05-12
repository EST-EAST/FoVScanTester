import cv2

import serial

#cte_serial_port = '/dev/ttyUSB0'
cte_serial_port = 'COM1:'

ser = serial.Serial(
    port=cte_serial_port,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    rtscts=False,
    dsrdtr=False
)

cte_camsource = 0
cte_verbose = True
cte_fileprefix = "frame"
cte_framePath = "./00_acquired/"

cte_stepTime=1000

cte_lsx_min = -500      # End of LS travel in lower units
cte_lsx_max = +500      # End of LS travel in upper units
cte_lsx_scale = 40.0     # LS units / mm
cte_lsx_zero = +50      # LS units coincidence with 0 mm (center) 

cte_lsy_min = -500      # End of LS travel in lower units
cte_lsy_max = +500      # End of LS travel in upper units
cte_lsy_scale = 40.0     # LS units / mm
cte_lsy_zero = +50      # LS units coincidence with 0 mm (center) 

cte_lscomp_min = -500      # End of LS travel in lower units
cte_lscomp_max = +500      # End of LS travel in upper units
cte_lscomp_scale = 40.0     # LS units / mm
cte_lscomp_zero = +50      # LS units coincidence with 0 mm (center) 



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
        cmdx_str = "1MOV%4d" % (lsx_pos)
        ser.write(cmdx_str+'\0')
        cmdy_str = "2MOV%4d" % (lsy_pos)
        ser.write(cmdy_str+'\0')
        ret = 0
    return ret

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
  a = 1
  b = 2
  c = 3
  return a,b,c

def motorClose():
    ser.close()             # close port
    
