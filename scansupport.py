import scanconfig
import sys
from time import sleep
from scancalib import *
from BitManipulation import *

sys.path.insert(0, './fsm')
import FoV

if scanconfig.cte_use_cvcam:
    import cv2

# ########## XPORT SIDE #################


# Sends an escape char to clear the Xport channel
def resetXport():
    if scanconfig.cte_use_socket:
        st = "" + chr(27)
        FoV.dre.ser.sendall(st)
        sendMotorCommand("@")
        r = getMotorResponse()


# Sends an XPort command, and process its response
# while waiting for the response, also processes the probable
# pending Ok's and P's
def sendXportCmd(st):
    global numberOfOkToRx
    global numberOfPToRx
    sendMotorCommand(st)
    if scanconfig.cte_verbose:
        print("XportCmd>" + st)
    done = False
    while not done:
        r = getMotorResponse()
        if scanconfig.cte_verbose:
            print("XPortResponse>" + r + "< nothing?")
        done = (len(r) == 0)
        if not done:
            processPendingResponse(r)


# Sends the addressing XPort command, and process it response
# while waiting for the response, also processes the probable
# pending Ok's and P's
def sendXportBegin(m):
    if scanconfig.cte_use_socket:
        cmd_str = "#" + str(m)
        sendXportCmd(cmd_str)


# Sends the END of addressing XPort command, and process it response
# while waiting for the response, also processes the probable
# pending Ok's and P's
def sendXportEnd():
    if scanconfig.cte_use_socket:
        cmd_str = "@"
        sendXportCmd(cmd_str)


# ######### COMM PROTOCOL #############


# Gets a response from the Motors
def getMotorResponse():
    FoV.getCtrlResponse()
    return FoV.dre.command_rx_buf


# Sends a command to the Motors
def sendMotorCommand(cmd_str):
    # ser.write(cmd_str+chr(13))
    if scanconfig.cte_verbose:
        print "Command sent: "+cmd_str
    FoV.dre.command_tx_buf = cmd_str
    FoV.sendCtrlCommand()


# # PENDING RESPONSES SECTION ########

numberOfPToRx = 0       # Number of pending P responses
numberOfOkToRx = 0      # Number of pending Ok responses


# Processes the given response to decrement the pending Ok's and pending P's
def processPendingResponse(r):
    global numberOfOkToRx
    global numberOfPToRx
    if scanconfig.cte_verbose:
        print("Resp2:" + r)
    if r == "p":
        if scanconfig.cte_wait_for_p:
            numberOfPToRx -= 1
    if r == "OK":
        numberOfOkToRx -= 1
    if scanconfig.cte_verbose:
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
    while numberOfOkToRx > 0:
        consumeResponse()
    if numberOfOkToRx == 0:
        ret = 0
    else:
        ret = -1
    return ret


# Reads as many responses needed to receive all the pending P's
# While reading the responses, it also decrements the count of pending Ok's
def consumePendingPs():
    global numberOfOkToRx
    global numberOfPToRx
    if scanconfig.cte_wait_for_p:
        while numberOfPToRx > 0:
            consumeResponse()
        if numberOfPToRx == 0:
            ret = 0
        else:
            ret = -1
    else:
        ret = 0
    return ret


# Increments the count of pending P responses
def incrementPendingP():
    global numberOfPToRx
    if scanconfig.cte_wait_for_p:
        numberOfPToRx += 1


# Increments the count of pending Ok responses
def incrementPendingOk():
    global numberOfOkToRx
    if scanconfig.cte_mode_answ == 2:
        numberOfOkToRx += 1
# Just for documentation:   
# if scanconfig.cte_mode_answ == 1:
#        numberOfOkToRx += 0


############ MOTOR ACTIONS SECTION #############

# Sends to Home the motor identified with the given index
def goHome(idx):
        # Programming the Home speeds
        cmd_str = prefixX+"HOSP-%3d" % (cte_vh[idx])
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()

        cmd_str = prefixX+"APL0"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()

        if scanconfig.cte_command_np_flags:
            cmd_str = prefixX + "NP"
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("Command:"+cmd_str)
            incrementPendingOk()
            consumePendingOks()
            incrementPendingP()

        cmd_str = prefixX + "GOHOSEQ"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()
        consumePendingPs()

        cmd_str = prefixX+"HOSP%3d" % (cte_vi[idx])
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()

        if scanconfig.cte_command_np_flags:
            cmd_str = prefixX + "NP"
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("Command:"+cmd_str)
            incrementPendingOk()
            consumePendingOks()
            incrementPendingP()

        cmd_str = prefixX + "GOIX"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()
        consumePendingPs()

        cmd_str = prefixX+"APL1"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()

        cmd_str = prefixX+"HOSP-%3d" % (cte_vh[idx])
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:"+cmd_str)
        incrementPendingOk()
        consumePendingOks()


