# -*- coding: utf-8 -*-
"""
Simulator of GCS on TCP system
"""
import scanconfig
import errno
import sys
sys.path.insert(0, './fsm')

import DRE

from thread import *
from datetime import datetime

# Generic code items' definitions
dre = DRE.DRE()
cte_stepTime=1000
cte_timeout = 20

############ FUNCTIONS ##########################
# Code items' definitions
def serialCharRead(  ):
        readlen=0
        while(readlen<1):
            data = dre.ser.recv(1)
            readlen=len(data)

        dre.char_read=str(data)[0]

ID_GETCTRLCOMMAND_INITIAL = 43
ID_GETCTRLCOMMAND_FINAL = 44
ID_GETCTRLCOMMAND_READING = 45
ID_GETCTRLCOMMAND_PREVBUF = 46

state = ID_GETCTRLCOMMAND_INITIAL

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
                # ['<global>::prependActiveMotor' end]
                state = ID_GETCTRLCOMMAND_FINAL

            elif( len(dre.rx_buffer)<1 ):
                # Transition ID: ID_GETCTRLCOMMAND_TRANSITION_CONNECTION
                # Actions:
                # ['<global>::appendCharToRxBuf' begin]
                dre.command_rx_buf += dre.char_read
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


def readCommand():
    ret=getCtrlCommand()
    dre.lastconnection = datetime.now()
    return ret


def sendResponse():
    dre.ser.sendall(dre.command_tx_buf+chr(13)+chr(10))
    print "Envie " + dre.command_tx_buf+chr(13)+chr(10)
    dre.lastconnection = datetime.now()
    dre.response=""


def serialClose():
    ser.close()             # close port


def processCommand():
    readCommand()
    print "Arrived command: " + dre.command_rx_buf
    dre.command_tx_buf = "0 1 2 3 4"
    sendResponse()


#Function for handling connections. This will be used to create threads
def clientthread(conn):

    #Sending message to connected client
    dre.ser = conn
    #infinite loop so that function do not terminate and thread do not end.
    endthread=False
    dre.lastconnection = datetime.now()
    while not(endthread):
        #print "Waiting for command"
        # Check if there is data
        data=""
        try:
            data = dre.ser.recv(1)
        except socket.error as e:
            print("Voy a ejecutar la excepcion")
            endthread = True
            if e.errno == errno.ECONNRESET:
                        # Handle disconnection -- close & reopen socket etc.
                print "Disconnection ({0}): {1}".format(e.errno, e.strerror)
            else:
                # Other error, re-raise
                print "Timeout ({0}): {1}".format(e.errno, e.strerror)
        #print(str((datetime.now()-dre.lastconnection).total_seconds()))
        if ((datetime.now()-dre.lastconnection).total_seconds()>cte_timeout):
            print("Timeout manual")
            endthread=True
        if (not(endthread)):
            #print("Parece que no salgo")
            if (len(data)>=1):
                dre.rx_buffer=dre.rx_buffer+str(data)
                # print("Buffer data"+dre.rx_buffer)
                processCommand()

                
    print("Cierro la conexion")
    conn.close()

################ MAIN ####################

dre.disable_untimely_resp = scanconfig.cte_sim_disable_untimely_resp

import socket
import sys

sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
#Bind socket to local host and port
try:
    sckt.bind((scanconfig.cte_command_gcs_ip, scanconfig.cte_command_gcs_port))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'
#Start listening on socket
sckt.listen(1)
print 'Socket now listening'

dre.cte_use_socket = scanconfig.cte_use_socket

while (True):
    #wait to accept a connection - blocking call
    conn, addr = sckt.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    conn.settimeout(10)
    start_new_thread(clientthread ,(conn,))
sckt.close
