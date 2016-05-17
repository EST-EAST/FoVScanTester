# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:44:56 2016

@author: Txinto
"""


import serial
import sweepconfig

cte_serial_port_loopback = sweepconfig.cte_serial_port_loopback

print "Chosen serial port: "+cte_serial_port_loopback

cte_stepTime=1000
cte_timeout = 2000

def readCommand():
    current_command=""
    done=False
    while (done==False):
        char_read=ser.read(1)
        if (char_read=='\13'):
            print "done: "+current_command
            done=True
        else:
            current_command+=char_read
            print "acum: "+current_command
    return current_command

def sendResponse(response_lenght):
    response = ""
    for i in range (1,response_lenght+1):
        response += str(i)
    ser.write(response+'\13'+'\10')

def serialClose():
    ser.close()             # close port
    
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

while (True):
    command=readCommand()
    print("Comando: "+command)
    sendResponse(len(command))