# Sends to Home the motor assigned to X movements
def goHomeMx():
    if scanconfig.cte_use_motor_x:
        sendXportBegin(scanconfig.cte_motor_x_xport)
        goHome(scanconfig.cte_motor_x - 1)
        sendXportEnd()


# Sends to Home the motor assigned to Y movements
def goHomeMy():
    if scanconfig.cte_use_motor_y:
        sendXportBegin(scanconfig.cte_motor_y_xport)
        goHome(scanconfig.cte_motor_y - 1)
        sendXportEnd()


# Sends to Home the motor assigned to compensation movements
def goHomeMcomp():
    if scanconfig.cte_use_motor_comp:
        sendXportBegin(scanconfig.cte_motor_comp_xport)
        goHome(scanconfig.cte_motor_comp - 1)
        sendXportEnd()


# Commands a new position to LSx
def commandLSx(setpoint, blocking = True):
    # Program the motor to warn when the command is done
    if scanconfig.cte_use_motor_x:
        if abs(setpoint - current_pos_x) > cte_tol_x:
            sendXportBegin(scanconfig.cte_motor_x_xport)

            if scanconfig.cte_command_np_flags and blocking:
                cmd_str = prefixX + "NP"
                sendMotorCommand(cmd_str)
                if scanconfig.cte_verbose:
                    print("Command:" + cmd_str)
                incrementPendingOk()
                consumePendingOks()
                incrementPendingP()

            cmd_str = prefixX + "LA%04d" % setpoint
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("Command:" + cmd_str)
            incrementPendingOk()
            consumePendingOks()

            # Move the motor
            cmd_str = prefixX + "M"
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("Command:" + cmd_str)
            incrementPendingOk()
            consumePendingOks()

            # Wait for command responses
            if blocking:
                ret = consumePendingPs()
                
            sendXportEnd()
        else:
            if scanconfig.cte_verbose:
                print("Cancelled actuation.  Current pos: " + str(current_pos_x) +
                      " too much close to new command: " + str(setpoint))


# Commands a new position to LSy
def commandLSy(setpoint, blocking = True):
    if scanconfig.cte_use_motor_y:
        if abs(setpoint - current_pos_y) > cte_tol_y:
            sendXportBegin(scanconfig.cte_motor_y_xport)

            # Program the motor to warn when the command is done
            if scanconfig.cte_command_np_flags and blocking:
                cmd_str = prefixY + "NP"
                sendMotorCommand(cmd_str)
                if scanconfig.cte_verbose:
                    print("Command:" + cmd_str)
                incrementPendingOk()
                consumePendingOks()
                incrementPendingP()

            cmd_str = prefixY + "LA%04d" % setpoint
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("Command:" + cmd_str)
            incrementPendingOk()
            consumePendingOks()

            cmd_str = prefixY + "M"
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("Command:" + cmd_str)
            incrementPendingOk()
            consumePendingOks()

            # Wait for command responses
            if blocking:
                ret = consumePendingPs()

            sendXportEnd()
        else:
            if scanconfig.cte_verbose:
                print("Cancelled actuation.  Current pos: " + str(current_pos_y) +
                      " too much close to new command: " + str(setpoint))


# Commands a new position to LScomp
def commandLScomp(setpoint, blocking = True):
    if scanconfig.cte_use_motor_comp:
        if abs(setpoint - current_pos_comp) > cte_tol_comp:
            sendXportBegin(scanconfig.cte_motor_comp_xport)
            # Program the motor to warn when the command is done
            if scanconfig.cte_command_np_flags and blocking:
                cmd_str = prefixComp + "NP"
                sendMotorCommand(cmd_str)
                if scanconfig.cte_verbose:
                    print("Command:" + cmd_str)
                incrementPendingOk()
                consumePendingOks()
                incrementPendingP()

            cmd_str = prefixComp + "LA%04d" % setpoint
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("Command:" + cmd_str)
            incrementPendingOk()
            consumePendingOks()

            cmd_str = prefixComp + "M"
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("Command:" + cmd_str)
            incrementPendingOk()
            consumePendingOks()

            # Wait for command responses
            if blocking:
                ret = consumePendingPs()

            sendXportEnd()
        else:
            if scanconfig.cte_verbose:
                print("Cancelled actuation.  Current pos: " + str(current_pos_comp) +
                      " too much close to new command: " + str(setpoint))


