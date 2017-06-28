# ['Common imports' begin (DON'T REMOVE THIS LINE!)]
from FoV_CI import *
# ['Common imports' end (DON'T REMOVE THIS LINE!)]

# ['Common definitions for 'Hierarchical State Chart generator'' begin (DON'T REMOVE THIS LINE!)]
# Code items' definitions
def serialCharRead(  ):
    # ['<global>::serialCharRead' begin]
    if not(dre.cte_use_socket):
        dre.char_read=dre.ser.read(1) 
    else:
        readlen=0
        while(readlen<1):
            data = dre.ser.recv(1)
            readlen=len(data)

        dre.char_read=str(data)[0]
    # ['<global>::serialCharRead' end]


def decodeM1Cmd(  ):
    # ['<global>::decodeM1Cmd' begin]
    # Prepare common decoder with M1 values
    dre.mX=dre.m1
    
    # Call common decoder
    DecodeMotorCmd()
    # ['<global>::decodeM1Cmd' end]

def decodeM2Cmd(  ):
    # ['<global>::decodeM2Cmd' begin]
    # Prepare common decoder with M2 values
    dre.mX=dre.m2
    
    # Call common decoder
    DecodeMotorCmd()
    # ['<global>::decodeM2Cmd' end]

def decodeM3Cmd(  ):
    # ['<global>::decodeM3Cmd' begin]
    # Prepare common decoder with M3 values
    dre.mX=dre.m3
    
    # Call common decoder
    DecodeMotorCmd()
    # ['<global>::decodeM3Cmd' end]

def resetDecoder(  ):
    # ['<global>::resetDecoder' begin]
    # Flush commands from M1
    dre.mX.la=False
    dre.mX.np=False
    dre.mX.hosp=False
    dre.mX.goix=False
    dre.mX.apl=False
    dre.mX.gohoseq=False
    dre.mX.reqpos=False
    dre.mX.m=False
    dre.mX.spd=False
    # Flush arguments from M1
    dre.mX.spdarg=0
    dre.mX.posarg=0
    # Flush error
    dre.mX.error=False
    # ['<global>::resetDecoder' end]

def programGoHoSeq(  ):
    # ['<global>::programGoHoSeq' begin]
    # Program GoHoSeq similar to program LA with setpoint = 0

    dre.mX.setpoint = 0

    dre.mX.m = True

    # ['<global>::programGoHoSeq' end]

def checkCharAtPos( idx, cToCheck, isEqual ):
    # ['<global>::checkCharAtPos' begin]
    if (isEqual):
        return (dre.mX.cmd[idx]==cToCheck)
    else:
        return (dre.mX.cmd[idx]!=cToCheck)
    # ['<global>::checkCharAtPos' end]

# ['Common definitions for 'Hierarchical State Chart generator'' end (DON'T REMOVE THIS LINE!)]

# ['Moving' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_MOVING_INITIAL = 0
ID_MOVING_FINAL = 1
ID_MOVING_INTEGRATOR = 2

def Moving(  ):
    # set initial state
    state = ID_MOVING_INITIAL

    while( True ):
        # State ID: ID_MOVING_INITIAL
        if( state==ID_MOVING_INITIAL ):
            # Transition ID: ID_MOVING_TRANSITION_CONNECTION
            state = ID_MOVING_INTEGRATOR

        # State ID: ID_MOVING_INTEGRATOR
        elif( state==ID_MOVING_INTEGRATOR ):
            if( dre.m1setpoint > dre.m1pos ):
                # Transition ID: ID_MOVING_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::incrDelta' begin]
                tmp=dre.m1pos
                dre.m1pos+=1
                print obtainVarName(dre.m1pos)+":"+str(tmp)+"+"+str(1)+"="+str(dre.m1pos)
                # ['<global>::incrDelta' end]

            elif( dre.m1pos > dre.m1setpoint ):
                # Transition ID: ID_MOVING_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::incrDelta' begin]
                tmp=dre.m1pos
                dre.m1pos+=-1
                print obtainVarName(dre.m1pos)+":"+str(tmp)+"+"+str(-1)+"="+str(dre.m1pos)
                # ['<global>::incrDelta' end]

            else:
                # Transition ID: ID_MOVING_TRANSITION_CONNECTION
                state = ID_MOVING_FINAL

        # State ID: ID_MOVING_FINAL
        elif( state==ID_MOVING_FINAL ):
            return ID_MOVING_FINAL

# ['Moving' end (DON'T REMOVE THIS LINE!)]

# ['M1' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_M1_INITIAL = 18
ID_M1_FINAL = 19
ID_M1_WAITING = 20

