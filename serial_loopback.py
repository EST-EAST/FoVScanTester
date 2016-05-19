# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:44:56 2016

@author: Txinto
"""
import sweepconfig
import sys
sys.path.insert(0, './fsm')

import FoV
import DRE

cte_stepTime=1000
cte_timeout = 2000

############ FUNCTIONS ##########################

def readCommand():
    '''
    current_command=""
    done=False
    while (done==False):
        char_read=sim_ser.read(1)
        if (char_read=='\13'):
            print "done: "+current_command
            done=True
        else:
            current_command+=char_read
            print "acum: "+current_command
    return current_command
    '''
    return FoV.getCtrlCommand()

def sendResponse():
    FoV.dre.command_tx_buf = FoV.dre.response
    FoV.sendCtrlResponse()

def serialClose():
    ser.close()             # close port

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    import FoV
    
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
    FoV.dre.ser = conn
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        ''' 
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data: 
            break
        print data
        conn.sendall(reply)
        '''
        print "Waiting for command"
        FoV.getCtrlCommand()
        try:
            print "hiola"
            print "Arrived command: "+FoV.dre.command_rx_buf
            print "adios"
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print e
            
        FoV.CmdDispatcher()
        print "Decoder executed"
        FoV.M1()
        print "M1 simulator executed"
        sendResponse()
        
    #came out of loop
    conn.close()

################ MAIN ####################

if not(sweepconfig.cte_use_socket):
    import serial
    cte_serial_port_loopback = sweepconfig.cte_serial_port_loopback
    print "Chosen serial port: "+cte_serial_port_loopback
    ser = serial.Serial(
        port=cte_serial_port_loopback,
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
    import socket
    import sys
    from thread import *

    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
    #Bind socket to local host and port
    try:
        sckt.bind((sweepconfig.cte_socket_ip, sweepconfig.cte_socket_port))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    print 'Socket bind complete'
    #Start listening on socket
    sckt.listen(10)
    print 'Socket now listening'
 
FoV.dre.cte_use_socket = sweepconfig.cte_use_socket

if not(sweepconfig.cte_use_socket):
    while (True):
        print ("Me pongo a leer el comando")
        command=readCommand()
        print("Comando: "+command)
        sendResponse(len(command))
    ser.close()
else:     
    while (True):
        #wait to accept a connection - blocking call
        conn, addr = sckt.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread ,(conn,))
    sckt.close

    