# Commands the window to x, y and z positions (already filtered).
# DO NOT USE THIS FUNCTION DIRECTLY, USE commandMotorUnits3D or commandMotor ones.
def commandMotorInternalStep(lsx_pos, lsy_pos, lscomp_pos,
                             enable_lsx=True, enable_lsy=True, enable_lscomp=True):
    if enable_lsx:
        xDict = {'Name': 'x', 'Function': commandLSx, 'Argument': lsx_pos,
                 'Delta': abs(lsx_pos - current_pos_x) / (float(cte_vx) / 100.0),
                 'Blocking': False}

    if enable_lsy:
        yDict = {'Name': 'y', 'Function': commandLSy, 'Argument': lsy_pos,
                 'Delta': abs(lsy_pos - current_pos_y) / (float(cte_vy) / 100.0),
                 'Blocking': False}

    if enable_lscomp:
        compDict = {'Name': 'comp', 'Function': commandLScomp, 'Argument': lscomp_pos,
                    'Delta': abs(lscomp_pos - current_pos_comp) / (float(cte_vcomp) / 100.0),
                    'Blocking': False}

    if scanconfig.cte_force_wait_for_motor == 0:
        # reordDict = [xDict, yDict, compDict]
        reordDict=[]
        if enable_lsx:
            reordDict += [xDict]
        if enable_lsy:
            reordDict += [yDict]
        if enable_lscomp:
            reordDict += [compDict]
        # sort the commands
        newlist = sorted(reordDict, key=lambda k: k['Delta'])
    else:
        newlist = []
        if scanconfig.cte_force_wait_for_motor == 1:
            # Manual sort
            # newlist = [yDict, compDict, xDict]
            if enable_lsy:
                newlist += [yDict]
            if enable_lscomp:
                newlist += [compDict]
            if enable_lsx:
                newlist += [xDict]
        else:
            if scanconfig.cte_force_wait_for_motor == 2:
                # Manual sort
                # newlist = [xDict, compDict, yDict]
                if enable_lsx:
                    newlist += [xDict]
                if enable_lscomp:
                    newlist += [compDict]
                if enable_lsy:
                    newlist += [yDict]
            else:
                if scanconfig.cte_force_wait_for_motor >= 3:
                    # Manual sort
                    # newlist = [xDict, yDict, compDict]
                    if enable_lsx:
                        newlist += [xDict]
                    if enable_lsy:
                        newlist += [yDict]
                    if enable_lscomp:
                        newlist += [compDict]

    # Last command of the list must be the 'blocking' one
    newlist[len(newlist) - 1]['Blocking'] = True
    # Explore the list and send the commands
    for func in newlist:
        print("Ord: " + func['Name'] + ", Delta:" + str(func['Delta']) + ", blocking:" + str(
            func['Blocking']))
        (func['Function'])(func['Argument'], func['Blocking'])

    return 0


# Decide if a there is the need of execute a previous step due to backslash corrections
def backSlashPresent():
    return (cte_backslash_comp_correction_enable or cte_backslash_x_correction_enable or
            cte_backslash_y_correction_enable)


# Calculates the backslash previous step for a given X coordinate
def calculateBackslashStepX(stepXcoord):
    if cte_backslash_x_correction_enable:
        # The x movement has backslash
        backslash_correction = cte_backslash_x_correction_delta
        if cte_backslash_x_correction_direction == CTE_DIRECTION_POSITIVE:
            newStepXcoord = stepXcoord - backslash_correction
        else:
            newStepXcoord = stepXcoord + backslash_correction
    else:
        newStepXcoord = stepXcoord

    return newStepXcoord


# Calculates the backslash previous step for a given Y coordinate
def calculateBackslashStepY(stepYcoord):
    if cte_backslash_y_correction_enable:
        # The y movement has backslash
        backslash_correction = cte_backslash_y_correction_delta
        if cte_backslash_y_correction_direction == CTE_DIRECTION_POSITIVE:
            newStepYcoord = stepYcoord - backslash_correction
        else:
            newStepYcoord = stepYcoord + backslash_correction
    else:
        newStepYcoord = stepYcoord

    return newStepYcoord


# Calculates the backslash previous step for a given Z coordinate
def calculateBackslashStepZ(stepZcoord):
    if cte_backslash_y_correction_enable:
        # The y movement has backslash
        backslash_correction = cte_backslash_comp_correction_delta
        if cte_backslash_y_correction_direction == CTE_DIRECTION_POSITIVE:
            newStepZcoord = stepZcoord - backslash_correction
        else:
            newStepZcoord = stepZcoord + backslash_correction
    else:
        newStepZcoord = stepZcoord

    return newStepZcoord


def calculateBackslashStep(stepXcoord, stepYcoord, stepZcoord):
    backslash_step_x = calculateBackslashStepX(stepXcoord)
    backslash_step_y = calculateBackslashStepY(stepYcoord)
    backslash_step_z = calculateBackslashStepZ(stepZcoord)
    return backslash_step_x, backslash_step_y, backslash_step_z


def calculateBackslashStepXY(x, y):
    # Compute compensation
    lscomp = ((cte_comp_factor_x * x) + (cte_comp_factor_x * y)) / cte_comp_divisor
    # Compute LSX and LSY
    lsx_temp = cte_lsx_zero + (x * cte_lsx_scale)
    lsx_pos = max(min(lsx_temp, cte_lsx_max), cte_lsx_min)
    lsy_temp = cte_lsy_zero + (y * cte_lsy_scale)
    lsy_pos = max(min(lsy_temp, cte_lsy_max), cte_lsy_min)
    lscomp_temp = cte_lscomp_zero + (lscomp * cte_lscomp_scale)
    lscomp_pos = max(min(lscomp_temp, cte_lscomp_max), cte_lscomp_min)

    backslash_step_x = calculateBackslashStepX(lsx_pos)
    backslash_step_y = calculateBackslashStepY(lsy_pos)
    backslash_step_z = calculateBackslashStepZ(lscomp_pos)
    return backslash_step_x, backslash_step_y, backslash_step_z


