# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:26:24 2020

@author: louedkhe
"""
import sys
sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts')
sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts\\PainBehavioral')
import serial as serial
import time
from random import randint
import numpy as np
from datetime import datetime
from serial_ports import serial_ports
import winsound


def LaserPainFunClose(ser):

    
    #Laser on, L111
    L0 = [204, 76, 48, 48, 48, 185]
    #Diode on, H111
    D0 = [204, 72, 48, 48, 48, 185]
    #Operate on, O111
    O0 = [204, 79, 48, 48, 48, 185]
    
    
    ser.write(O0)
    time.sleep(1)
    #H000 means the diode is OFF state
    ser.write(D0)
    time.sleep(1)
       
     #L000 means the laser is OFF state
    ser.write(L0)
    time.sleep(1)

    ser.close()
