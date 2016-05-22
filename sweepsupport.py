import cv2
import sweepconfig
import sys
sys.path.insert(0, './fsm')
import FoV

if not(sweepconfig.cte_use_socket):
    import serial
    cte_serial_port = sweepconfig.cte_serial_port
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
    FoV.dre.ser = ser
else:
    import socket               # Import socket module
    
    sckt = socket.socket()         # Create a socket object
    sckt.connect((sweepconfig.cte_socket_ip, sweepconfig.cte_socket_port))
    FoV.dre.ser = sckt
    
FoV.dre.cte_use_socket = sweepconfig.cte_use_socket

cte_camsource = sweepconfig.cte_camsource

cte_verbose = True
cte_fileprefix = "frame"
cte_framePath = "./00_acquired/"

cte_stepTime=1000

# Mx = x
cte_lsx_min = 0         # End of LS travel in lower units
cte_lsx_max = +(2000)*18  # End of LS travel in upper units
cte_lsx_scale = 2000*1000     # LS units / mm * 1000 mm / 1 m
cte_lsx_zero = +(2000)*9      # LS units coincidence with 0 mm (center) 

# My = y
cte_lsy_min = 0      # End of LS travel in lower units
cte_lsy_max = +(2000)*18  # End of LS travel in upper units
cte_lsy_scale = 2000*1000     # LS units / mm * 1000 mm / 1 m
cte_lsy_zero = +(2000)*9      # LS units coincidence with 0 mm (center) 

# Mcomp = compensacion
cte_lscomp_min = 0      # End of LS travel in lower units
cte_lscomp_max = +(2000)*18  # End of LS travel in upper units
cte_lscomp_scale = 2000*1000     # LS units / mm * 1000 mm / 1 m
cte_lscomp_zero = +(2000)*9      # LS units coincidence with 0 mm (center) 

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

def getMotorResponse():
    FoV.getCtrlResponse()
    return FoV.dre.command_rx_buf


def sendMotorCommand(cmd_str):
    #ser.write(cmd_str+'\13')
    print "Command sent: "+cmd_str
    FoV.dre.command_tx_buf = cmd_str
    FoV.sendCtrlCommand()