# Commands the window to x, y and z positions (already filtered).
# DO NOT USE THIS FUNCTION DIRECTLY, USE commandMotorUnits3D or commandMotor ones.
def commandMotorInternal(x, y, lsx_pos, lsx_temp, lsy_pos, lsy_temp, lscomp_pos, lscomp_temp,
                         enable_lsx=True, enable_lsy=True, enable_lscomp=True):

    ret = 0
    if scanconfig.cte_verbose:
        print("Waiting delay time between steps")
    sleep(scanconfig.cte_step_delay_time)

    if lsx_temp != lsx_pos or lsy_temp != lsy_pos or lscomp_temp != lscomp_pos:
        print "Error on calculating position: out of range of LS motors"
        if scanconfig.cte_verbose:
            print "X: %f Y: %f" % (x, y)
            print "LSX_TEMP: %.2f LSY_TEMP: %.2f LSCOMP_TEMP: %.2f" % (lsx_temp, lsy_temp, lscomp_temp)
            print "LSX_POS: %.2f LSY_POS: %.2f LSCOMP_POS: %.2f" % (lsx_pos, lsy_pos, lscomp_pos)

        ret = -1
    else:
        if backSlashPresent():
            correctionNeeded = False
            backslash_lsx_pos = lsx_pos
            backslash_lsy_pos = lsy_pos
            backslash_lscomp_pos = lscomp_pos
            # Let's calculate the correction step, and execute it
            if cte_backslash_x_correction_enable:
                # The x movement has backslash
                # Decide if this step is in the "unprivileged" direction
                if cte_backslash_x_correction_direction == CTE_DIRECTION_POSITIVE:
                    if lsx_pos < current_pos_x:
                        correctionNeeded = True
                        backslash_lsx_pos = calculateBackslashStepX(lsx_pos)

                else:
                    if lsx_pos > current_pos_x:
                        correctionNeeded = True
                        backslash_lsx_pos = calculateBackslashStepX(lsx_pos)

            if cte_backslash_y_correction_enable:
                # The y movement has backslash
                # Decide if this step is in the "unprivileged" direction
                if cte_backslash_y_correction_direction == CTE_DIRECTION_POSITIVE:
                    if lsy_pos < current_pos_y:
                        correctionNeeded = True
                        backslash_lsy_pos = calculateBackslashStepY(lsy_pos)
                else:
                    if lsy_pos > current_pos_y:
                        correctionNeeded = True
                        backslash_lsy_pos = calculateBackslashStepY(lsy_pos)

            if cte_backslash_comp_correction_enable:
                # The comp movement has backslash
                # Decide if this step is in the "unprivileged" direction
                if cte_backslash_comp_correction_direction == CTE_DIRECTION_POSITIVE:
                    if lscomp_pos < current_pos_comp:
                        correctionNeeded = True
                        backslash_lscomp_pos = calculateBackslashStepZ(lscomp_pos)
                else:
                    if lscomp_pos > current_pos_comp:
                        correctionNeeded = True
                        backslash_lscomp_pos = calculateBackslashStepZ(lscomp_pos)

            if correctionNeeded:
                print ("***************** WE INTRODUCE A BACKSLASH STEP *************************")
                print "lsx_pos: %.6f, lsy_pos: %.6f lscomp_pos: %.6f" % (lsx_pos, lsy_pos, lscomp_pos)
                print "backslash_lsx_pos: %.6f, backslash_lsy_pos: %.6f backslash_lscomp_pos: %.6f" % \
                      (backslash_lsx_pos, backslash_lsy_pos, backslash_lscomp_pos)
                # Let's perform the backslash correction step
                ret = commandMotorInternalStep(backslash_lsx_pos, backslash_lsy_pos, backslash_lscomp_pos,
                                               enable_lsx, enable_lsy, enable_lscomp)

        # Let's perform the scanning step
        ret = commandMotorInternalStep(lsx_pos, lsy_pos, lscomp_pos,
                                       enable_lsx, enable_lsy, enable_lscomp)
    return ret


# Commands the window to x and y position (in raw motor units)
# It calculates the needed commands for Mx, My and Mcomp motors and sends them.
def commandMotorUnits3D(x, y, z):
    # Set LSX, LSY, LSCOMP "as is" (no computation)
    lsx_temp = x
    lsx_pos = max(min(lsx_temp, cte_lsx_max), cte_lsx_min)
    lsy_temp = y
    lsy_pos = max(min(lsy_temp, cte_lsy_max), cte_lsy_min)
    lscomp_temp = z
    lscomp_pos = max(min(lscomp_temp, cte_lscomp_max), cte_lscomp_min)
    print "lsx_pos: %.6f, lsy_pos: %.6f lscomp_pos: %.6f" % (lsx_pos, lsy_pos, lscomp_pos)

    ret = commandMotorInternal(x, y, lsx_pos, lsx_temp, lsy_pos, lsy_temp, lscomp_pos, lscomp_temp)

    return ret, lsx_pos, lsy_pos, lscomp_pos


