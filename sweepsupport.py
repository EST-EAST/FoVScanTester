import sweepconfig
import sys
sys.path.insert(0, './fsm')
import FoV

if sweepconfig.cte_use_cvcam:
    import cv2

########### XPORT SIDE #################


# Sends an escape char to clear the Xport channel
def resetXport():
    if sweepconfig.cte_use_socket:
        str = "" + chr(27)
        FoV.dre.ser.sendall(str)
        sendMotorCommand("@")
        r=getMotorResponse()


# Sends an XPort command, and process its response
# while waiting for the response, also processes the probable
# pending Ok's and P's
def sendXportCmd(str):
    global numberOfOkToRx
    global numberOfPToRx
    sendMotorCommand(str)
    print("XportCmd>" + str)
    done = False
    while not (done):
        r = getMotorResponse()
        print("XPortResponse>" + r + "< nothing?")
        done = (len(r) == 0)
        if not (done):
            processPendingResponse(r)


# Sends the addressing XPort command, and process it response
# while waiting for the response, also processes the probable
# pending Ok's and P's
def sendXportBegin(m):
    if (sweepconfig.cte_use_socket):
        cmd_str = "#" + str(m)
        sendXportCmd(cmd_str)


# Sends the END of addressing XPort command, and process it response
# while waiting for the response, also processes the probable
# pending Ok's and P's
def sendXportEnd():
    if (sweepconfig.cte_use_socket):
        cmd_str = "@"
        sendXportCmd(cmd_str)


########## COMM PROTOCOL #############


# Gets a response from the Motors
def getMotorResponse():
    FoV.getCtrlResponse()
    return FoV.dre.command_rx_buf


# Sends a command to the Motors
def sendMotorCommand(cmd_str):
    #ser.write(cmd_str+chr(13))
    print "Command sent: "+cmd_str
    FoV.dre.command_tx_buf = cmd_str
    FoV.sendCtrlCommand()


## PENDING RESPONSES SECTION ########

numberOfPToRx = 0       # Number of pending P responses
numberOfOkToRx = 0      # Number of pending Ok responses

# Processes the given response to decrement the pending Ok's and pending P's
def processPendingResponse(r):
    global numberOfOkToRx
    global numberOfPToRx
    print("Resp2:" + r)
    if (r == "p"):
        if sweepconfig.cte_wait_for_p:
            numberOfPToRx -= 1
    if (r == "OK"):
        numberOfOkToRx -= 1
    print("Number of pending P to Rx: " + str(numberOfPToRx))
    print("Number of pending Ok to Rx: " + str(numberOfOkToRx))


# Sets the number of pending responses to zero Ok's and zero P's
def resetPendingResponses():
    global numberOfOkToRx
    global numberOfPToRx
    numberOfPToRx = 0
    numberOfOkToRx = 0


# Reads a response and processes it, decrementing pending P's and pending Ok's
def consumeResponse():
    global numberOfOkToRx
    global numberOfPToRx
    r = getMotorResponse()
    processPendingResponse(r)


# Reads as many responses needed to receive all the pending Ok's
# While reading the responses, it also decrements the count of pending P's
def consumePendingOks():
    global numberOfOkToRx
    global numberOfPToRx
    while (numberOfOkToRx > 0):
        consumeResponse()
    if (numberOfOkToRx == 0):
        ret = 0
    else:
        ret = -1
    return ret


# Reads as many responses needed to receive all the pending P's
# While reading the responses, it also decrements the count of pending Ok's
def consumePendingPs():
    global numberOfOkToRx
    global numberOfPToRx
    if sweepconfig.cte_wait_for_p:
        while (numberOfPToRx > 0):
            consumeResponse()
        if (numberOfPToRx == 0):
            ret = 0
        else:
            ret = -1
    else:
        ret = 0
    return ret


# Increments the count of pending P responses
def incrementPendingP():
    global numberOfPToRx
    if sweepconfig.cte_wait_for_p:
        numberOfPToRx += 1


# Increments the count of pending Ok responses
def incrementPendingOk():
    global numberOfOkToRx
    numberOfOkToRx += 1


############ MOTOR ACTIONS SECTION #############

