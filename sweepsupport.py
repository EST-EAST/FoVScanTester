import sweepconfig
import sys
sys.path.insert(0, './fsm')
import FoV

if sweepconfig.cte_use_cvcam:
    import cv2

if not(sweepconfig.cte_use_socket):
    import serial

    FoV.dre.m1port = sweepconfig.cte_motor_x_xport
    FoV.dre.m2port = sweepconfig.cte_motor_y_xport
    FoV.dre.m3port = sweepconfig.cte_motor_comp_xport

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

if sweepconfig.cte_use_cvcam:
    cte_camsource = sweepconfig.cte_camsource


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

if (sweepconfig.cte_use_socket):
    prefixX = ""
    prefixY = ""
    prefixComp = ""
else:
    prefixX = str(sweepconfig.cte_motor_x)
    prefixY = str(sweepconfig.cte_motor_y)
    prefixComp = str(sweepconfig.cte_motor_comp)

def getMotorResponse():
    FoV.getCtrlResponse()
    return FoV.dre.command_rx_buf

def sendMotorCommand(cmd_str):
    #ser.write(cmd_str+'\13')
    print "Command sent: "+cmd_str
    FoV.dre.command_tx_buf = cmd_str
    FoV.sendCtrlCommand()

def sendXportBegin(m):
    if (sweepconfig.cte_use_socket):
        cmdx_str = "#" + str(m)
        sendMotorCommand(cmdx_str)
        print(cmdx_str)

def sendXportEnd():
    if (sweepconfig.cte_use_socket):
        cmdx_str = "@"
        sendMotorCommand(cmdx_str)
        print(cmdx_str)