def commandMotorUnits2D(xMot, yMot):
    x = (xMot - cte_lsx_zero) / cte_lsx_scale
    y = (yMot - cte_lsy_zero) / cte_lsy_scale
    print "commandMotorUnits2D x: %.6f y: %.6f" % (x, y)
    ret, lsx_pos, lsy_pos, lscomp_pos = commandMotor(x, y)

import dcpwrapper

def sendGcsTcpCommand( command_tx_buf ):
    FoV.dre.ser.sendall(command_tx_buf+chr(13))

gcs_pos_x = 0
gcs_pos_y = 0

# Commands the window to x and y position (in mm from centered position)
# It calculates the needed commands for Mx, My and Mcomp motors and sends them.
def commandMotor(x, y, initial_step = False):
    global gcs_pos_x
    global gcs_pos_y

    if scanconfig.cte_command_gcs:
        if initial_step:
            gcs_pos_x = 0
            gcs_pos_y = 0
            
        gcs_jump_y = (y * scanconfig.cte_command_gcs_scale) - gcs_pos_y
        gcs_jump_x = (x * scanconfig.cte_command_gcs_scale) - gcs_pos_x
        gcs_pos_y += gcs_jump_y
        gcs_pos_x += gcs_jump_x
        gcs_command_str = "5000 IFU set position rel FM1 0 " + str(gcs_jump_y) + " " + str(gcs_jump_x)
        print ">>GCSTCP: " + gcs_command_str
        sendGcsTcpCommand(gcs_command_str)
        response = getGcsTcpResponse()
        response_list = response.split()
        response_code = int(response_list[0])
        if (response_code == 0):
            print ("OK")
            lsx_pos = int(response_list[2])
            lsy_pos = int(response_list[1])
            lscomp_pos = int(response_list[3])
            ret = 0
        else:
            if (response_code > 0):
                print ("ERROR: "+ response_list[0])
                lsx_pos = 0
                lsy_pos = 0
                lscomp_pos = 0
                ret = -1
                
            else:
                print ("WARNING: "+ response_list[0])
                lsx_pos = int(response_list[2])
                lsy_pos = int(response_list[1])
                lscomp_pos = int(response_list[3])
                ret = 0

        print ("lsy_pos " + str(lsy_pos))
        print ("lsx_pos " + str(lsx_pos))
        print ("lscomp_pos " + str(lscomp_pos))
    else:
        # Compute compensation
        lscomp = ((cte_comp_factor_x * x) + (cte_comp_factor_x * y)) / cte_comp_divisor
        # Compute LSX and LSY
        lsx_temp = cte_lsx_zero + (x * cte_lsx_scale)
        lsx_pos = max(min(lsx_temp, cte_lsx_max), cte_lsx_min)
        lsy_temp = cte_lsy_zero + (y * cte_lsy_scale)
        lsy_pos = max(min(lsy_temp, cte_lsy_max), cte_lsy_min)
        lscomp_temp = cte_lscomp_zero + (lscomp * cte_lscomp_scale)
        lscomp_pos = max(min(lscomp_temp, cte_lscomp_max), cte_lscomp_min)

        ret = commandMotorInternal(x, y, lsx_pos, lsx_temp, lsy_pos, lsy_temp, lscomp_pos, lscomp_temp)

    return ret, lsx_pos, lsy_pos, lscomp_pos


# For a given X,Y window position, it computes the compensation, but only commands the compensation motor
def commandMotorComp(x, y):
    ret = 0
    # Compute compensation
    lscomp = ((cte_comp_factor_x * x) + (cte_comp_factor_x * y)) / cte_comp_divisor
    # Compute LSX and LSY
    lsx_temp = cte_lsx_zero + (x * cte_lsx_scale)
    lsx_pos = max(min(lsx_temp, cte_lsx_max), cte_lsx_min)
    lsy_temp = cte_lsy_zero + (y * cte_lsy_scale)
    lsy_pos = max(min(lsy_temp, cte_lsy_max), cte_lsy_min)
    lscomp_temp = cte_lscomp_zero + (lscomp * cte_lscomp_scale)
    lscomp_pos = max(min(lscomp_temp, cte_lscomp_max), cte_lscomp_min)

    ret = commandMotorInternal(x, y, lsx_pos, lsx_temp, lsy_pos, lsy_temp, lscomp_pos, lscomp_temp,
                               False, False, True)

    return ret, lsx_pos, lsy_pos, lscomp_pos


