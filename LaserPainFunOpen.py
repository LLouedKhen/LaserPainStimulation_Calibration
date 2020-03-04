#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:50:50 2019

@author: loued
"""
import serial as serial
import time
from random import randint
import numpy as np
from datetime import datetime
from serial_ports import serial_ports
import winsound

def LaserPainFunOpen(ser):
    #El En receives stuff in code
    #eg for laser pulse duration, code is x ms -1; so for 4 ms, it should be 3
    #Then the code for energy is ix([0.5:0.25:2]== xJ; for instance 0.5 J == 1
    #watch out for 0 indexing if in python
    #Then the spot size is the the size in mm -4; so for 4 mm, it is 0. 
    
    LaserFootPulse = 4; # ms not clear at all 
    LaserFootSpotsize =6 ; # mm
    LaserFootPulseCode = LaserFootPulse - 1;
    LaserFootSpotsizeCode = LaserFootSpotsize - 4;
    #  The following values are temporary, average  
    
#    thisPort = serial_ports()
#    
#    ser = serial.Serial(thisPort[0])  # open first serial port
#    print(ser.name)       # check which port was really used
#    ser.baudrate = 9600 #set baudrate to 9600 as in Manual p.47
#    ser.flush()
    
    switchSerial = input('Serial connection open on laser (1/0)?')
    if switchSerial == '1':
        t0=time.time()
        print('Connect to serial from the panel...')
        while time.time() -t0 <20:
            ser.write(b'P')          
            time.sleep(0.1)
            outIt =ser.read(6)
            print(list(outIt))
            if time.time() -t0 ==20:
                break
        
        #ser.read()
    
        #ser.write(str([str(80).encode('utf-8')]))
    Start = u'\u2560'
    End = u'\u2563'    
    Laser = u'\u004C'
    On1 = u'\u0031'
    
    #Now for some translating into uint8
    #Laser on, L111
    L1 = [204, 76, 49, 49, 49, 185]
    #Diode on, H111
    D1 = [204, 72, 49, 49, 49, 185]
    #Operate on, O111
    O1 = [204, 79, 49, 49, 49, 185]
    
    #FIRE
    #G1 = [204, 71, 49, 49, 49, 185]
    
    laserLit=[]
    diodeOn = []
    operateOn=[]
    
    startThis = input('Start laser (1/0)?')
    if startThis == '1':
        while 'L111' not in str(laserLit):
            t0=time.time()
            ser.write(L1)
            time.sleep(0.1)
            laserLit =ser.read(6)
            print(list(laserLit))
            if 'L111' in str(laserLit):
                t1=time.time() - t0
                laserLit =ser.read(6)
                print(list(laserLit))
                print('Laser on...')
                break 
                   
        time.sleep(1)
        t2=time.time() - t0
        ser.write(D1)
        time.sleep(0.1)
        diodeOn=ser.read(6)
        t3=time.time() - t0   
        print(list(diodeOn))
        if 'H111' in str(diodeOn):
            print('Diode on...')
        time.sleep(1)
        
        
        #O111 means the operate is ON state, that is the letter O, not zero
        t4=time.time() - t0
        ser.write(O1)
        time.sleep(0.1)
        operateOn = ser.read(6)
        print(list(operateOn))
        if 'O111' in str(operateOn):
            print('\n Operate on...')
        t5=time.time() - t0
        
        timesLaserOn = [t0, t1, t2, t3, t4, t5]
        return (timesLaserOn, LaserFootPulse, LaserFootSpotsize, LaserFootPulseCode, LaserFootSpotsizeCode, ser)