# -*- coding: utf-8 -*-
from threading import Thread, Lock

class Motor:

    mutex = Lock()

    en = False
    cmd = ""
    req = False
    resp = ""

    la = False
    np = False
    reqpos = False
    m = False
    spd = False

    spdarg = 0
    posarg = 0

    pos = 0
    setpoint = pos

    npflag = False
    laflag = False
    simstop = False

    hosp = False
    goix = False
    apl = False
    gohoseq = False
    
class DRE:
    lastconnection = None
    m1 = Motor()
    m2 = Motor()
    m3 = Motor()
    mX = m1
    rx_buffer=""
    command_rx_buf = ""
    char_read = '\0'
    ser = None
    command_tx_buf = ""
    cte_use_socket = False
    response = "Wey"
    activeMotorPrefix = ""
    m1port=0
    m2port=0
    m3port=0