# Commands the window to x and y position (in mm from centered position)
# It calculates the needed commands for Mx, My and Mcomp motors and sends them.
def commandMotorWindow(x, y):
    ret = 0
    # Compute compensation
    lscomp = ((cte_comp_factor_x * x) + (cte_comp_factor_x * y)) / cte_comp_divisor
    # Compute LSX and LSY
    lsx_temp = cte_lsx_zero + (x * cte_lsx_scale)
    lsx_pos = max(min(lsx_temp, cte_lsx_max), cte_lsx_min)
    lsy_temp = cte_lsy_zero + (y * cte_lsy_scale)
    lsy_pos = max(min(lsy_temp, cte_lsy_max), cte_lsy_min)
    lscomp_temp = cte_lscomp_zero + (lscomp * cte_lscomp_scale)
    lscomp_pos = max(min(lscomp_temp, cte_lscomp_max), cte_lscomp_min)

    ret = commandMotorInternal(x, y, lsx_pos, lsx_temp, lsy_pos, lsy_temp, lscomp_pos, lscomp_temp,
                               True, True, False)

    return ret, lsx_pos, lsy_pos, lscomp_pos


# Commands all motors to their home positions
def homeMotors():
    if not scanconfig.cte_command_gcs:    
        goHomeMx()
        goHomeMy()
        goHomeMcomp()


# Commands home for all the motors, and then puts the window at the central position.
def resetMotors():
    homeMotors()

    # Calculate the center position of the window over the FoV
    lsx = 0.0
    lsy = 0.0

    print("lsx: "+str(lsx))
    print("lsy: "+str(lsy))
    
    commandMotor(lsx, lsy)


# Commands home for only the window motors (X and Y), and then puts the window at the central position, ignoring
# compensation motor movements
def resetMotorsWindow():
    goHomeMx()
    goHomeMy()

    # Calculate the center position of the window over the FoV
    lsx = 0.0
    lsy = 0.0

    print("lsx: "+str(lsx))
    print("lsy: "+str(lsy))
    
    commandMotorWindow(lsx, lsy)


# Commands home for compensation motor, and then moves the compensation to its zero position
def resetMotorsComp():
    goHomeMcomp()

    # Calculate the center position of the window over the FoV
    lsx = 0.0
    lsy = 0.0

    print("lsx: "+str(lsx))
    print("lsy: "+str(lsy))
    
    commandMotorComp(lsx, lsy)


# Disables the motors
def disableMotors():
    if scanconfig.cte_use_motor_x:
        sendXportBegin(scanconfig.cte_motor_x_xport)
        cmd_str = prefixX + "DI"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()

    if scanconfig.cte_use_motor_y:
        sendXportBegin(scanconfig.cte_motor_y_xport)
        cmd_str = prefixY + "DI"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()

    if scanconfig.cte_use_motor_comp:
        sendXportBegin(scanconfig.cte_motor_comp_xport)
        cmd_str = prefixComp + "DI"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()


# Disables the motors
def enableMotors():
    if scanconfig.cte_use_motor_x:
        sendXportBegin(scanconfig.cte_motor_x_xport)
        cmd_str = prefixX + "EN"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()

    if scanconfig.cte_use_motor_y:
        sendXportBegin(scanconfig.cte_motor_y_xport)
        cmd_str = prefixY + "EN"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()

    if scanconfig.cte_use_motor_comp:
        sendXportBegin(scanconfig.cte_motor_comp_xport)
        cmd_str = prefixComp + "EN"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("Command:" + cmd_str)
        incrementPendingOk()
        consumePendingOks()
        sendXportEnd()


# Waits for a defined time for user to press a key
def waitKey(t):
    if cte_waitTime > 0 or scanconfig.cte_step_wait_for_key:
        import time
        startTime = time.time()

        if scanconfig.cte_step_wait_for_key:
            import os
            if os.name == 'nt':
                import msvcrt
                print "waiting for key"
            else:
                from getch import pause
                pause('Waiting for key')
        else:
            print "waiting "+str(cte_waitTime)+" seconds"

        done = False
        ret = -1
        while not done:
            if scanconfig.cte_step_wait_for_key:
                if os.name == 'nt':
                    if msvcrt.kbhit():
                        ret = msvcrt.getch()
                        done = True

                else:
                    done = True

            elif time.time() - startTime > t:
                done = True

        return ret
    else:
        return -1


# Checks if the scan step has been done.  It also returns if the scan has to be cancelled
def stepDone():

    global mx_finished
    global my_finished
    global mcomp_finished
 
    # Wait for command or step time
    # it returns True if nobody presses the ESC
    if scanconfig.cte_use_cvcam:
        key = cv2.waitKey(cte_stepTime)
    else:
        key = waitKey(cte_waitTime)
    if key == 27:
        # Someone presses the ESC key, should return
        ret = -1
    else:
        if (key == -1) or True:
            # Time expired or any key is pressed. should continue
            # We have added True to allow any key to work.
            # This is done in order to maintain the structure of the code
            # The "else" corresponding to "another key present" is not possible to reach, but it is kept
            # to maintain the structure of this code
            if scanconfig.cte_force_wait_bit_x:
                mx_finished = False
                while not mx_finished:
                    mx_finished = stepFinishedXPoll()

            if scanconfig.cte_force_wait_bit_y:
                my_finished = False
                while not my_finished:
                    my_finished = stepFinishedYPoll()

            if scanconfig.cte_force_wait_bit_comp:
                mcomp_finished = False
                while not mcomp_finished:
                    mcomp_finished = stepFinishedCompPoll()

            ret = 1

        else:
            # Another key presssed
            ret = 0

    return ret