def M1(  ):
    # set initial state
    state = ID_M1_INITIAL

    while( True ):
        # State ID: ID_M1_INITIAL
        if( state==ID_M1_INITIAL ):
            # Transition ID: ID_M1_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::setM1Response' begin]
            dre.m1.resp="OK"
            # ['<global>::setM1Response' end]
            state = ID_M1_WAITING

        # State ID: ID_M1_WAITING
        elif( state==ID_M1_WAITING ):
            if( ((dre.m1.np)==(True)) ):
                # Transition ID: ID_M1_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setMutexFlag' begin]
                dre.m1.mutex.acquire()

                try:

                    dre.m1.npflag=True

                finally:

                    dre.m1.mutex.release()
                # ['<global>::setMutexFlag' end]
                state = ID_M1_FINAL

            elif( ((dre.m1.m)==(True)) ):
                # Transition ID: ID_M1_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setMutexFlag' begin]
                dre.m1.mutex.acquire()

                try:

                    dre.m1.laflag=True

                finally:

                    dre.m1.mutex.release()
                # ['<global>::setMutexFlag' end]
                state = ID_M1_FINAL

            elif( ((dre.m1.reqpos)==(True)) ):
                # Transition ID: ID_M1_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setM1Response' begin]
                dre.m1.resp=str(dre.m1.pos)
                # ['<global>::setM1Response' end]
                state = ID_M1_FINAL

            elif( ((dre.m1.la)==(True)) ):
                # Transition ID: ID_M1_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setVar' begin]
                dre.m1.setpoint=(dre.m1.posarg)
                # ['<global>::setVar' end]
                state = ID_M1_FINAL

            else:
                # Transition ID: ID_M1_TRANSITION_CONNECTION
                state = ID_M1_FINAL

        # State ID: ID_M1_FINAL
        elif( state==ID_M1_FINAL ):
            return ID_M1_FINAL

# ['M1' end (DON'T REMOVE THIS LINE!)]

# ['DecodeMotorCmd' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_DECODEMOTORCMD_INITIAL = 21
ID_DECODEMOTORCMD_FINAL = 22
ID_DECODEMOTORCMD_ERROR = 23
ID_DECODEMOTORCMD_NRECEIVED = 24
ID_DECODEMOTORCMD_SRECEIVED = 25
ID_DECODEMOTORCMD_PORECEIVED = 26
ID_DECODEMOTORCMD_PRECEIVED = 27
ID_DECODEMOTORCMD_LRECEIVED = 28
ID_DECODEMOTORCMD_GRECEIVED = 29