# Sends to Home the motor identified with the given index
def goHome(idx):
        # Programming the Home speeds
        cmd_str = prefixX+"HOSP-%3d" % (cte_vh[idx])
        sendMotorCommand(cmd_str)
        print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()

        cmd_str = prefixX+"APL0"
        sendMotorCommand(cmd_str)
        print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()

        if (sweepconfig.cte_command_np_flags):
            cmd_str = prefixX + "NP"
            sendMotorCommand(cmd_str)
            print("Command:"+cmd_str)
            incrementPendingOk()
            consumePendingOks()
            incrementPendingP()

        cmd_str = prefixX + "GOHOSEQ"
        sendMotorCommand(cmd_str)
        print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()
        consumePendingPs()

        cmd_str = prefixX+"HOSP%3d" % (cte_vi[idx])
        sendMotorCommand(cmd_str)
        print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()

        if (sweepconfig.cte_command_np_flags):
            cmd_str = prefixX + "NP"
            sendMotorCommand(cmd_str)
            print("Command:"+cmd_str)
            incrementPendingOk()
            consumePendingOks()
            incrementPendingP()

        cmd_str = prefixX + "GOIX"
        sendMotorCommand(cmd_str)
        print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()
        consumePendingPs()

        cmd_str = prefixX+"APL1"
        sendMotorCommand(cmd_str)
        print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()

        cmd_str = prefixX+"HOSP-%3d" % (cte_vh[idx])
        sendMotorCommand(cmd_str)
        print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()


# Sends to Home the motor assigned to X movements
def goHomeMx():
    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        goHome(sweepconfig.cte_motor_x - 1)
        sendXportEnd()


# Sends to Home the motor assigned to Y movements
def goHomeMy():
    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        goHome(sweepconfig.cte_motor_y - 1)
        sendXportEnd()


# Sends to Home the motor assigned to compensation movements
def goHomeMcomp():
    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        goHome(sweepconfig.cte_motor_comp - 1)
        sendXportEnd()

cte_tol_x = 10
cte_tol_y = 10
cte_tol_comp = 10

# Commands the window to x and y position (in mm from centered position)
# It calculates the needed commands for Mx, My and Mcomp motors and sends them.
def commandMotor(x, y):

    global current_pos_x
    global current_pos_y
    global current_pos_comp

    ret = 0
    # Compute compensation
    lscomp = (x + y) / 2
    # Compute LSX and LSY
    lsx_temp = cte_lsx_zero + (x * cte_lsx_scale)
    lsx_pos = max(min(lsx_temp, cte_lsx_max), cte_lsx_min)
    lsy_temp = cte_lsy_zero + (y * cte_lsy_scale)
    lsy_pos = max(min(lsy_temp, cte_lsy_max), cte_lsy_min)
    lscomp_temp = cte_lscomp_zero + (lscomp * cte_lscomp_scale)
    lscomp_pos = max(min(lscomp_temp, cte_lscomp_max), cte_lscomp_min)

    if (lsx_temp != lsx_pos or
                lsy_temp != lsy_pos or
                lscomp_temp != lscomp_pos):
        print "Error on calculating position: out of range of LS motors"
        print "X: %f Y: %f" % (x, y)
        print "LSX_TEMP: %.2f LSY_TEMP: %.2f LSCOMP_TEMP: %.2f" % (lsx_temp, lsy_temp, lscomp_temp)
        print "LSX_POS: %.2f LSY_POS: %.2f LSCOMP_POS: %.2f" % (lsx_pos, lsy_pos, lscomp_pos)
        ret = -1
    else:
        # send the commands

        # Program the motor to warn when the command is done
        if (sweepconfig.cte_use_motor_x):
            if (abs(lsx_pos-current_pos_x)>cte_tol_x):
                sendXportBegin(sweepconfig.cte_motor_x_xport)
    
                if (sweepconfig.cte_command_np_flags):
                    cmd_str = prefixX + "NP"
                    sendMotorCommand(cmd_str)
                    print("Command:" + cmd_str)
                    incrementPendingOk()
                    consumePendingOks()
                    incrementPendingP()
    
                cmd_str = prefixX + "LA%04d" % (lsx_pos)
                sendMotorCommand(cmd_str)
                print("Command:" + cmd_str)
                incrementPendingOk()
                consumePendingOks()
    
                # Move the motor
                cmd_str = prefixX + "M"
                sendMotorCommand(cmd_str)
                print("Command:" + cmd_str)
                incrementPendingOk()
                consumePendingOks()
    
                # Wait for command responses
                ret = consumePendingPs()
                sendXportEnd()
            else:
                print("Cancelo pues Pos actual: "+str(current_pos_x)+" parecida a orden: "+str(lsx_pos))

        if (sweepconfig.cte_use_motor_y):
            if (abs(lsy_pos-current_pos_y)>cte_tol_y):
                sendXportBegin(sweepconfig.cte_motor_y_xport)
    
                # Program the motor to warn when the command is done
                if (sweepconfig.cte_command_np_flags):
                    cmd_str = prefixY + "NP"
                    sendMotorCommand(cmd_str)
                    print("Command:" + cmd_str)
                    incrementPendingOk()
                    consumePendingOks()
                    incrementPendingP()
    
                cmd_str = prefixY + "LA%04d" % (lsy_pos)
                sendMotorCommand(cmd_str)
                print("Command:" + cmd_str)
                incrementPendingOk()
                consumePendingOks()
    
                cmd_str = prefixY + "M"
                sendMotorCommand(cmd_str)
                print("Command:" + cmd_str)
                incrementPendingOk()
                consumePendingOks()
    
                # Wait for command responses
                ret = consumePendingPs()
    
                sendXportEnd()
            else:
                print("Cancelo pues Pos actual: "+str(current_pos_y)+" parecida a orden: "+str(lsy_pos))

        if (sweepconfig.cte_use_motor_comp):
            if (abs(lscomp_pos-current_pos_comp)>cte_tol_comp):
                sendXportBegin(sweepconfig.cte_motor_comp_xport)
                # Program the motor to warn when the command is done
                if (sweepconfig.cte_command_np_flags):
                    cmd_str = prefixComp + "NP"
                    sendMotorCommand(cmd_str)
                    print("Command:" + cmd_str)
                    incrementPendingOk()
                    consumePendingOks()
                    incrementPendingP()
    
                cmd_str = prefixComp + "LA%04d" % (lscomp_pos)
                sendMotorCommand(cmd_str)
                print("Command:" + cmd_str)
                incrementPendingOk()
                consumePendingOks()
    
                cmd_str = prefixComp + "M"
                sendMotorCommand(cmd_str)
                print("Command:" + cmd_str)
                incrementPendingOk()
                consumePendingOks()
    
                # Wait for command responses
                ret = consumePendingPs()
    
                sendXportEnd()
            else:
                print("Cancelo pues Pos actual: "+str(current_pos_comp)+" parecida a orden: "+str(lscomp_pos))


    return ret, lsx_pos, lsy_pos, lscomp_pos