current_pos_x = 0
current_pos_y = 0
current_pos_comp = 0

mx_status = 0
my_status = 0
mcomp_status = 0


# # Gets the status of the X motor
def getMotorStatusX():
    global mx_status

    # Obtain final positions
    if scanconfig.cte_use_motor_x:
        sendXportBegin(scanconfig.cte_motor_x_xport)
        cmd_str = prefixX + "OST"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("OSTCmd:" + cmd_str)
        r = getMotorResponse()
        if scanconfig.cte_verbose:
            print("OSTResp x:" + r)
        mx_status = int(r)
        sendXportEnd()
    else:
        mx_status = 0


# # Gets the status of the Y motor
def getMotorStatusY():
    global my_status

    # Obtain final positions
    if scanconfig.cte_use_motor_y:
        sendXportBegin(scanconfig.cte_motor_y_xport)
        cmd_str = prefixY + "OST"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("OSTCmd:" + cmd_str)
        r = getMotorResponse()
        if scanconfig.cte_verbose:
            print("OSTResp y:" + r)
        my_status = int(r)
        sendXportEnd()
    else:
        my_status = 0


# # Gets the status of the Comp motor
def getMotorStatusComp():
    global mcomp_status

    # Obtain final positions
    if scanconfig.cte_use_motor_comp:
        sendXportBegin(scanconfig.cte_motor_comp_xport)
        cmd_str = prefixComp + "OST"
        sendMotorCommand(cmd_str)
        if scanconfig.cte_verbose:
            print("OSTCmd:" + cmd_str)
        r = getMotorResponse()
        if scanconfig.cte_verbose:
            print("OSTResp Comp:" + r)
        mcomp_status = int(r)
        sendXportEnd()
    else:
        mcomp_status = 0


mx_finished = False
my_finished = False
mcomp_finished = False


# Checks if the positions has been attained for motor X
def stepFinishedXPoll():
    global mx_finished

    if not mx_finished:
        getMotorStatusX()
        mx_finished = testBit(mx_status, 16)
    if mx_finished:
        print "Finished X!\n"
    else:
        print "Not Finished X!\n"

    return mx_finished


# Checks if the positions has been attained for motor X
def stepFinishedYPoll():
    global my_finished

    if not my_finished:
        getMotorStatusY()
        my_finished = testBit(my_status, 16)
    if my_finished:
        print "Finished Y!\n"
    else:
        print "Not Finished Y!\n"

    return my_finished


# Checks if the positions has been attained for motor Comp
def stepFinishedCompPoll():
    global mcomp_finished

    if not mcomp_finished:
        getMotorStatusComp()
        mcomp_finished = testBit(mcomp_status, 16)
    if mcomp_finished:
        print "Finished Comp!\n"
    else:
        print "Not Finished Comp!\n"

    return mcomp_finished


# Retrieves the position for each motor
def motorPositions():
    global current_pos_x
    global current_pos_y
    global current_pos_comp

    if not scanconfig.cte_command_gcs:    
        # Obtain final positions
        if scanconfig.cte_use_motor_x:
            sendXportBegin(scanconfig.cte_motor_x_xport)
            cmd_str = prefixX + "POS"
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("PosCmd:" + cmd_str)
            r = getMotorResponse()
            if scanconfig.cte_verbose:
                print("PosResp x:" + r)
            mx_fdback = int(r)
            current_pos_x = mx_fdback
            sendXportEnd()
        else:
            mx_fdback = -1

        if scanconfig.cte_use_motor_y:
            sendXportBegin(scanconfig.cte_motor_y_xport)
            cmd_str = prefixY + "POS"
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("PosCmd:" + cmd_str)
            r = getMotorResponse()
            if scanconfig.cte_verbose:
                print("PosResp y:" + r)
            my_fdback = int(r)
            current_pos_y = my_fdback
            sendXportEnd()
        else:
            my_fdback = -1

        if scanconfig.cte_use_motor_comp:
            sendXportBegin(scanconfig.cte_motor_comp_xport)
            cmd_str = prefixComp + "POS"
            sendMotorCommand(cmd_str)
            if scanconfig.cte_verbose:
                print("PosCmd:" + cmd_str)
            r = getMotorResponse()
            if scanconfig.cte_verbose:
                print("PosResp comp:" + r)
            mcomp_fdback = int(r)
            current_pos_comp = mcomp_fdback
            sendXportEnd()
        else:
            mcomp_fdback = -1
            
        
    else:
        mx_fdback = my_fdback = mcomp_fdback = 0
                
        
    return mx_fdback, my_fdback, mcomp_fdback


