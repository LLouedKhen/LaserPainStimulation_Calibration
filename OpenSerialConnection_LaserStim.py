# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 10:41:35 2020
This script opens the serial connection to the Stimul 1340. 
Is it ideal? No. But it works. Only, for some reason, it hangs once the connection is
established. Ctrl-c doesn't work, you have to restart the kernel...So kind of a pain. 
Don't forget your goggles. 
@author: Leyla Loued-Khenissi
lkhenissi@gmail.com
ToPLab, University of Geneva
"""
import sys
#sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts')
#sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts\\PainBehavioral')

import time
import serial as serial
from serial_ports import serial_ports



thisPort = serial_ports()
    
ser = serial.Serial(thisPort[0])  # open first serial port
print(ser.name)       # check which port was really used
ser.baudrate = 9600 #set baudrate to 9600 as in Manual p.47
ser.flush()

switchSerial = input('Serial connection open on laser (1/0)?')
if switchSerial == '1':
    t0=time.time()
    print('Connect to serial from the panel...')
    while time.time() -t0 <20:
        ser.write(b'P')          
        time.sleep(0.1)
        outIt =ser.read(6)
        print(list(outIt))
        if (list(outIt)) == [80, 80, 80, 80, 80, 80]:
            print('We have contact')
            core.wait(5)
            break
        
#ser.close()