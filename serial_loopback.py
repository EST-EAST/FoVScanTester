# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:44:56 2016

@author: Txinto
"""

import os
import serial

if (os.name == 'nt'):
    cte_serial_port = 'COM2:'
else:
    cte_serial_port = '/dev/ttyUSB1'

print "Chosen serial port: "+cte_serial_port


cte_stepTime=1000
cte_timeout = 2000

def readCommand():
    current_command=""
    done=False
    while (done==False):
        char_read=ser.read(1)
        if (char_read=='\0'):
            done=True
        else:
            current_command+=char_read
    return current_command

def sendResponse(response_lenght):
    response = ""
    for i in range (1,response_lenght+1):
        response += str(i)
    ser.write(response+'\0')

def serialClose():
    ser.close()             # close port
    
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

while (True):
    command=readCommand()
    print("Comando: "+command)
    sendResponse(len(command))