# Commands home for all the motors, and then puts the window at the central position.
def resetMotors():
    goHomeMx()
    goHomeMy()
    goHomeMcomp()

    # Calculate the center position of the window over the FoV
    lsx_pos = cte_lsx_zero
    lsy_pos = cte_lsy_zero
    lscomp_pos = cte_lscomp_zero
    
    commandMotor(0.0, 0.0)


# Disables the motors
def disableMotors():
    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        cmd_str = prefixX + "DI"
        sendMotorCommand(cmd_str)
        print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()

    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        cmd_str = prefixY + "DI"
        sendMotorCommand(cmd_str)
        print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()


    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        cmd_str = prefixComp + "DI"
        sendMotorCommand(cmd_str)
        print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()

# Disables the motors
def enableMotors():
    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        cmd_str = prefixX + "EN"
        sendMotorCommand(cmd_str)
        print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()

    if (sweepconfig.cte_use_motor_y):
        sendXportBegin(sweepconfig.cte_motor_y_xport)
        cmd_str = prefixY + "EN"
        sendMotorCommand(cmd_str)
        print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()


    if (sweepconfig.cte_use_motor_comp):
        sendXportBegin(sweepconfig.cte_motor_comp_xport)
        cmd_str = prefixComp + "EN"
        sendMotorCommand(cmd_str)
        print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()


cte_waitTime = 1
cte_stepTime = cte_waitTime * 1000     # Time to wait between steps, apart from motors and camera ones


# Waits for a defined time for user to press a key
def waitKey(t):
    '''
    import time, msvcrt
    startTime=time.time()

    print "Press any key or wait "+str(cte_waitTime)+" seconds"
    done = False
    ret = -1
    while not(done):
        if msvcrt.kbhit():
            ret=msvcrt.getch()
            done = True
        elif time.time() - startTime > t:
            done = True
    return ret
    '''
    return -1