# Closes the communication with the motors
def motorClose():
    if not scanconfig.cte_use_socket:
        ser.close()             # close port
    else:    
        sckt.close              # Close the socket when done    


ID_GETCTRLGCSTCPRESPONSE_INITIAL = 49
ID_GETCTRLGCSTCPRESPONSE_FINAL = 50
ID_GETCTRLGCSTCPRESPONSE_READING = 51
ID_GETCTRLGCSTCPRESPONSE_FINISHING = 52

gcs_tcp_response_state = ID_GETCTRLGCSTCPRESPONSE_INITIAL

def getGcsTcpCtrlResponse(  ):
    # set initial state
    gcs_tcp_response_state = ID_GETCTRLGCSTCPRESPONSE_INITIAL

    while( True ):
        # State ID: ID_GETCTRLGCSTCPRESPONSE_INITIAL
        if( gcs_tcp_response_state==ID_GETCTRLGCSTCPRESPONSE_INITIAL ):
            # Transition ID: ID_GETCTRLGCSTCPRESPONSE_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::resetRxTask' begin]
            FoV.dre.command_rx_buf=""
            # ['<global>::resetRxTask' end]
            FoV.serialCharRead()
            gcs_tcp_response_state = ID_GETCTRLGCSTCPRESPONSE_READING

        # State ID: ID_GETCTRLGCSTCPRESPONSE_READING
        elif( gcs_tcp_response_state==ID_GETCTRLGCSTCPRESPONSE_READING ):
            if( FoV.dre.char_read==chr(10) or FoV.dre.char_read==chr(13) ):
                # Transition ID: ID_GETCTRLGCSTCPRESPONSE_TRANSITION_CONNECTION
                # Actions:
                FoV.serialCharRead()
                gcs_tcp_response_state = ID_GETCTRLGCSTCPRESPONSE_FINISHING

            elif( (FoV.dre.char_read != chr(10)) and (FoV.dre.char_read != chr(13)) ):
                # Transition ID: ID_GETCTRLGCSTCPRESPONSE_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::appendCharToRxBuf' begin]
                FoV.dre.command_rx_buf += FoV.dre.char_read
                # ['<global>::appendCharToRxBuf' end]
                FoV.serialCharRead()

        # State ID: ID_GETCTRLGCSTCPRESPONSE_FINISHING
        elif( gcs_tcp_response_state==ID_GETCTRLGCSTCPRESPONSE_FINISHING ):
            if( FoV.dre.char_read==chr(10) or dre.char_read==chr(13) ):
                # Transition ID: ID_GETCTRLGCSTCPRESPONSE_TRANSITION_CONNECTION
                gcs_tcp_response_state = ID_GETCTRLGCSTCPRESPONSE_FINAL

            elif( (FoV.dre.char_read != chr(10)) and (FoV.dre.char_read != chr(13)) ):
                # Transition ID: ID_GETCTRLGCSTCPRESPONSE_TRANSITION_CONNECTION
                # Actions:
                FoV.serialCharRead()

        # State ID: ID_GETCTRLGCSTCPRESPONSE_FINAL
        elif( gcs_tcp_response_state==ID_GETCTRLGCSTCPRESPONSE_FINAL ):
            return ID_GETCTRLGCSTCPRESPONSE_FINAL



# Gets a response from the GCS over TCP
def getGcsTcpResponse(  ):
    getGcsTcpCtrlResponse()
    print ("GCSTCP>> " + FoV.dre.command_rx_buf)        
    return FoV.dre.command_rx_buf


cte_vh = [cte_vhx, cte_vhy, cte_vhcomp]
cte_vi = [cte_vix, cte_viy, cte_vicomp]
cte_v = [cte_vx, cte_vy, cte_vcomp]

# ########## MAIN INITIALIZATIONS ###############

# Indicates to the DRE (fsm data base) which kind of connection must be used
FoV.dre.cte_use_socket = scanconfig.cte_use_socket

# Opens the communication channel
if not scanconfig.cte_use_socket:
    import serial

    cte_serial_port = scanconfig.cte_serial_port
    if scanconfig.cte_verbose:
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
    if scanconfig.cte_command_gcs:
        sckt.connect((scanconfig.cte_command_gcs_ip, scanconfig.cte_command_gcs_port))
    else:
        sckt.connect((scanconfig.cte_socket_ip, scanconfig.cte_socket_port))
        
    FoV.dre.ser = sckt
    if not scanconfig.cte_command_gcs:
        resetXport()
        
    resetPendingResponses()

if scanconfig.cte_use_socket:
    prefixX = ""
    prefixY = ""
    prefixComp = ""
else:
    prefixX = str(scanconfig.cte_motor_x)
    prefixY = str(scanconfig.cte_motor_y)
    prefixComp = str(scanconfig.cte_motor_comp)



