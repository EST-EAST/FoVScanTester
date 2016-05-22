# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:44:56 2016

@author: Txinto
"""
import sweepconfig
import errno
import sys
sys.path.insert(0, './fsm')

import FoV
import DRE
from datetime import datetime

cte_stepTime=1000
cte_timeout = 10

############ FUNCTIONS ##########################

def readCommand():
    ret=FoV.getCtrlCommand()
    FoV.dre.lastconnection = datetime.now()
    return ret

def sendResponse():
    FoV.dre.command_tx_buf = FoV.dre.response
    FoV.sendCtrlResponse()
    FoV.dre.lastconnection = datetime.now()
    FoV.dre.response=""

def serialClose():
    ser.close()             # close port

def m1sim(conn):
	print("Arranco el simulador")  
	FoV.dre.ser = conn
	#print("Voy simulando el motor: "+str(FoV.dre.m1.setpoint)+" "+str(FoV.dre.m1.pos))
	FoV.M1Sim()
	print("Saliendo del simulador")  

def m2sim(conn):
	print("Arranco el simulador")  
	FoV.dre.ser = conn
	#print("Voy simulando el motor: "+str(FoV.dre.m2.setpoint)+" "+str(FoV.dre.m2.pos))
	FoV.M2Sim()
	print("Saliendo del simulador") 

def m3sim(conn):
	print("Arranco el simulador")  
	FoV.dre.ser = conn
	#print("Voy simulando el motor: "+str(FoV.dre.m2.setpoint)+" "+str(FoV.dre.m2.pos))
	FoV.M3Sim()
	print("Saliendo del simulador") 
        
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    import FoV
    
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
    FoV.dre.ser = conn
    #infinite loop so that function do not terminate and thread do not end.
    endthread=False
    FoV.dre.lastconnection = datetime.now()
    while not(endthread):
        #print "Waiting for command"
	# Check if there is data
	data=""
	try:
		data = FoV.dre.ser.recv(1)

	except socket.error as e:
		print("Voy a ejecutar la excepcion")
		endthread = True
        	if e.errno == errno.ECONNRESET:
            		# Handle disconnection -- close & reopen socket etc.
			print "Disconnection ({0}): {1}".format(e.errno, e.strerror)
        	else:
            		# Other error, re-raise
			print "Timeout ({0}): {1}".format(e.errno, e.strerror)
	#print("longitud de data: "+str(len(data))+" : "+str(data))
	if ((datetime.now()-FoV.dre.lastconnection).total_seconds()>cte_timeout):
		print("Timeout manual")
		endthread=True
	if (not(endthread)):
		if (len(data)>=1):
			FoV.dre.rx_buffer=FoV.dre.rx_buffer+str(data)
			print("Buffer data"+FoV.dre.rx_buffer)
			readCommand()
			'''
			try:
			    print "hiola"
			    print "Arrived command: "+FoV.dre.command_rx_buf
			    print "adios"
			except: # catch *all* exceptions
			    e = sys.exc_info()[0]
			    print e
			''' 
			print "Arrived command: "+FoV.dre.command_rx_buf   
			FoV.dre.response=""
			FoV.CmdDispatcher()
			print "Decoder executed"
			if (FoV.dre.m1.req):
				FoV.M1()
				print "M1 simulator executed"
				FoV.dre.response = FoV.dre.m1.resp
				print "M1 Response to send "+FoV.dre.response
				sendResponse()			
			if (FoV.dre.m2.req):
				FoV.M2()
				print "M2 simulator executed"
				FoV.dre.response = FoV.dre.m2.resp
				print "M2 Response to send "+FoV.dre.response
				sendResponse()
			if (FoV.dre.m3.req):
				FoV.M3()
				print "M3 simulator executed"
				FoV.dre.response = FoV.dre.m3.resp
				print "M3 Response to send "+FoV.dre.response
				sendResponse()
    print("Cierro la conexion")
    FoV.dre.m1.simstop=True
    FoV.dre.m2.simstop=True
    FoV.dre.m3.simstop=True
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
    sckt.listen(1)
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
	#conn.settimeout(10)
	FoV.dre.m1.simstop=False
	idsim=start_new_thread(m1sim,(conn,))
	FoV.dre.m2.simstop=False
	idsim=start_new_thread(m2sim,(conn,))
	FoV.dre.m3.simstop=False
	idsim=start_new_thread(m3sim,(conn,))
        start_new_thread(clientthread ,(conn,))
    sckt.close