# Checks if the sweep step has been done.  It also returns if the sweep has to be cancelled
def stepDone():
    # Wait for command or step time
    # it returns True if nobody presses the ESC
    if (sweepconfig.cte_use_cvcam):
        key = cv2.waitKey(cte_stepTime)
    else:
        key = waitKey(cte_waitTime)
    if (key == 27):
        # Someone presses the ESC key, should return
        ret = -1
    else:
        if (key == -1):
            # Time expired
            ret = 1
        else:
            # Another key presssed
            ret=0

    return ret

current_pos_x = 0
current_pos_y = 0
current_pos_comp = 0

# Retrieves the position for each motor
def motorPositions():
    global current_pos_x
    global current_pos_y
    global current_pos_comp
    
    # Obtain final positions
    if (sweepconfig.cte_use_motor_x):
        sendXportBegin(sweepconfig.cte_motor_x_xport)
        cmd_str = prefixX+"POS"
        sendMotorCommand(cmd_str)
        print("PosCmd:"+cmd_str)
        r=getMotorResponse()
        print("PosResp:"+r)
        mx_fdback=int(r)
        current_pos_x = mx_fdback
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
        current_pos_y = my_fdback
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
        current_pos_comp = mcomp_fdback
        sendXportEnd()
    else:
        mcomp_fdback = -1

    return mx_fdback, my_fdback, mcomp_fdback


# Closes the communication with the motors
def motorClose():
    if not(sweepconfig.cte_use_socket):
        ser.close()             # close port
    else:    
        sckt.close              # Close the socket when done    


########### WINDOW TO MOTORS DEFINITIONS ################

# Mx = x
cte_lsx_min = 0  # End of LS travel in lower units
cte_lsx_scale = -(1000 * 1000)  # LS units / mm * 1000 mm / 1 m
cte_lsx_max = 0.030 * (-cte_lsx_scale)  # End of LS travel in upper units
cte_lsx_zero = (cte_lsx_max / 2)  # LS units coincidence with 0 mm (center)

# My = y
cte_lsy_min = 0  # End of LS travel in lower units
cte_lsy_scale = (2000 * 1000)  # LS units / mm * 1000 mm / 1 m
cte_lsy_max = 0.020 * (cte_lsy_scale)  # End of LS travel in upper units
cte_lsy_zero = (cte_lsy_max / 2)  # LS units coincidence with 0 mm (center)

# Mcomp = compensaTion
cte_lscomp_min = 0  # End of LS travel in lower units
cte_lscomp_scale = -(2000 * 1000)  # LS units / mm * 1000 mm / 1 m
cte_lscomp_max = 0.020 * (-cte_lscomp_scale)  # End of LS travel in upper units
cte_lscomp_zero = (cte_lscomp_max / 2)  # LS units coincidence with 0 mm (center)

# Home speeds
cte_vhx = 100
cte_vhy = 100
cte_vhcomp = 100

cte_vh = [cte_vhx, cte_vhy, cte_vhcomp]

# Index speeds
cte_vix = 30
cte_viy = 30
cte_vicomp = 30

cte_vi = [cte_vix, cte_viy, cte_vicomp]

# Movement speeds
cte_vx = 100
cte_vy = 100
cte_vcomp = 100

cte_v = [cte_vh, cte_vh, cte_vcomp]

# Calculated positions for each linear stage
lsx_pos = 0.0
lsy_pos = 0.0
lscomp_pos = 0.0

########### MAIN INITIALIZATIONS ###############

# Indicates to the DRE (fsm data base) which kind of connection must be used
FoV.dre.cte_use_socket = sweepconfig.cte_use_socket

# Opens the communication channel
if not (sweepconfig.cte_use_socket):
    import serial

    cte_serial_port = sweepconfig.cte_serial_port
    print "Chosen serial port: " + cte_serial_port
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
    resetPendingResponses()
else:
    import socket  # Import socket module

    sckt = socket.socket()  # Create a socket object
    sckt.connect((sweepconfig.cte_socket_ip, sweepconfig.cte_socket_port))
    FoV.dre.ser = sckt
    resetXport()
    resetPendingResponses()

if (sweepconfig.cte_use_socket):
    prefixX = ""
    prefixY = ""
    prefixComp = ""
else:
    prefixX = str(sweepconfig.cte_motor_x)
    prefixY = str(sweepconfig.cte_motor_y)
    prefixComp = str(sweepconfig.cte_motor_comp)
