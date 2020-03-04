# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 12:04:17 2020

@author: louedkhe
"""

import serial as serial
import time
from random import randint
import numpy as np
from datetime import datetime
from serial_ports import serial_ports
import winsound
import sys 

def FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times):
 

       #FIRE code
    G1 = [204, 71, 49, 49, 49, 185]
    print('Trial ' + str(i))
    Times[i,0] = time.time()

    LaserFootEnergyCode = int((LaserFootEnergy/0.25)-1);
    
    if pain > 0:
     #C is to calibrate, followed by pulse parameter d (1ms * d +1), and e, energy (which is the c parameter of the P command, from 1 to 59)
        Times[i,1]= time.time() - Times[i,0]
        calSTR = [204, 67, LaserFootPulseCode,  LaserFootEnergyCode,  1, 185]
        ser.write(calSTR)
        resp = []
        time.sleep(0.1)
        resp = ser.read(6)
        calDone = [204, 86, LaserFootEnergyCode, 63, 63, 185]
        while 'V' not in str(resp):
            resp = ser.read(6)
            print(list(resp))
            print(chr(resp[1]), chr(resp[2]), chr(resp[3]), chr(resp[4]))
            print('\n Calibrating...')
            if 'V' in str(resp):
                print(('\n Calibrated.'))
                Times[i,2] = time.time() - Times[i,0]
                #durCal[i] = timeCalE[i] - timeCalS[i]
                time.sleep(1)   
                #P, set parameters {abc}, pulse parameter (1ms * (a + 1)), energy parameter b, (0.25 * (b +1)), spot size c in mm (diameter)
        pStr = [204, 80, LaserFootPulseCode, LaserFootEnergyCode, LaserFootSpotsizeCode, 185]
        resp2 = []
        ser.write(pStr)
        Times[i,3] = time.time() - Times[i,0]
        time.sleep(0.1)
        resp2 = ser.read(6)     
        while 'P'not in str(resp2):
            ser.write(pStr)
            time.sleep(0.1)
            resp2 = ser.read(6)
            print('\n Setting Parameters...')
            print(list(resp))
        if 'P' in str(resp2):
            print("Parameters set")
            Times[i,4] = time.time() - Times[i,0]
            time.sleep(1)
            print('Press the laser foot pedal NOW !!!!!!\n')
            winsound.Beep(1000, 100)
            Times[i,5] = time.time() - Times[i,0]
            time.sleep(3)
                        #Now G is the most relevant. It is th1e pain delivery
            print('\n FIRE.')
            ser.write(G1)
            time.sleep(0.1)
            resp3 = ser.read(6)
            print(list(resp3)) 
            if 'G111' in str(resp3):
                print('Laser pulse sent.')
                Times[i,6] = time.time() - Times[i,0]
                fire = 1
                print('Release Laser Foot Pedal NOW!\n');
            else:
                print('NO PULSE')
                time.sleep(1)
                fire = 0
                Times[i,6] = 0
            
            ser.flush() 

    #Times = [tStart, timeCalS, timeCalE, timeP, timePSet, timeFP, timeFire]
    return Times, fire