# Commands home and puts the window at the central position.
def resetMotor():

    if (sweepconfig.cte_use_motor_x):
        # Programming the Home speeds
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        cmdx_str = prefixX+"V%3d" % (cte_vhx)
        sendMotorCommand(cmdx_str)
        print(cmdx_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        cmdy_str = prefixY+"V%3d" % (cte_vhy)
        sendMotorCommand(cmdy_str)
        print(cmdy_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        cmdcomp_str = prefixComp+"V%3d" % (cte_vhcomp)
        sendMotorCommand(cmdcomp_str)
        print(cmdcomp_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        #Execute the home sequence:
        cmdx_str = prefixX+"GOHOSEQ"
        sendMotorCommand(cmdx_str)
        print(cmdx_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        cmdy_str = prefixY+"GOHOSEQ"
        sendMotorCommand(cmdy_str)
        print(cmdy_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        cmdcomp_str = prefixComp+"GOHOSEQ"
        sendMotorCommand(cmdcomp_str)
        print(cmdcomp_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        # Programming the Index speeds
        cmdx_str = prefixX+"V%03d" % (cte_vix)
        sendMotorCommand(cmdx_str)
        print(cmdx_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        cmdy_str = prefixY+"V%03d" % (cte_viy)
        sendMotorCommand(cmdy_str)
        print(cmdy_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        cmdcomp_str = prefixComp+"V%03d" % (cte_vicomp)
        sendMotorCommand(cmdcomp_str)
        print(cmdcomp_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        # Find the indexes
        cmdx_str = prefixX+"GOIX"
        sendMotorCommand(cmdx_str)
        print(cmdx_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        cmdy_str = prefixY+"GOIX"
        sendMotorCommand(cmdy_str)
        print(cmdy_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        cmdcomp_str = prefixComp+"GOIX"
        sendMotorCommand(cmdcomp_str)
        print(cmdcomp_str)
        print(getMotorResponse())
        sendXportEnd()

    # Calculate the center position of the window over the FoV
    lsx_pos = cte_lsx_zero
    lsy_pos = cte_lsy_zero
    lscomp_pos = cte_lscomp_zero
    
    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        # Set center position as target for the movement
        cmdx_str = prefixX+"LA%05d" % (lsx_pos)
        sendMotorCommand(cmdx_str)
        print(cmdx_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        cmdy_str = prefixY+"LA%05d" % (lsy_pos)
        sendMotorCommand(cmdy_str)
        print(cmdy_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        cmdcomp_str = prefixComp+"LA%05d" % (lscomp_pos)
        sendMotorCommand(cmdcomp_str)
        print(cmdcomp_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        cmdx_str = prefixX+"V%03d" % (cte_vx)
        sendMotorCommand(cmdx_str)
        print(cmdx_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        cmdy_str = prefixY+"V%03d" % (cte_vy)
        sendMotorCommand(cmdy_str)
        print(cmdy_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        cmdcomp_str = prefixComp+"V%03d" % (cte_vcomp)
        sendMotorCommand(cmdcomp_str)
        print(cmdcomp_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        # Move the motor
        cmdx_str = prefixX+"M"
        sendMotorCommand(cmdx_str)
        print(cmdx_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        cmdy_str = prefixY+"M"
        sendMotorCommand(cmdy_str)
        print(cmdy_str)
        print(getMotorResponse())
        sendXportEnd()

    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        cmdcomp_str = prefixComp+"M"
        sendMotorCommand(cmdcomp_str)
        print(cmdcomp_str)
        print(getMotorResponse())
        sendXportEnd()

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
        if (sweepconfig.cte_use_motor_x):
            sendXportBegin(sweepconfig.cte_motor_x_xport)
            cmd_str = prefixX+"NP"
            sendMotorCommand(cmd_str)
            print("Cmd: "+ cmd_str)
            r=getMotorResponse()
            print("Resp:"+r)

            cmdx_str = prefixX+"LA%04d" % (lsx_pos)
            sendMotorCommand(cmdx_str)
            print(cmdx_str)
            r=getMotorResponse()
            print("Resp:"+r)
            sendXportEnd()

        if (sweepconfig.cte_use_motor_y):
            sendXportBegin(sweepconfig.cte_motor_y_xport)
            # Program the motor to warn when the command is done
            cmd_str = prefixY+"NP"
            sendMotorCommand(cmd_str)
            print(cmd_str)
            r=getMotorResponse()
            print("Resp:"+r)

            cmdy_str = prefixY+"LA%04d" % (lsy_pos)
            sendMotorCommand(cmdy_str)
            print(cmdy_str)
            r=getMotorResponse()
            print("Resp:"+r)
            sendXportEnd()

        if (sweepconfig.cte_use_motor_comp):
            sendXportBegin(sweepconfig.cte_motor_comp_xport)
            # Program the motor to warn when the command is done
            cmd_str = prefixComp+"NP"
            sendMotorCommand(cmd_str)
            print(cmd_str)
            r=getMotorResponse()
            print("Resp:"+r)

            cmdcomp_str = prefixComp+"LA%04d" % (lscomp_pos)
            sendMotorCommand(cmdcomp_str)
            print(cmdcomp_str)
            r=getMotorResponse()
            print("Resp:"+r)
            sendXportEnd()

        numberOfPToRx = 0
        numberOfOkToRx = 0

        if (sweepconfig.cte_use_motor_x):
            sendXportBegin(sweepconfig.cte_motor_x_xport)
            # Move the motor
            cmdx_str = prefixX+"M"
            sendMotorCommand(cmdx_str)
            print(cmdx_str)
            numberOfPToRx+=1
            numberOfOkToRx+=1
            r=getMotorResponse()
            print("Resp:"+r)
            if (r=="p"):
                numberOfPToRx -= 1
            if (r=="OK"):
                numberOfOkToRx -= 1
            print("Number of P to Rx: "+str(numberOfPToRx))
            sendXportEnd()

        if (sweepconfig.cte_use_motor_y):
            sendXportBegin(sweepconfig.cte_motor_y_xport)
            cmdy_str = prefixY+"M"
            sendMotorCommand(cmdy_str)
            print("Cmd:"+cmdy_str)
            numberOfPToRx += 1
            numberOfOkToRx += 1
            r=getMotorResponse()
            print("Resp:"+r)
            if (r=="p"):
                numberOfPToRx -= 1
            if (r=="OK"):
                numberOfOkToRx -= 1
            print("Number of P to Rx: " + str(numberOfPToRx))
            sendXportEnd()

        if (sweepconfig.cte_use_motor_comp):
            sendXportBegin(sweepconfig.cte_motor_comp_xport)
            cmdcomp_str = prefixComp+"M"
            sendMotorCommand(cmdcomp_str)
            print("Cmd:"+cmdcomp_str)
            numberOfPToRx += 1
            numberOfOkToRx+=1
            r=getMotorResponse()
            print("Resp:"+r)
            if (r=="p"):
                numberOfPToRx-=1
            if (r=="OK"):
                numberOfOkToRx-=1
            print("Number of P to Rx: " + str(numberOfPToRx))
            sendXportEnd()

        # Wait for command responses
        while  (numberOfPToRx>0 or numberOfOkToRx>0):
            print("Waiting "+str(numberOfPToRx)+" Motors to finish")
            r=getMotorResponse()
            print("Resp:"+r)
            if (r=="p"):
                numberOfPToRx-=1
            if (r=="OK"):
                numberOfOkToRx-=1
            print("Number of P to Rx: " + str(numberOfPToRx))

        if (numberOfPToRx==0):
            ret = 0
        else:
            ret = -1

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
    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        cmd_str = prefixX+"POS"
        sendMotorCommand(cmd_str)
        print("PosCmd:"+cmd_str)
        r=getMotorResponse()
        print("PosResp:"+r)
        mx_fdback=int(r)
        sendXportEnd()
    else:
        mx_fdback = -1

    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        cmd_str = prefixY+"POS"
        sendMotorCommand(cmd_str)
        print("PosCmd:"+cmd_str)
        r=getMotorResponse()
        print("PosResp:"+r)
        my_fdback=int(r)
        sendXportEnd()
    else:
        my_fdback = -1

    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        cmd_str = prefixComp+"POS"
        sendMotorCommand(cmd_str)
        print("PosCmd:"+cmd_str)
        r=getMotorResponse()
        print("PosResp:"+r)
        mcomp_fdback=int(r)
        sendXportEnd()
    else:
        mcomp_fdback = -1

    return mx_fdback, my_fdback, mcomp_fdback

def motorClose():
    if not(sweepconfig.cte_use_socket):
        ser.close()             # close port
    else:    
        sckt.close              # Close the socket when done    
