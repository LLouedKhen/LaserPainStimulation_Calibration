#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 16:01:19 2019

This script controls the Stimul 1340 infrared laser remotely. 
It employs a double random staircase procedure with pain energy ratings from 
0.5:0.5:2.25 J (Spot size 6mm, pulse duration 4 ms)
This code has not been tested with the machine, only with sound.
If my code is redundant, it's cuz I'm a mom. 
Don't forget your goggles. 
@author: Leyla Loued-Khenissi
lkhenissi@gmail.com
ToPLab, University of Geneva
"""


import os
import glob
import numpy as np
import re
import numpy.matlib
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
from psychopy import visual, core, event, sound, logging #import some libraries from PsychoPy
from psychopy.hardware import keyboard
import serial as serial
import math
from serial_ports import serial_ports
import winsound
from FireLaser import FireLaser
from LaserPainFunOpen import LaserPainFunOpen
from LaserPainFunClose import LaserPainFunClose


def subjIntake():

    subNum = input("Enter participant identifier: ") 
    while len(subNum)!= 3:
        print("Error! Must enter 3 characters!")
        subNum = input("Please re-enter participant identifier: ")     
        print(subNum)
    
    participant = input("Spouse, main participant or test? Enter 1 for main, 2 for spouse, 3 for test: ") 
    
    while len(participant) > 1:
        print("Error! Must enter 1, 2 or 3.")
        participant = input("Spouse, main or test participant? Enter 1 for main, 2 for spouse, 3 for test:  ")    
        print(participant)
        
    if participant == '1':
        string = 'OPPM'
    elif participant == '2':
        string = 'OPPS'
    elif participant == '3':
        string = 'LPTS'
        
    return(string, subNum)


#Enter your own path for the output here
procPath =''
os.chdir(procPath)   

string, subNum = subjIntake() 
    
subject = string  + subNum + '_Thresh'
subDir = os.path.join('' + string + subNum)
if not os.path.exists(subDir):
        os.makedirs(subDir)
os.chdir(subDir)
if not os.path.exists('Calibration'):
        os.makedirs('Calibration')
        
savePath =os.path.join('' + string + subNum + '\Calibration') 

os.chdir(savePath)
if not glob.glob('*.csv'):
    print("All clear.")
else:
    subjIntake() 
    
stairCase1 = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25]
stairCase2 = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25]

Rate1 = pd.Series(np.zeros([100]).astype('int'))
Rate2 = pd.Series(np.zeros([100]).astype('int'))
Pain1 = pd.Series(np.zeros([100]))
Pain2 = pd.Series(np.zeros([100]))

stairCase = []

i = 0

tic = time.time()

thisPort = serial_ports()
    
ser = serial.Serial(thisPort[0])  # open first serial port
print(ser.name)       # check which port was really used
ser.baudrate = 9600 #set baudrate to 9600 as in Manual p.47
ser.flush()

#In case the laser isn't on yet
openLaser =input('Shall we turn on the laser? (Y/N)')
if openLaser == 'Y':
    timesLaserOn, LaserFootPulse, LaserFootSpotsize, LaserFootPulseCode, LaserFootSpotsizeCode, ser= LaserPainFunOpen(ser)

    
Times =np.zeros([3,7])


#Timing 
clock = core.Clock()
#Keyboard
kb = keyboard.Keyboard()
kb.clock.reset()

#Screen, full screen or no?
whichWin = input('Are you testing? (Y/N)')
if whichWin == 'Y':
    mywin = visual.Window([900, 900],screen=0,  monitor="testMonitor",units='deg' )
   # win = visual.Window([900, 900],screen=1,  monitor="controlMonitor",units='deg' )
else:
    mywin = visual.Window([1280, 720],screen=0, fullscr=True, monitor="testMonitor", units="deg")
    #win = visual.Window([1280, 720],screen=1, fullscr=True, monitor="controlMonitor", units="deg")

Instructions1 = visual.TextStim(win=mywin, text=('You will now be subject to a series of laser stimulations.'),
pos=(0,1),
depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', opacity=1.0, contrast=1.0, units='deg', 
ori=0.0, height=0.7,  antialias=True, bold=False, italic=False,  alignHoriz = 'center',
fontFiles=(), wrapWidth=20,  languageStyle='LTR', name=None, autoLog=None)


Instructions2 = visual.TextStim(win=mywin, text=('You will first receive the highest level of pain possible for this experiment, \n\nso you can rate the following stimulations without fear of the unknown.\n\n'),
pos=(0,0),
depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', opacity=1.0, contrast=1.0, units='deg', 
ori=0.0, height=0.7,  antialias=True, bold=False, italic=False,  alignHoriz = 'center',
fontFiles=(), wrapWidth=20,  languageStyle='LTR', name=None, autoLog=None)

Instructions3 = visual.TextStim(win=mywin, text=('Afterwards, we will present you with a series of pain stimulations. \n\nPlease rate how painful the event was for you. \n\n0 indicates you felt no pain.  \n\n1 indicates you felt a first pain.\n\nPlease indicate your rating with the use of the left and right arrow keys, and the press enter.\n\nTo begin the procedure, press the space bar.'),
pos=(0,-0.5),
depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', opacity=1.0, contrast=1.0, units='deg', 
ori=0.0, height=0.7,  antialias=True, bold=False, italic=False,  alignHoriz = 'center',
fontFiles=(), wrapWidth=20,  languageStyle='LTR', name=None, autoLog=None)

FixationText= Instructions3 = visual.TextStim(win=mywin, text=('+'),
pos=(0,-0.5),
depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', opacity=1.0, contrast=1.0, units='deg', 
ori=0.0, height=0.7,  antialias=True, bold=False, italic=False,  alignHoriz = 'center',
fontFiles=(), wrapWidth=20,  languageStyle='LTR', name=None, autoLog=None)
Instructions1.draw()
mywin.flip()
core.wait(3)
#event.waitKeys()
#if 'escape' in event.waitKeys():
#    core.quit()
FixationText.draw()
mywin.flip()
#mywin.close() 

Instructions2.draw()
mywin.flip()
core.wait(3)

FixationText.draw()
mywin.flip()

Instructions3.draw()
mywin.flip()
core.wait(5)
event.waitKeys()
#if 'escape' in event.waitKeys():
#    core.quit()
FixationText.draw()
mywin.flip()



ratePain = visual.TextStim(win=mywin, text=('How painful was that?'),font='', pos=(0,0),
depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', opacity=1.0, contrast=1.0, units='deg', 
ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center',
fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)

pain =[]

crit = 5
i = 0
ii = 0
#while list(Rate1.values).count(1) < 3:
while Rate1.iloc[i-1] == 0 and Rate2.iloc[ii-1] == 0:
    i += 1
    ii += 1
    markStart = (random.randrange(2, 9, 1))
    pain= stairCase1[i]
    
    LaserFootEnergy = pain
    Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
    print(fire)
    rateScale = visual.RatingScale(win = mywin, low=0, high=10, precision= 0.1, 
    pos=(0, -0.4), markerStart=markStart, choices =None, acceptPreText =None, 
    showValue = None, showAccept = None, scale = None,  textSize=0.5,
    leftKeys='left', rightKeys='right',acceptKeys ='return')
    while rateScale.noResponse:
        ratePain.draw()
        rateScale.draw()
        mywin.flip()
    Rate=rateScale.getRating()
    Rate1.iloc[i] = Rate
    Pain1.iloc[i] = pain
    print(Rate1[i])
    fdbk = visual.TextStim(win=mywin, text=(str(Rate1.iloc[i])),font='', units ='deg', pos=(0,0),  alignHoriz='center')
    fdbk.draw()
    mywin.flip()
    core.wait(2.0)
    FixationText.draw()
    mywin.flip()

    pain= stairCase2[ii-1]
    LaserFootEnergy = pain
    Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
    print(fire)
    rateScale = visual.RatingScale(win = mywin, low=0, high=10, precision= 0.1, 
    pos=(0, -0.4), markerStart=markStart, choices =None, acceptPreText =None, 
    showValue = None, showAccept = None, scale = None,  textSize=0.5,
    leftKeys='left', rightKeys='right',acceptKeys ='return')
    while rateScale.noResponse:
        ratePain.draw()
        rateScale.draw()
        mywin.flip()
    Rate=rateScale.getRating()
    Rate2.iloc[i] = Rate
    Pain2.iloc[i] = pain
    print(Rate1[i])
    fdbk = visual.TextStim(win=mywin, text=(str(Rate1.iloc[i])),font='', units ='deg', pos=(0,0),  alignHoriz='center')
    fdbk.draw()
    mywin.flip()
    core.wait(2.0)
    FixationText.draw()
    mywin.flip()
    

thresh1 = Rate1.iloc[i-1].astype('int')
threshPain = stairCase1[thresh1]
threshI1 = i-1

thresh2 = Rate2.iloc[ii-1].astype('int')
threshDB2 = stairCase2[thresh2]
threshI2 = ii -2

Reversals = np.zeros([9,1])
#Reversals2 = np.zeros([9,1])

i = threshI1
l = threshI1

ii = threshI2
ll = threshI2

tic = time.time()


for k in range (0,8):
    while Rate1.iloc[l] != 5 and Rate2.iloc[ll] != 5 and i <= 8:
        i += 1
        l += 1
        ii += 1
        ll += 1
        if Rate1.iloc[l-1] == 5:
           pain= stairCase1[i-1]
           LaserFootEnergy = pain
           Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
           print(fire)
        else:
          
           pain= stairCase1[i]
           LaserFootEnergy = pain
           Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
           print(fire)
        while rateScale.noResponse:
            ratePain.draw()
            rateScale.draw()
            mywin.flip()
        Rating= rateScale.getRating()
        rateScale.reset()
        Rate1.iloc[l] = Rating
        Pain1.iloc[l] = pain
        print(Rate1[l])
        fdbk = visual.TextStim(win=mywin, text=(str(Rate1.iloc[l])),font='', pos=(0, 0))
        fdbk.draw()
        mywin.flip()
        core.wait(2.0)
        if Rate2.iloc[ll-1] == 5:
           pain= stairCase2[i]
           LaserFootEnergy = pain
           Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
           print(fire)  
        else:
            pain= stairCase2[ii]
            LaserFootEnergy = pain
            Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
            print(fire)    
        while rateScale.noResponse:
            ratePain.draw()
            rateScale.draw()
            mywin.flip()
        Rating= rateScale.getRating()
        rateScale.reset()
        Rate2.iloc[ll] = Rating
        Pain2.iloc[ll] = pain
        print(Rate2[ll])
        fdbk = visual.TextStim(win=mywin, text=(str(Rate2.iloc[ll])),font='', pos=(0, 0))
        fdbk.draw()
        mywin.flip()
        core.wait(2.0)
        j = l
        jj = ll
    Reversals[k] = 1
    while Rate1.iloc[l-1]!= 0 and  Rate2.iloc[ll -1] != 0 and i <= 15:
        i -= 1
        j += 1
        ii -= 1
        jj += 1
        if Rate1.iloc[l-1] == 0:
            pain= stairCase1[i+1 -1 -1]
            LaserFootEnergy = pain
            Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
            print(fire)    
        else:
            pain= stairCase1.iloc[i+1 -1]
            LaserFootEnergy = pain
            Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
            print(fire)    
        while rateScale.noResponse:
            ratePain.draw()
            rateScale.draw()
            mywin.flip()
        Rating= rateScale.getRating()
        rateScale.reset()
        Rate1.iloc[l] = Rating
        Pain1.iloc[l] = pain
        print(Rate1[l])
        fdbk = visual.TextStim(win=mywin, text=(str(Rate1.iloc[l])),font='', pos=(0, 0))
        fdbk.draw()
        mywin.flip()
        core.wait(2.0)
        if Rate2.iloc[l-1] == 0:
            pain= stairCase2[ii+1 -1 -1]
            LaserFootEnergy = pain
            Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
            print(fire)    
        else:
            pain= stairCase1[i+1 -1 -1]
            LaserFootEnergy = pain
            Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
            print(fire)  
        while rateScale.noResponse:
            ratePain.draw()
            rateScale.draw()
            mywin.flip()
        Rating= rateScale.getRating()
        rateScale.reset()
        Rate2.iloc[ll] = Rating
        Pain2.iloc[ll] = pain
        print(Rate2[ll])
        fdbk = visual.TextStim(win=mywin, text=(str(Rate2.iloc[ll])),font='', pos=(0, 0))
        fdbk.draw()
        mywin.flip()
        core.wait(2.0)            
        l = j
        ll = jj
    Reversals[k +1] = 1
 
toc = time.time() - tic
    
if not os.path.exists(savePath):
    os.makedirs(savePath)
os.chdir(savePath)     


out1 = pd.concat([Rate1, Rate2], axis = 0)
out2 = pd.concat([Pain1, Pain2], axis = 0)
outAll = pd.concat([out1, out2], axis = 1)
outAll = outAll.reset_index(drop=True)
outAll = outAll.drop(outAll.index[ll+1:len(outAll)])

outAll.columns = {'Rating', 'Pain (J)'}

weirdTrials = outAll[outAll.eq(0).all(1)]
dropDat = weirdTrials.index
outAll = outAll.drop(dropDat)
outAll.db = np.negative(outAll.db)

meanRate= outAll.groupby(['db']).mean()
meanThresh = outAll.groupby(['Rating']).mean()

minThresh = math.floor(meanThresh.iloc[0])
midThresh = math.floor(meanThresh.iloc[len(meanThresh)-1])
maxThresh = math.floor(midThresh + (midThresh -minThresh))
DangerMax = 0
if maxThresh > 0:
    maxThresh = 0
    
minmidmaxVal = pd.DataFrame([minThresh, midThresh, maxThresh])


plt.plot(Pain1)
plt.plot(Pain2)
plt.xlabel(['Trials'])
plt.ylabel(['Pain'])
plt.legend(['Staircase 1', 'Staircase 2'], loc='upper left')
plt.show()

plt.plot(meanRate)
plt.xlabel(['db'])
#plt.legend(['Staircase 1', 'Staircase 2'], loc='upper left')
plt.show()

minmidmaxVal = minmidmaxVal.append(pd.DataFrame([toc/60]))

outAll.to_csv(os.path.join(savePath, subject + '_All_StaircaseCalibration.csv'))

minmidmaxVal.to_csv(os.path.join(savePath, subject + '_StaircasePainCalibration_Values.csv'))

mywin.close()