# Commands home and puts the window at the central position.
def resetMotor():
    # Programming the Home speeds
    cmdx_str = str(sweepconfig.cte_motor_x)+"V%3d" % (cte_vhx)
    sendMotorCommand(cmdx_str)
    print(cmdx_str)
    print(getMotorResponse())

    cmdy_str = str(sweepconfig.cte_motor_y)+"V%3d" % (cte_vhy)
    sendMotorCommand(cmdy_str)
    print(cmdy_str)
    print(getMotorResponse())
    
    '''
    cmdcomp_str = str(sweepconfig.cte_motor_comp)+"V%3d" % (cte_vhcomp)
    sendMotorCommand(cmdcomp_str)
    print(cmdcomp_str)
    print(getMotorResponse())
    '''    
    
    #Execute the home sequence:
    cmdx_str = str(sweepconfig.cte_motor_x)+"GOHOSEQ"
    sendMotorCommand(cmdx_str)
    print(cmdx_str)
    print(getMotorResponse())

    cmdy_str = str(sweepconfig.cte_motor_y)+"GOHOSEQ"
    sendMotorCommand(cmdy_str)
    print(cmdy_str)
    print(getMotorResponse())
    
    '''    
    cmdcomp_str = str(sweepconfig.cte_motor_comp)+"GOHOSEQ"
    sendMotorCommand(cmdcomp_str)
    print(cmdcomp_str)
    print(getMotorResponse())
    '''
    
    # Programming the Index speeds
    cmdx_str = str(sweepconfig.cte_motor_x)+"V%03d" % (cte_vix)
    sendMotorCommand(cmdx_str)
    print(cmdx_str)
    print(getMotorResponse())

    cmdy_str = str(sweepconfig.cte_motor_y)+"V%03d" % (cte_viy)
    sendMotorCommand(cmdy_str)
    print(cmdy_str)
    print(getMotorResponse())
    
    '''    
    cmdcomp_str = str(sweepconfig.cte_motor_comp)+"V%03d" % (cte_vicomp)
    sendMotorCommand(cmdcomp_str)
    print(cmdcomp_str)
    print(getMotorResponse())
    '''
    
    # Find the indexes
    cmdx_str = str(sweepconfig.cte_motor_x)+"GOIX"
    sendMotorCommand(cmdx_str)
    print(cmdx_str)
    print(getMotorResponse())

    cmdy_str = str(sweepconfig.cte_motor_y)+"GOIX"
    sendMotorCommand(cmdy_str)
    print(cmdy_str)
    print(getMotorResponse())
    
    '''
    cmdcomp_str = str(sweepconfig.cte_motor_comp)+"GOIX"
    sendMotorCommand(cmdcomp_str)
    print(cmdcomp_str)
    print(getMotorResponse())
    '''
    
    # Calculate the center position of the window over the FoV
    lsx_pos = cte_lsx_zero
    lsy_pos = cte_lsy_zero
    lscomp_pos = cte_lscomp_zero
    
    # Set center position as target for the movement
    cmdx_str = str(sweepconfig.cte_motor_x)+"LA%05d" % (lsx_pos)
    sendMotorCommand(cmdx_str)
    print(cmdx_str)
    print(getMotorResponse())

    cmdy_str = str(sweepconfig.cte_motor_y)+"LA%05d" % (lsy_pos)
    sendMotorCommand(cmdy_str)
    print(cmdy_str)
    print(getMotorResponse())
    
    '''    
    cmdcomp_str = str(sweepconfig.cte_motor_comp)+"LA%05d" % (lscomp_pos)
    sendMotorCommand(cmdcomp_str)
    print(cmdcomp_str)
    print(getMotorResponse())
    '''
    
    cmdx_str = str(sweepconfig.cte_motor_x)+"V%03d" % (cte_vx)
    sendMotorCommand(cmdx_str)
    print(cmdx_str)
    print(getMotorResponse())

    cmdy_str = str(sweepconfig.cte_motor_y)+"V%03d" % (cte_vy)
    sendMotorCommand(cmdy_str)
    print(cmdy_str)
    print(getMotorResponse())    

    '''    
    cmdcomp_str = str(sweepconfig.cte_motor_comp)+"V%03d" % (cte_vcomp)
    sendMotorCommand(cmdcomp_str)
    print(cmdcomp_str)
    print(getMotorResponse())
    '''
    
    # Move the motor
    cmdx_str = str(sweepconfig.cte_motor_x)+"M"
    sendMotorCommand(cmdx_str)
    print(cmdx_str)
    print(getMotorResponse())

    cmdy_str = str(sweepconfig.cte_motor_y)+"M"
    sendMotorCommand(cmdy_str)
    print(cmdy_str)
    print(getMotorResponse())
    
    '''
    cmdcomp_str = str(sweepconfig.cte_motor_comp)+"M"
    sendMotorCommand(cmdcomp_str)
    print(cmdcomp_str)
    print(getMotorResponse())
    '''
    

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

        # Program the motor to warn when the command is done

        cmd_str = str(sweepconfig.cte_motor_x)+"NP"
        sendMotorCommand(cmd_str)
        print("Cmd: "+ cmd_str)
	r=getMotorResponse()
	print("Resp:"+r)

        cmdx_str = str(sweepconfig.cte_motor_x)+"LA%04d" % (lsx_pos)
        sendMotorCommand(cmdx_str)
        print(cmdx_str)
	r=getMotorResponse()
	print("Resp:"+r)

        # Program the motor to warn when the command is done
        cmd_str = str(sweepconfig.cte_motor_y)+"NP"
        sendMotorCommand(cmd_str)
        print(cmd_str)
	r=getMotorResponse()
	print("Resp:"+r)

        cmdy_str = str(sweepconfig.cte_motor_y)+"LA%04d" % (lsy_pos)
        sendMotorCommand(cmdy_str)
        print(cmdy_str)
	r=getMotorResponse()
	print("Resp:"+r)

    	'''
        # Program the motor to warn when the command is done
        cmd_str = str(sweepconfig.cte_motor_comp)+"NP"
        sendMotorCommand(cmd_str)
        print(cmd_str)
	r=getMotorResponse()
	print("Resp:"+r)

        cmdcomp_str = str(sweepconfig.cte_motor_comp)+"LA%04d" % (lscomp_pos)
        sendMotorCommand(cmdcomp_str)
        print(cmdcomp_str)        
	r=getMotorResponse()
	print("Resp:"+r)
    	'''

        numberOfPReceived=0
        # Move the motor
        cmdx_str = str(sweepconfig.cte_motor_x)+"M"
        sendMotorCommand(cmdx_str)
        print(cmdx_str)
	r=getMotorResponse()
	print("Resp:"+r)
        if (r=="p"):
            numberOfPReceived+=1
        print("Number of P: "+str(numberOfPReceived))
        
        cmdy_str = str(sweepconfig.cte_motor_y)+"M"
        sendMotorCommand(cmdy_str)
        print("Cmd:"+cmdy_str)
	r=getMotorResponse()
	print("Resp:"+r)
        if (r=="p"):
            numberOfPReceived+=1        
        print("Number of P: "+str(numberOfPReceived))
    	'''
        cmdcomp_str = str(sweepconfig.cte_motor_comp)+"M"
        sendMotorCommand(cmdcomp_str)
        print(cmdcomp_str)
	r=getMotorResponse()
	print("Resp:"+r)
        if (r=="p"):
            numberOfPReceived+=1        
    	'''

	# Wait for command responses
	print("Waiting Motors to finish")
	r=getMotorResponse()
	print("Resp:"+r)
        if (r=="p"):
            numberOfPReceived+=1        
        print("Number of P: "+str(numberOfPReceived))
	r=getMotorResponse()
	print("Resp:"+r)
        if (r=="p"):
            numberOfPReceived+=1        
        print("Number of P: "+str(numberOfPReceived))
        #print("Second resp:"+getMotorResponse())
        if (numberOfPReceived==2):
            ret = 0
        else:
            ret = -1
        print("Number of P: "+str(numberOfPReceived))

    return ret,lsx_pos,lsy_pos,lscomp_pos

def stepDone():
    # Wait for command or step time
    # it returns True if nobody presses the ESC
    #key = cv2.waitKey(cte_stepTime)
    key=-1
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
	# Obtain final positions
	cmd_str = str(sweepconfig.cte_motor_x)+"POS"
	sendMotorCommand(cmd_str)
	print("PosCmd:"+cmd_str)
	r=getMotorResponse()
	print("PosResp:"+r)
	mx_fdback=int(r)

        cmd_str = str(sweepconfig.cte_motor_y)+"POS"
	sendMotorCommand(cmd_str)
	print("PosCmd:"+cmd_str)
	r=getMotorResponse()
	print("PosResp:"+r)
	my_fdback=int(r)

	'''
	cmd_str = str(sweepconfig.cte_motor_comp)+"POS"
	sendMotorCommand(cmd_str)
	print("PosCmd:"+cmd_str)
	r=getMotorResponse()
	print("PosResp:"+r)
	mcomp_fdback=int(r)
	'''
	mcomp_fdback=0

	return mx_fdback, my_fdback, mcomp_fdback

def motorClose():
    if not(sweepconfig.cte_use_socket):
        ser.close()             # close port
    else:    
        sckt.close              # Close the socket when done    

