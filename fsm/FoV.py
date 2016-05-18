# ['Common imports' begin (DON'T REMOVE THIS LINE!)]
from FoV_CI import *
# ['Common imports' end (DON'T REMOVE THIS LINE!)]

# ['Common definitions for 'Hierarchical State Chart generator'' begin (DON'T REMOVE THIS LINE!)]
# Code items' definitions
# ['Common definitions for 'Hierarchical State Chart generator'' end (DON'T REMOVE THIS LINE!)]

# ['getCtrlResponse' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_GETCTRLRESPONSE_INITIAL = 7
ID_GETCTRLRESPONSE_FINAL = 8
ID_GETCTRLRESPONSE_READING = 9
ID_GETCTRLRESPONSE_FINISHING = 10

def getCtrlResponse(  ):
    # set initial state
    state = ID_GETCTRLRESPONSE_INITIAL

    while( True ):
        # State ID: ID_GETCTRLRESPONSE_INITIAL
        if( state==ID_GETCTRLRESPONSE_INITIAL ):
            # Transition ID: ID_GETCTRLRESPONSE_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::resetRxTask' begin]
            command_rx_buf=""
            # ['<global>::resetRxTask' end]
            # ['<global>::serialCharRead' begin]
            char_read=ser.read(1)
            # ['<global>::serialCharRead' end]
            state = ID_GETCTRLRESPONSE_READING

        # State ID: ID_GETCTRLRESPONSE_READING
        elif( state==ID_GETCTRLRESPONSE_READING ):
            if( char_read=='\10' or char_read=='\13' ):
                # Transition ID: ID_GETCTRLRESPONSE_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::serialCharRead' begin]
                char_read=ser.read(1)
                # ['<global>::serialCharRead' end]
                state = ID_GETCTRLRESPONSE_FINISHING

            elif( (char_read != '\10') and (char_read != '\13') ):
                # Transition ID: ID_GETCTRLRESPONSE_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::appendCharToRxBuf' begin]
                command_rx_buf+=char_read
                # ['<global>::appendCharToRxBuf' end]
                # ['<global>::serialCharRead' begin]
                char_read=ser.read(1)
                # ['<global>::serialCharRead' end]

        # State ID: ID_GETCTRLRESPONSE_FINISHING
        elif( state==ID_GETCTRLRESPONSE_FINISHING ):
            if( char_read=='\10' or char_read=='\13' ):
                # Transition ID: ID_GETCTRLRESPONSE_TRANSITION_CONNECTION
                state = ID_GETCTRLRESPONSE_FINAL

            elif( (char_read != '\10') and (char_read != '\13') ):
                # Transition ID: ID_GETCTRLRESPONSE_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::serialCharRead' begin]
                char_read=ser.read(1)
                # ['<global>::serialCharRead' end]

        # State ID: ID_GETCTRLRESPONSE_FINAL
        elif( state==ID_GETCTRLRESPONSE_FINAL ):
            return command_rx_buf

# ['getCtrlResponse' end (DON'T REMOVE THIS LINE!)]

# ['sendCtrlCommand' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_SENDCTRLCOMMAND_INITIAL = 5
ID_SENDCTRLCOMMAND_FINAL = 6

def sendCtrlCommand(  ):
    # set initial state
    state = ID_SENDCTRLCOMMAND_INITIAL

    while( True ):
        # State ID: ID_SENDCTRLCOMMAND_INITIAL
        if( state==ID_SENDCTRLCOMMAND_INITIAL ):
            # Transition ID: ID_SENDCTRLCOMMAND_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::serialCommandWrite' begin]
            ser.write(command_tx_buf+'\13')
            # ['<global>::serialCommandWrite' end]
            state = ID_SENDCTRLCOMMAND_FINAL

        # State ID: ID_SENDCTRLCOMMAND_FINAL
        elif( state==ID_SENDCTRLCOMMAND_FINAL ):
            return ID_SENDCTRLCOMMAND_FINAL

# ['sendCtrlCommand' end (DON'T REMOVE THIS LINE!)]

# ['getCtrlCommand' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_GETCTRLCOMMAND_INITIAL = 2
ID_GETCTRLCOMMAND_FINAL = 3
ID_GETCTRLCOMMAND_READING = 4

def getCtrlCommand(  ):
    # set initial state
    state = ID_GETCTRLCOMMAND_INITIAL

    while( True ):
        # State ID: ID_GETCTRLCOMMAND_INITIAL
        if( state==ID_GETCTRLCOMMAND_INITIAL ):
            # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::resetRxTask' begin]
            command_rx_buf=""
            # ['<global>::resetRxTask' end]
            # ['<global>::serialCharRead' begin]
            char_read=ser.read(1)
            # ['<global>::serialCharRead' end]
            state = ID_GETCTRLCOMMAND_READING

        # State ID: ID_GETCTRLCOMMAND_READING
        elif( state==ID_GETCTRLCOMMAND_READING ):
            if( char_read=='\10' or char_read=='\13' ):
                # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
                state = ID_GETCTRLCOMMAND_FINAL

            elif( (char_read != '\10') and (char_read != '\13') ):
                # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::appendCharToRxBuf' begin]
                command_rx_buf+=char_read
                # ['<global>::appendCharToRxBuf' end]
                # ['<global>::serialCharRead' begin]
                char_read=ser.read(1)
                # ['<global>::serialCharRead' end]

        # State ID: ID_GETCTRLCOMMAND_FINAL
        elif( state==ID_GETCTRLCOMMAND_FINAL ):
            return command_rx_buf

# ['getCtrlCommand' end (DON'T REMOVE THIS LINE!)]

# ['sendCtrlResponse' begin (DON'T REMOVE THIS LINE!)]
# State IDs
ID_SENDCTRLRESPONSE_INITIAL = 0
ID_SENDCTRLRESPONSE_FINAL = 1

def sendCtrlResponse(  ):
    # set initial state
    state = ID_SENDCTRLRESPONSE_INITIAL

    while( True ):
        # State ID: ID_SENDCTRLRESPONSE_INITIAL
        if( state==ID_SENDCTRLRESPONSE_INITIAL ):
            # Transition ID: ID_SENDCTRLRESPONSE_TRANSITION_CONNECTION
            # Actions:
            # ['<global>::serialResposeWrite' begin]
            ser.write(command_tx_buf+'\13'+'\10')
            # ['<global>::serialResposeWrite' end]
            state = ID_SENDCTRLRESPONSE_FINAL

        # State ID: ID_SENDCTRLRESPONSE_FINAL
        elif( state==ID_SENDCTRLRESPONSE_FINAL ):
            return ID_SENDCTRLRESPONSE_FINAL

# ['sendCtrlResponse' end (DON'T REMOVE THIS LINE!)]