def DecodeMotorCmd(  ):
    # set initial state
    state = ID_DECODEMOTORCMD_INITIAL

    while( True ):
        # State ID: ID_DECODEMOTORCMD_INITIAL
        if( state==ID_DECODEMOTORCMD_INITIAL ):
            if( checkCharAtPos(0, 'N', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                resetDecoder()
                state = ID_DECODEMOTORCMD_NRECEIVED

            elif( checkCharAtPos(0, 'L', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                resetDecoder()
                state = ID_DECODEMOTORCMD_LRECEIVED

            elif( checkCharAtPos(0, 'P', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                resetDecoder()
                state = ID_DECODEMOTORCMD_PRECEIVED

            elif( checkCharAtPos(0, 'M', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                resetDecoder()
                # ['<global>::programM' begin]
                dre.mX.m = True
                # ['<global>::programM' end]
                state = ID_DECODEMOTORCMD_FINAL

            elif( checkCharAtPos(0, 'S', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                resetDecoder()
                state = ID_DECODEMOTORCMD_SRECEIVED

            elif( checkCharAtPos(0, 'G', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                resetDecoder()
                state = ID_DECODEMOTORCMD_GRECEIVED

            else:
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                resetDecoder()
                state = ID_DECODEMOTORCMD_ERROR

        # State ID: ID_DECODEMOTORCMD_NRECEIVED
        elif( state==ID_DECODEMOTORCMD_NRECEIVED ):
            if( checkCharAtPos(1, 'P', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::programNP' begin]
                dre.mX.np=True
                # ['<global>::programNP' end]
                state = ID_DECODEMOTORCMD_FINAL

            else:
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                state = ID_DECODEMOTORCMD_ERROR

        # State ID: ID_DECODEMOTORCMD_ERROR
        elif( state==ID_DECODEMOTORCMD_ERROR ):
            # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::decodeError' begin]
            dre.mX.error=True
            # ['<global>::decodeError' end]
            state = ID_DECODEMOTORCMD_FINAL

        # State ID: ID_DECODEMOTORCMD_FINAL
        elif( state==ID_DECODEMOTORCMD_FINAL ):
            return ID_DECODEMOTORCMD_FINAL

        # State ID: ID_DECODEMOTORCMD_LRECEIVED
        elif( state==ID_DECODEMOTORCMD_LRECEIVED ):
            if( checkCharAtPos(1, 'A', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::programLA' begin]
                dre.mX.la=True
                dre.mX.posarg=int(dre.mX.cmd[2:])
                # ['<global>::programLA' end]
                state = ID_DECODEMOTORCMD_FINAL

            elif( checkCharAtPos(1, 'R', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::programLR' begin]
                # LR is similar to LA 

                dre.mX.la=True
                dre.mX.posarg=dre.mX.pos+int(dre.mX.cmd[2:])
                # ['<global>::programLR' end]
                state = ID_DECODEMOTORCMD_FINAL

            else:
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                state = ID_DECODEMOTORCMD_ERROR

        # State ID: ID_DECODEMOTORCMD_SRECEIVED
        elif( state==ID_DECODEMOTORCMD_SRECEIVED ):
            if( checkCharAtPos(1, 'P', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::programSP' begin]
                dre.mX.spd = True
                dre.mX.spdarg = int(dre.mX.cmd[2:])
                # ['<global>::programSP' end]
                state = ID_DECODEMOTORCMD_FINAL

            else:
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                state = ID_DECODEMOTORCMD_ERROR

        # State ID: ID_DECODEMOTORCMD_PRECEIVED
        elif( state==ID_DECODEMOTORCMD_PRECEIVED ):
            if( checkCharAtPos(1, 'O', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                state = ID_DECODEMOTORCMD_PORECEIVED

            else:
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                state = ID_DECODEMOTORCMD_ERROR

        # State ID: ID_DECODEMOTORCMD_PORECEIVED
        elif( state==ID_DECODEMOTORCMD_PORECEIVED ):
            if( checkCharAtPos(2, 'S', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::programPOS' begin]
                dre.mX.reqpos=True
                # ['<global>::programPOS' end]
                state = ID_DECODEMOTORCMD_FINAL

            else:
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                state = ID_DECODEMOTORCMD_ERROR

        # State ID: ID_DECODEMOTORCMD_GRECEIVED
        elif( state==ID_DECODEMOTORCMD_GRECEIVED ):
            if( checkCharAtPos(2, 'H', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                programGoHoSeq()
                state = ID_DECODEMOTORCMD_FINAL

            elif( checkCharAtPos(2, 'I', True) ):
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::programGoIx' begin]
                # Program GoIx similar to program LA with setpoint = 0

                dre.mX.setpoint = 0

                dre.mX.m = True

                # ['<global>::programGoIx' end]
                state = ID_DECODEMOTORCMD_FINAL

            else:
                # Transition ID: ID_DECODEMOTORCMD_TRANSITION_CONNECTION
                state = ID_DECODEMOTORCMD_ERROR

# ['DecodeMotorCmd' end (DON'T REMOVE THIS LINE!)]

# ['ProgramMotors' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_PROGRAMMOTORS_INITIAL = 30
ID_PROGRAMMOTORS_FINAL = 31
ID_PROGRAMMOTORS_M2BYPASS = 32
ID_PROGRAMMOTORS_M1BYPASS = 33
ID_PROGRAMMOTORS_M2DECODED = 34
ID_PROGRAMMOTORS_M3DECODED = 35
ID_PROGRAMMOTORS_M1DECODED = 36

def ProgramMotors(  ):
    # set initial state
    state = ID_PROGRAMMOTORS_INITIAL

    while( True ):
        # State ID: ID_PROGRAMMOTORS_INITIAL
        if( state==ID_PROGRAMMOTORS_INITIAL ):
            if( dre.m1.req==False ):
                # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
                state = ID_PROGRAMMOTORS_M1BYPASS

            elif( dre.m1.req==True ):
                # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
                # Actions:
                decodeM1Cmd()
                state = ID_PROGRAMMOTORS_M1DECODED

        # State ID: ID_PROGRAMMOTORS_M1DECODED
        elif( state==ID_PROGRAMMOTORS_M1DECODED ):
            if( dre.m2.req==False ):
                # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
                state = ID_PROGRAMMOTORS_M2BYPASS

            elif( dre.m2.req==True ):
                # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
                # Actions:
                decodeM2Cmd()
                state = ID_PROGRAMMOTORS_M2DECODED

        # State ID: ID_PROGRAMMOTORS_M2DECODED
        elif( state==ID_PROGRAMMOTORS_M2DECODED ):
            if( dre.m3.req==True ):
                # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
                # Actions:
                decodeM3Cmd()
                state = ID_PROGRAMMOTORS_M3DECODED

            elif( dre.m3.req==False ):
                # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
                state = ID_PROGRAMMOTORS_FINAL

        # State ID: ID_PROGRAMMOTORS_FINAL
        elif( state==ID_PROGRAMMOTORS_FINAL ):
            return ID_PROGRAMMOTORS_FINAL

        # State ID: ID_PROGRAMMOTORS_M3DECODED
        elif( state==ID_PROGRAMMOTORS_M3DECODED ):
            # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
            state = ID_PROGRAMMOTORS_FINAL

        # State ID: ID_PROGRAMMOTORS_M2BYPASS
        elif( state==ID_PROGRAMMOTORS_M2BYPASS ):
            if( dre.m3.req==True ):
                # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
                # Actions:
                decodeM3Cmd()
                state = ID_PROGRAMMOTORS_M3DECODED

            elif( dre.m3.req==False ):
                # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
                state = ID_PROGRAMMOTORS_FINAL

        # State ID: ID_PROGRAMMOTORS_M1BYPASS
        elif( state==ID_PROGRAMMOTORS_M1BYPASS ):
            if( dre.m2.req==True ):
                # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
                # Actions:
                decodeM2Cmd()
                state = ID_PROGRAMMOTORS_M2DECODED

            elif( dre.m2.req==False ):
                # Transition ID: ID_PROGRAMMOTORS_TRANSITION_CONNECTION
                state = ID_PROGRAMMOTORS_M2BYPASS

# ['ProgramMotors' end (DON'T REMOVE THIS LINE!)]

# ['CmdDispatcher' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_CMDDISPATCHER_INITIAL = 37
ID_CMDDISPATCHER_FINAL = 38
ID_CMDDISPATCHER_DECODEENGINE = 39
ID_CMDDISPATCHER_PROGRAMMOTORS = 40

def CmdDispatcher(  ):
    # set initial state
    state = ID_CMDDISPATCHER_INITIAL

    while( True ):
        # State ID: ID_CMDDISPATCHER_INITIAL
        if( state==ID_CMDDISPATCHER_INITIAL ):
            # Transition ID: ID_CMDDISPATCHER_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::resetDispatcher' begin]
            dre.dispatcher_idx=0
            dre.m1.cmd=""
            dre.m2.cmd=""
            dre.m2.cmd=""
            dre.m1.req=False
            dre.m2.req=False
            dre.m3.req=False
            # ['<global>::resetDispatcher' end]
            state = ID_CMDDISPATCHER_DECODEENGINE

        # State ID: ID_CMDDISPATCHER_DECODEENGINE
        elif( state==ID_CMDDISPATCHER_DECODEENGINE ):
            if( (("#" in dre.command_rx_buf) or ("@" in dre.command_rx_buf)) ):
                # Transition ID: ID_CMDDISPATCHER_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setNewTarget' begin]
                if ("#" in dre.command_rx_buf):

                    port=dre.command_rx_buf.split("#")[1]

                    if (port==str(dre.m1port)):

                        dre.activeMotorPrefix=str(1)

                    if (port==str(dre.m2port)):

                        dre.activeMotorPrefix=str(2)

                    if (port==str(dre.m3port)):

                        dre.activeMotorPrefix=str(3)

                else:

                    #("@" in dre.command_rx_buf)

                    dre.activeMotorPrefix=""

                # ['<global>::setNewTarget' end]
                # ['<global>::sendAnticipatedResponse' begin]
                if not(dre.cte_use_socket):
                    dre.ser.write(""+chr(13)+chr(10))
                else:
                    dre.ser.sendall(""+chr(13)+chr(10))
                # ['<global>::sendAnticipatedResponse' end]
                state = ID_CMDDISPATCHER_PROGRAMMOTORS

            elif( str(1)[0]==dre.command_rx_buf[0] ):
                # Transition ID: ID_CMDDISPATCHER_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setM1Cmd' begin]
                dre.m1.req=True
                dre.m1.cmd=dre.command_rx_buf[1:]
                # ['<global>::setM1Cmd' end]
                state = ID_CMDDISPATCHER_PROGRAMMOTORS

            elif( str(2)[0]==dre.command_rx_buf[0] ):
                # Transition ID: ID_CMDDISPATCHER_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setM2Cmd' begin]
                dre.m2.req=True
                dre.m2.cmd=dre.command_rx_buf[1:]
                # ['<global>::setM2Cmd' end]
                state = ID_CMDDISPATCHER_PROGRAMMOTORS

            elif( str(3)[0]==dre.command_rx_buf[0] ):
                # Transition ID: ID_CMDDISPATCHER_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setM3Cmd' begin]
                dre.m3.req=True
                dre.m3.cmd=dre.command_rx_buf[1:]
                # ['<global>::setM3Cmd' end]
                state = ID_CMDDISPATCHER_PROGRAMMOTORS

            elif( ((""+chr(27)) in dre.command_rx_buf) ):
                # Transition ID: ID_CMDDISPATCHER_TRANSITION_CONNECTION
                state = ID_CMDDISPATCHER_FINAL

            else:
                # Transition ID: ID_CMDDISPATCHER_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setAllMotorsCmd' begin]
                dre.m1.req=True
                dre.m2.req=True
                dre.m3.req=True
                dre.m1.cmd=dre.command_rx_buf
                dre.m2.cmd=dre.command_rx_buf
                dre.m3.cmd=dre.command_rx_buf
                # ['<global>::setAllMotorsCmd' end]
                state = ID_CMDDISPATCHER_PROGRAMMOTORS

        # State ID: ID_CMDDISPATCHER_PROGRAMMOTORS
        elif( state==ID_CMDDISPATCHER_PROGRAMMOTORS ):
            # call substate function
            programmotors_retval = ProgramMotors(  )
            # Transition ID: ID_CMDDISPATCHER_TRANSITION_CONNECTION
            state = ID_CMDDISPATCHER_FINAL

        # State ID: ID_CMDDISPATCHER_FINAL
        elif( state==ID_CMDDISPATCHER_FINAL ):
            return ID_CMDDISPATCHER_FINAL

# ['CmdDispatcher' end (DON'T REMOVE THIS LINE!)]

# ['sendCtrlResponse' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_SENDCTRLRESPONSE_INITIAL = 41
ID_SENDCTRLRESPONSE_FINAL = 42

def sendCtrlResponse(  ):
    # set initial state
    state = ID_SENDCTRLRESPONSE_INITIAL

    while( True ):
        # State ID: ID_SENDCTRLRESPONSE_INITIAL
        if( state==ID_SENDCTRLRESPONSE_INITIAL ):
            # Transition ID: ID_SENDCTRLRESPONSE_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::serialResposeWrite' begin]
            if not(dre.cte_use_socket):

                dre.ser.write(dre.command_tx_buf+chr(13)+chr(10))

            else:

                dre.ser.sendall(dre.command_tx_buf+chr(13)+chr(10))
            # ['<global>::serialResposeWrite' end]
            state = ID_SENDCTRLRESPONSE_FINAL

        # State ID: ID_SENDCTRLRESPONSE_FINAL
        elif( state==ID_SENDCTRLRESPONSE_FINAL ):
            return ID_SENDCTRLRESPONSE_FINAL

# ['sendCtrlResponse' end (DON'T REMOVE THIS LINE!)]

# ['getCtrlCommand' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_GETCTRLCOMMAND_INITIAL = 43
ID_GETCTRLCOMMAND_FINAL = 44
ID_GETCTRLCOMMAND_READING = 45
ID_GETCTRLCOMMAND_PREVBUF = 46

def getCtrlCommand(  ):
    # set initial state
    state = ID_GETCTRLCOMMAND_INITIAL

    while( True ):
        # State ID: ID_GETCTRLCOMMAND_INITIAL
        if( state==ID_GETCTRLCOMMAND_INITIAL ):
            if( len(dre.rx_buffer)<1 ):
                # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::resetRxTask' begin]
                dre.command_rx_buf=""
                # ['<global>::resetRxTask' end]
                serialCharRead()
                state = ID_GETCTRLCOMMAND_READING

            else:
                # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::resetRxTask' begin]
                dre.command_rx_buf=""
                # ['<global>::resetRxTask' end]
                # ['<global>::bufferCharRead' begin]
                dre.char_read=dre.rx_buffer[0]
                dre.rx_buffer=dre.rx_buffer[1:]
                # ['<global>::bufferCharRead' end]
                state = ID_GETCTRLCOMMAND_PREVBUF

        # State ID: ID_GETCTRLCOMMAND_READING
        elif( state==ID_GETCTRLCOMMAND_READING ):
            if( (dre.char_read != chr(10)) and (dre.char_read != chr(13)) ):
                # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::appendCharToRxBuf' begin]
                dre.command_rx_buf+=dre.char_read
                # ['<global>::appendCharToRxBuf' end]
                serialCharRead()

            elif( dre.char_read==chr(10) or dre.char_read==chr(13) ):
                # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::prependActiveMotor' begin]
                dre.command_rx_buf=dre.activeMotorPrefix+dre.command_rx_buf
                # ['<global>::prependActiveMotor' end]
                state = ID_GETCTRLCOMMAND_FINAL

        # State ID: ID_GETCTRLCOMMAND_FINAL
        elif( state==ID_GETCTRLCOMMAND_FINAL ):
            return ID_GETCTRLCOMMAND_FINAL

        # State ID: ID_GETCTRLCOMMAND_PREVBUF
        elif( state==ID_GETCTRLCOMMAND_PREVBUF ):
            if( dre.char_read==chr(10) or dre.char_read==chr(13) ):
                # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::prependActiveMotor' begin]
                dre.command_rx_buf=dre.activeMotorPrefix+dre.command_rx_buf
                # ['<global>::prependActiveMotor' end]
                state = ID_GETCTRLCOMMAND_FINAL

            elif( len(dre.rx_buffer)<1 ):
                # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::appendCharToRxBuf' begin]
                dre.command_rx_buf+=dre.char_read
                # ['<global>::appendCharToRxBuf' end]
                serialCharRead()
                state = ID_GETCTRLCOMMAND_READING

            else:
                # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::bufferCharRead' begin]
                dre.char_read=dre.rx_buffer[0]
                dre.rx_buffer=dre.rx_buffer[1:]
                # ['<global>::bufferCharRead' end]
                # ['<global>::appendCharToRxBuf' begin]
                dre.command_rx_buf+=dre.char_read
                # ['<global>::appendCharToRxBuf' end]

# ['getCtrlCommand' end (DON'T REMOVE THIS LINE!)]

# ['sendCtrlCommand' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_SENDCTRLCOMMAND_INITIAL = 47
ID_SENDCTRLCOMMAND_FINAL = 48

def sendCtrlCommand(  ):
    # set initial state
    state = ID_SENDCTRLCOMMAND_INITIAL

    while( True ):
        # State ID: ID_SENDCTRLCOMMAND_INITIAL
        if( state==ID_SENDCTRLCOMMAND_INITIAL ):
            # Transition ID: ID_SENDCTRLCOMMAND_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::serialCommandWrite' begin]
            if not(dre.cte_use_socket):

                dre.ser.write(dre.command_tx_buf+chr(13))

            else:

                dre.ser.sendall(dre.command_tx_buf+chr(13))
            # ['<global>::serialCommandWrite' end]
            state = ID_SENDCTRLCOMMAND_FINAL

        # State ID: ID_SENDCTRLCOMMAND_FINAL
        elif( state==ID_SENDCTRLCOMMAND_FINAL ):
            return ID_SENDCTRLCOMMAND_FINAL

# ['sendCtrlCommand' end (DON'T REMOVE THIS LINE!)]

# ['getCtrlResponse' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_GETCTRLRESPONSE_INITIAL = 49
ID_GETCTRLRESPONSE_FINAL = 50
ID_GETCTRLRESPONSE_READING = 51
ID_GETCTRLRESPONSE_FINISHING = 52

def getCtrlResponse(  ):
    # set initial state
    state = ID_GETCTRLRESPONSE_INITIAL

    while( True ):
        # State ID: ID_GETCTRLRESPONSE_INITIAL
        if( state==ID_GETCTRLRESPONSE_INITIAL ):
            # Transition ID: ID_GETCTRLRESPONSE_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::resetRxTask' begin]
            dre.command_rx_buf=""
            # ['<global>::resetRxTask' end]
            serialCharRead()
            state = ID_GETCTRLRESPONSE_READING

        # State ID: ID_GETCTRLRESPONSE_READING
        elif( state==ID_GETCTRLRESPONSE_READING ):
            if( dre.char_read==chr(10) or dre.char_read==chr(13) ):
                # Transition ID: ID_GETCTRLRESPONSE_TRANSITION_CONNECTION
                # Actions:
                serialCharRead()
                state = ID_GETCTRLRESPONSE_FINISHING

            elif( (dre.char_read != chr(10)) and (dre.char_read != chr(13)) ):
                # Transition ID: ID_GETCTRLRESPONSE_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::appendCharToRxBuf' begin]
                dre.command_rx_buf+=dre.char_read
                # ['<global>::appendCharToRxBuf' end]
                serialCharRead()

        # State ID: ID_GETCTRLRESPONSE_FINISHING
        elif( state==ID_GETCTRLRESPONSE_FINISHING ):
            if( dre.char_read==chr(10) or dre.char_read==chr(13) ):
                # Transition ID: ID_GETCTRLRESPONSE_TRANSITION_CONNECTION
                state = ID_GETCTRLRESPONSE_FINAL

            elif( (dre.char_read != chr(10)) and (dre.char_read != chr(13)) ):
                # Transition ID: ID_GETCTRLRESPONSE_TRANSITION_CONNECTION
                # Actions:
                serialCharRead()

        # State ID: ID_GETCTRLRESPONSE_FINAL
        elif( state==ID_GETCTRLRESPONSE_FINAL ):
            return ID_GETCTRLRESPONSE_FINAL

# ['getCtrlResponse' end (DON'T REMOVE THIS LINE!)]

# ['M1Movement' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_M1MOVEMENT_INITIAL = 4
ID_M1MOVEMENT_FINAL = 5
ID_M1MOVEMENT_STEPDONE = 6
ID_M1MOVEMENT_ENABLE = 7

def M1Movement(  ):
    # set initial state
    state = ID_M1MOVEMENT_INITIAL

    while( True ):
        # State ID: ID_M1MOVEMENT_INITIAL
        if( state==ID_M1MOVEMENT_INITIAL ):
            if( ((dre.m1.laflag)==(True)) ):
                # Transition ID: ID_M1MOVEMENT_TRANSITION_CONNECTION
                state = ID_M1MOVEMENT_ENABLE

            else:
                # Transition ID: ID_M1MOVEMENT_TRANSITION_CONNECTION
                state = ID_M1MOVEMENT_FINAL

        # State ID: ID_M1MOVEMENT_ENABLE
        elif( state==ID_M1MOVEMENT_ENABLE ):
            if( dre.m1.setpoint > dre.m1.pos ):
                # Transition ID: ID_M1MOVEMENT_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::incrDelta' begin]
                tmp=dre.m1.pos
                dre.m1.pos+=+1
                #print obtainVarName(dre.m1.pos)+":"+str(tmp)+"+"+str(+1)+"="+str(dre.m1.pos)
                # ['<global>::incrDelta' end]
                state = ID_M1MOVEMENT_STEPDONE

            elif( dre.m1.pos > dre.m1.setpoint ):
                # Transition ID: ID_M1MOVEMENT_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::incrDelta' begin]
                tmp=dre.m1.pos
                dre.m1.pos+=-1
                #print obtainVarName(dre.m1.pos)+":"+str(tmp)+"+"+str(-1)+"="+str(dre.m1.pos)
                # ['<global>::incrDelta' end]
                state = ID_M1MOVEMENT_STEPDONE

            else:
                # Transition ID: ID_M1MOVEMENT_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::notifyEndMv' begin]
                if (dre.m1.npflag):
                    sendUntimelyResponse("p")
                # ['<global>::notifyEndMv' end]
                # ['<global>::setFlag' begin]
                dre.m1.npflag=False
                # ['<global>::setFlag' end]
                # ['<global>::setFlag' begin]
                dre.m1.laflag=False
                # ['<global>::setFlag' end]
                state = ID_M1MOVEMENT_FINAL

        # State ID: ID_M1MOVEMENT_STEPDONE
        elif( state==ID_M1MOVEMENT_STEPDONE ):
            # Transition ID: ID_M1MOVEMENT_TRANSITION_CONNECTION
            state = ID_M1MOVEMENT_FINAL

        # State ID: ID_M1MOVEMENT_FINAL
        elif( state==ID_M1MOVEMENT_FINAL ):
            return ID_M1MOVEMENT_FINAL

# ['M1Movement' end (DON'T REMOVE THIS LINE!)]

# ['M1Sim' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_M1SIM_INITIAL = 14
ID_M1SIM_FINAL = 15
ID_M1SIM_MOVING = 16
ID_M1SIM_IDLE = 17

def M1Sim(  ):
    # set initial state
    state = ID_M1SIM_INITIAL

    while( True ):
        # State ID: ID_M1SIM_INITIAL
        if( state==ID_M1SIM_INITIAL ):
            # Transition ID: ID_M1SIM_TRANSITION_CONNECTION
            state = ID_M1SIM_IDLE

        # State ID: ID_M1SIM_IDLE
        elif( state==ID_M1SIM_IDLE ):
            if( ((dre.m1.laflag)==(True)) ):
                # Transition ID: ID_M1SIM_TRANSITION_CONNECTION
                state = ID_M1SIM_MOVING

            elif( ((dre.m1.simstop)==(True)) ):
                # Transition ID: ID_M1SIM_TRANSITION_CONNECTION
                state = ID_M1SIM_FINAL

        # State ID: ID_M1SIM_MOVING
        elif( state==ID_M1SIM_MOVING ):
            if( dre.m1.pos > dre.m1.setpoint ):
                # Transition ID: ID_M1SIM_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::incrDelta' begin]
                tmp=dre.m1.pos

                dre.m1.pos+=-1

                #print obtainVarName(dre.m1.pos)+":"+str(tmp)+"+"+str(-1)+"="+str(dre.m1.pos)
                # ['<global>::incrDelta' end]

            elif( dre.m1.setpoint > dre.m1.pos ):
                # Transition ID: ID_M1SIM_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::incrDelta' begin]
                tmp=dre.m1.pos

                dre.m1.pos+=1

                #print obtainVarName(dre.m1.pos)+":"+str(tmp)+"+"+str(1)+"="+str(dre.m1.pos)
                # ['<global>::incrDelta' end]

            else:
                # Transition ID: ID_M1SIM_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::notifyEndM1Mv' begin]
                dre.m1.mutex.acquire()

                try:

                    if (dre.m1.npflag):

                        print("notify M1 #1")

                        dre.m1.npflag = False

                        print("notify M1 #2")

                        dre.m1.laflag = False

                        print("notify M1 #3")

                        sendUntimelyResponse("p")

                        print("notify M1 #4")

                finally:

                    dre.m1.mutex.release()

                # ['<global>::notifyEndM1Mv' end]
                # ['<global>::setFlag' begin]
                dre.m1.laflag=False

                # ['<global>::setFlag' end]
                state = ID_M1SIM_IDLE

        # State ID: ID_M1SIM_FINAL
        elif( state==ID_M1SIM_FINAL ):
            return ID_M1SIM_FINAL

# ['M1Sim' end (DON'T REMOVE THIS LINE!)]

# ['M2Sim' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_M2SIM_INITIAL = 7
ID_M2SIM_FINAL = 8
ID_M2SIM_IDLE = 9
ID_M2SIM_MOVING = 10

def M2Sim(  ):
    # set initial state
    state = ID_M2SIM_INITIAL

    while( True ):
        # State ID: ID_M2SIM_INITIAL
        if( state==ID_M2SIM_INITIAL ):
            # Transition ID: ID_M2SIM_TRANSITION_CONNECTION
            state = ID_M2SIM_IDLE

        # State ID: ID_M2SIM_IDLE
        elif( state==ID_M2SIM_IDLE ):
            if( ((dre.m2.laflag)==(True)) ):
                # Transition ID: ID_M2SIM_TRANSITION_CONNECTION
                state = ID_M2SIM_MOVING

            elif( ((dre.m2.simstop)==(True)) ):
                # Transition ID: ID_M2SIM_TRANSITION_CONNECTION
                state = ID_M2SIM_FINAL

        # State ID: ID_M2SIM_FINAL
        elif( state==ID_M2SIM_FINAL ):
            return ID_M2SIM_FINAL

        # State ID: ID_M2SIM_MOVING
        elif( state==ID_M2SIM_MOVING ):
            if( dre.m2.setpoint > dre.m2.pos ):
                # Transition ID: ID_M2SIM_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::incrDelta' begin]
                tmp=dre.m2.pos

                dre.m2.pos+=1

                #print obtainVarName(dre.m2.pos)+":"+str(tmp)+"+"+str(1)+"="+str(dre.m2.pos)
                # ['<global>::incrDelta' end]

            elif( dre.m2.pos > dre.m2.setpoint ):
                # Transition ID: ID_M2SIM_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::incrDelta' begin]
                tmp=dre.m2.pos

                dre.m2.pos+=-1

                #print obtainVarName(dre.m2.pos)+":"+str(tmp)+"+"+str(-1)+"="+str(dre.m2.pos)
                # ['<global>::incrDelta' end]

            else:
                # Transition ID: ID_M2SIM_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::notifyEndM2Mv' begin]
                dre.m2.mutex.acquire()

                try:

                    if (dre.m2.npflag):

                        print("notify M2 #1")

                        dre.m2.npflag = False

                        print("notify M2 #2")

                        dre.m2.laflag = False

                        print("notify M2 #3")

                        sendUntimelyResponse("p")

                        print("notify M2 #4")

                finally:

                    dre.m2.mutex.release()

                # ['<global>::notifyEndM2Mv' end]
                # ['<global>::setFlag' begin]
                dre.m2.laflag=False

                # ['<global>::setFlag' end]
                state = ID_M2SIM_IDLE

# ['M2Sim' end (DON'T REMOVE THIS LINE!)]

# ['M2' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_M2_INITIAL = 11
ID_M2_FINAL = 12
ID_M2_WAITING = 13

def M2(  ):
    # set initial state
    state = ID_M2_INITIAL

    while( True ):
        # State ID: ID_M2_INITIAL
        if( state==ID_M2_INITIAL ):
            # Transition ID: ID_M2_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::setM2Response' begin]
            dre.m2.resp="OK"
            # ['<global>::setM2Response' end]
            state = ID_M2_WAITING

        # State ID: ID_M2_WAITING
        elif( state==ID_M2_WAITING ):
            if( ((dre.m2.np)==(True)) ):
                # Transition ID: ID_M2_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setMutexFlag' begin]
                dre.m2.mutex.acquire()

                try:

                    dre.m2.npflag=True

                finally:

                    dre.m2.mutex.release()
                # ['<global>::setMutexFlag' end]
                state = ID_M2_FINAL

            elif( ((dre.m2.m)==(True)) ):
                # Transition ID: ID_M2_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setMutexFlag' begin]
                dre.m2.mutex.acquire()

                try:

                    dre.m2.laflag=True

                finally:

                    dre.m2.mutex.release()
                # ['<global>::setMutexFlag' end]
                state = ID_M2_FINAL

            elif( ((dre.m2.reqpos)==(True)) ):
                # Transition ID: ID_M2_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setM2Response' begin]
                dre.m2.resp=str(dre.m2.pos)
                # ['<global>::setM2Response' end]
                state = ID_M2_FINAL

            elif( ((dre.m2.la)==(True)) ):
                # Transition ID: ID_M2_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setVar' begin]
                dre.m2.setpoint=(dre.m2.posarg)
                # ['<global>::setVar' end]
                state = ID_M2_FINAL

            else:
                # Transition ID: ID_M2_TRANSITION_CONNECTION
                state = ID_M2_FINAL

        # State ID: ID_M2_FINAL
        elif( state==ID_M2_FINAL ):
            return ID_M2_FINAL

# ['M2' end (DON'T REMOVE THIS LINE!)]

# ['M3Sim' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_M3SIM_INITIAL = 0
ID_M3SIM_FINAL = 1
ID_M3SIM_IDLE = 2
ID_M3SIM_MOVING = 3

def M3Sim(  ):
    # set initial state
    state = ID_M3SIM_INITIAL

    while( True ):
        # State ID: ID_M3SIM_INITIAL
        if( state==ID_M3SIM_INITIAL ):
            # Transition ID: ID_M3SIM_TRANSITION_CONNECTION
            state = ID_M3SIM_IDLE

        # State ID: ID_M3SIM_IDLE
        elif( state==ID_M3SIM_IDLE ):
            if( ((dre.m3.laflag)==(True)) ):
                # Transition ID: ID_M3SIM_TRANSITION_CONNECTION
                state = ID_M3SIM_MOVING

            elif( ((dre.m3.simstop)==(True)) ):
                # Transition ID: ID_M3SIM_TRANSITION_CONNECTION
                state = ID_M3SIM_FINAL

        # State ID: ID_M3SIM_FINAL
        elif( state==ID_M3SIM_FINAL ):
            return ID_M3SIM_FINAL

        # State ID: ID_M3SIM_MOVING
        elif( state==ID_M3SIM_MOVING ):
            if( dre.m3.setpoint > dre.m3.pos ):
                # Transition ID: ID_M3SIM_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::incrDelta' begin]
                tmp=dre.m3.pos

                dre.m3.pos+=1

                #print obtainVarName(dre.m3.pos)+":"+str(tmp)+"+"+str(1)+"="+str(dre.m3.pos)
                # ['<global>::incrDelta' end]

            elif( dre.m3.pos > dre.m3.setpoint ):
                # Transition ID: ID_M3SIM_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::incrDelta' begin]
                tmp=dre.m3.pos

                dre.m3.pos+=-1

                #print obtainVarName(dre.m3.pos)+":"+str(tmp)+"+"+str(-1)+"="+str(dre.m3.pos)
                # ['<global>::incrDelta' end]

            else:
                # Transition ID: ID_M3SIM_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::NotifyEndM3Mv' begin]
                dre.m3.mutex.acquire()

                try:

                    if (dre.m3.npflag):

                        print("notify M3 #1")

                        dre.m3.npflag = False

                        print("notify M3 #2")

                        dre.m3.laflag = False

                        print("notify M3 #3")

                        sendUntimelyResponse("p")

                        print("notify M3 #4")

                finally:

                    dre.m3.mutex.release()

                # ['<global>::NotifyEndM3Mv' end]
                # ['<global>::setFlag' begin]
                dre.m3.laflag=False

                # ['<global>::setFlag' end]
                state = ID_M3SIM_IDLE

# ['M3Sim' end (DON'T REMOVE THIS LINE!)]

# ['M3' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_M3_INITIAL = 4
ID_M3_FINAL = 5
ID_M3_WAITING = 6

def M3(  ):
    # set initial state
    state = ID_M3_INITIAL

    while( True ):
        # State ID: ID_M3_INITIAL
        if( state==ID_M3_INITIAL ):
            # Transition ID: ID_M3_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::setM3Response' begin]
            dre.m3.resp="OK"
            # ['<global>::setM3Response' end]
            state = ID_M3_WAITING

        # State ID: ID_M3_WAITING
        elif( state==ID_M3_WAITING ):
            if( ((dre.m3.np)==(True)) ):
                # Transition ID: ID_M3_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setMutexFlag' begin]
                dre.m3.mutex.acquire()

                try:

                    dre.m3.npflag=True

                finally:

                    dre.m3.mutex.release()
                # ['<global>::setMutexFlag' end]
                state = ID_M3_FINAL

            elif( ((dre.m3.m)==(True)) ):
                # Transition ID: ID_M3_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setMutexFlag' begin]
                dre.m3.mutex.acquire()

                try:

                    dre.m3.laflag=True

                finally:

                    dre.m3.mutex.release()
                # ['<global>::setMutexFlag' end]
                state = ID_M3_FINAL

            elif( ((dre.m3.reqpos)==(True)) ):
                # Transition ID: ID_M3_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setM3Response' begin]
                dre.m3.resp=str(dre.m3.pos)
                # ['<global>::setM3Response' end]
                state = ID_M3_FINAL

            elif( ((dre.m3.la)==(True)) ):
                # Transition ID: ID_M3_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::setVar' begin]
                dre.m3.setpoint=(dre.m3.posarg)
                # ['<global>::setVar' end]
                state = ID_M3_FINAL

            else:
                # Transition ID: ID_M3_TRANSITION_CONNECTION
                state = ID_M3_FINAL

        # State ID: ID_M3_FINAL
        elif( state==ID_M3_FINAL ):
            return ID_M3_FINAL

# ['M3' end (DON'T REMOVE THIS LINE!)]
