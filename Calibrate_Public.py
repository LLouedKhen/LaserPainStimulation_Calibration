# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:33:06 2020
This script controls the Stimul 1340 infrared laser remotely. 
It asks individuals to give a rating to administered pain using the Stimul 1340.
Parameters used here are Energy = 0.5:0.5:2.25 J, 6 mm spot, 4ms pulse duration,
3 repetition times.
Stimuli are presented randomly, 3 times each. Ratings per stim are then averaged. 
If my code is redundant, it's cuz I'm a mom. 
Don't forget your goggles. 
@author: Leyla Loued-Khenissi
lkhenissi@gmail.com
ToPLab, University of Geneva

"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
#sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts')
#sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts\\Laser')
#sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts\\PainBehavioral')
#sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts\\PainBehavioral\\TaskImagesAndScripts')
#sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts\\PainBehavioral\\Common')
#sys.path.append('C:\\Users\\louedkhe\\Documents\\PythonScripts\\PainBehavioral\\Peer_Test')

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
import time
from random import randint
import numpy as np
from datetime import datetime
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
#dataPath = '/Users/loued/Documents/Testing_StairCase_Sound/Sounds'
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
    
stairCase1 = pd.DataFrame([0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25])
stairCase1 = stairCase1.reset_index(drop=True)

#Max energy
linTest =  [2.25]

Rate1 = pd.Series(np.zeros([3]))
Pain1 = pd.Series(np.zeros([3]))
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
for i in range (0):
    markStart = (random.randrange(2, 9, 1))
    pain= linTest[i]
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

stairCase = pd.concat([stairCase1]*3)
stairCase  = stairCase.sample(frac=1).reset_index(drop=True)
stairList = stairCase[0].values.tolist()
Rate2 = pd.Series(np.zeros([len(stairCase)]))
Pain2 = pd.Series(np.zeros([len(stairCase)]))
Times = np.zeros([len(stairCase), 7])
    
pain =[]
TP4 = np.zeros([len(stairCase),1])
TP5 = np.zeros([len(stairCase),1])
Rate = np.zeros([len(stairCase),1])
Times =np.zeros([len(stairCase),7])

for i in range (0, len(stairCase)):
    markStart = (random.randrange(2, 9, 1))
    pain= stairList[i]
    LaserFootEnergy = pain
    Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
    print(fire)
    rateScale = visual.RatingScale(win = mywin, low=0, high=10, precision= 0.1, 
    pos=(0, -0.4), markerStart=markStart, choices =None, acceptPreText =None, 
    showValue = None, showAccept = None,scale = None,  textSize=0.5,
    leftKeys='left', rightKeys='right',acceptKeys ='return')
    while rateScale.noResponse:
        ratePain.draw()
        rateScale.draw()
        mywin.flip()
    Rate=rateScale.getRating()
    
    Rate2.iloc[i] = Rate
    Pain2.iloc[i] = pain
    print(Rate2[i])
    fdbk = visual.TextStim(win=mywin, text=(str(Rate2.iloc[i])),font='', units ='deg', pos=(0,0))
    fdbk.draw()
    mywin.flip()
    core.wait(2.0)
    FixationText.draw()
    mywin.flip()
    
toc = time.time() 


firstStim = pd.concat([Rate1, stairCase1], axis = 1)
firstStim.columns = ['rating1', 'Pain1']


allTypes = pd.concat([Rate2, stairCase], axis = 1)
allTypes.columns = ['rating', 'Pain']

meanResp = allTypes.groupby('Pain').mean()

fig = plt.figure()
plt.plot((meanResp.index), meanResp.rating)
plt.xlabel('Pain')
plt.ylabel('Rating')
fig.savefig(subject + '.jpg')

minThresh = np.argmin((np.abs(meanResp.rating -1)))

CeilingPain = (np.abs(meanResp.rating -10)).argmin()

#minPain = minThresh + 0.5
minPain= (np.abs(meanResp.rating- 1)).argmin()
if minPain == 0.5:
    minPain = 1
midPain= (np.abs(meanResp.rating- 5)).argmin()
if midPain == minPain or midPain < minPain:
    midPain = minPain + 0.25
maxPain= (np.abs(meanResp.rating- 8)).argmin()
if maxPain == midPain or maxPain < midPain:
    maxPain = midPain + 0.25
#maxPain= CeilingPain 

minPainRed = minPain -0.25
midPainRed = minPain
maxPainRed = midPain

subPain = [maxPain, midPain, minPain, minPainRed]

Result = visual.TextStim(win=mywin, text=('We will now present you with the 4 levels of pain to be used in the study, from lowest to highest.'),
pos=(0,-0.5),
depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', opacity=1.0, contrast=1.0, units='deg', 
ori=0.0, height=0.7,  antialias=True, bold=False, italic=False,  alignHoriz = 'center',
fontFiles=(), wrapWidth=20,  languageStyle='LTR', name=None, autoLog=None)
Result.draw()
mywin.flip()

for i in range(4):
    pain= subPain[i]
    LaserFootEnergy = pain
    Times, fire = FireLaser(LaserFootEnergy, pain, ser, i, LaserFootPulseCode, LaserFootSpotsizeCode, Times)
    print(fire)
    rem= visual.TextStim(win=mywin, text=('This is level ' + str(i) + '.'),
    pos=(0,-0.5),
    depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', opacity=1.0, contrast=1.0, units='deg', 
    ori=0.0, height=0.7,  antialias=True, bold=False, italic=False,  alignHoriz = 'center',
    fontFiles=(), wrapWidth=20,  languageStyle='LTR', name=None, autoLog=None)
    rem.draw()
    mywin.flip()
    core.wait(3.0)
    


DangerMax = 2.25
if CeilingPain> DangerMax:
    maxThresh = 2.25
    
minmidmaxVal = pd.DataFrame([minPain, minPainRed, midPain, midPainRed, maxPain, maxPainRed])

duration = pd.DataFrame([toc-tic/60])


if not os.path.exists(savePath):
    os.makedirs(savePath)
os.chdir(savePath)

allTimes = pd.DataFrame(Times)

allTimes.to_csv(os.path.join(savePath, subject + '_allTimes.csv'))
firstStim.to_csv(os.path.join(savePath, subject + '_FirstStim.csv'))
allTypes.to_csv(os.path.join(savePath, subject + '_All_BrutCalibration.csv'))
duration.to_csv(os.path.join(savePath, subject + '_CalibrationDuration.csv'))

minmidmaxVal.to_csv(os.path.join(savePath, subject + '_BrutPainCalibration_Values.csv'))


LaserPainFunClose(ser)

mywin.close()