#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 16:01:19 2019
Double random staircase procedure using sounds (not loud enough, too loud).
Recommend testing this before using it with the laser pain stimulation device. 

@author: loued
"""

#wavTones.com.unregistred.burst_75Hz_-6dBFS_x3.wav

import sounddevice as sd
import soundfile as sf
import os
import glob
import numpy as np
import re
import time
import pandas as pd
import math
import random
import matplotlib.pyplot as plt
from psychopy import visual, core, event, sound, logging #import some libraries from PsychoPy
from psychopy.hardware import keyboard

#Your Output Path here 
procPath = '' 
#Your sound stim Path here 
dataPath = ''
os.chdir(dataPath)

subNum = input("Enter participant identifier: ") 
while len(subNum)!= 3:
    print("Error! Must enter 3 characters!")
    input("Please re-enter participant identifier: ")     
    print(subNum)


participant = input("Spouse or main participant? Enter 1 for main, 2 for spouse: ") 

while len(participant) > 1:
    print("Error! Must enter 1 or 2!")
    participant = input("Spouse or main participant? Enter 1 for main, 2 for spouse:  ")    
    print(participant)
    
if participant == '1':
    string = 'OPPM'
elif participant == '2':
    string = 'OPPS'
    
subject = string + '_Thresh' + subNum

savePath =os.path.join('' + string + subNum + '/Calibration') 

filenames = glob.glob('*.wav')
fileDBs = np.zeros(len(filenames))

regex = re.compile(r'\d+')
for i in range(0,len(filenames)):
    fileDBs[i] = regex.findall(filenames[i])[1]
fileDBs[fileDBs.any==5] = 5
fileDBs = fileDBs.astype(int)
idx1 = np.argsort(fileDBs)
fileDB = fileDBs[idx1]
fileDB[fileDB > 0] = np.negative(fileDB[fileDB > 0])
soundFiles = pd.DataFrame(np.transpose([fileDBs, filenames]))
soundFiles[0] = soundFiles[0].astype('int') 
soundFiles = soundFiles.sort_values(by =[0], ascending = False)

stairCase1 = soundFiles
stairCase1 = stairCase1.reset_index(drop=True)
stairCase2 = soundFiles
stairCase2 = stairCase2.reset_index(drop=True)
#


Rate1 = pd.Series(np.zeros([100]).astype('int'))
sounds1 = pd.Series(np.zeros([100]).astype('int'))
dbs1 = pd.Series(np.zeros([100]).astype('int'))
Rate2 = pd.Series(np.zeros([100]).astype('int'))
sounds2 = pd.Series(np.zeros([100]).astype('int'))
dbs2 = pd.Series(np.zeros([100]).astype('int'))


#Timing 
clock = core.Clock()
#Keyboard
kb = keyboard.Keyboard()
kb.clock.reset()

#Screen
mywin = visual.Window([900,900], [0, 0], monitor="testMonitor", units="deg")

markStart = (random.randrange(2, 9, 1))

rateSound = visual.TextStim(win=mywin, text=('How loud is the sound from 0 to 10? 0 indicates you cannot hear it.'),font='', pos=(0, 0),
depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
ori=1.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)

ratingScale = visual.RatingScale(win = mywin, low=0, high=10, precision= 0.1, 
pos=(0, -0.4),choices =None,scale= None, acceptPreText =None, 
showValue = None, markerStart=markStart, showAccept = None, labels=None, stretch=2.0, 
leftKeys='left', rightKeys='right',acceptKeys ='return', maxTime=5)

stairCase = []

fs =44100

crit = 5
i = 0
ii = 0
#while list(Rate1.values).count(1) < 3:
while Rate1.iloc[i-1] == 0 and Rate2.iloc[ii-1] == 0:
    i += 1
    ii += 1
    file= stairCase1.iloc[i-1,1]
    db= stairCase1.iloc[i-1,0]
    print(file)
    data, fs = sf.read(stairCase1.iloc[i-1,1], dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing
    while ratingScale.noResponse:
        rateSound.draw()
        ratingScale.draw()
        mywin.flip()
    Rating= ratingScale.getRating()
    ratingScale.reset()
    Rate1.iloc[i-1] = Rating
    sounds1.iloc[i-1] = file
    dbs1.iloc[i-1] = db
    print(Rate1[i-1])
    fdbk = visual.TextStim(win=mywin, text=(str(Rate1.iloc[i-1])),font='', pos=(0, 0))
    fdbk.draw()
    mywin.flip()
    core.wait(2.0)

    file= stairCase2.iloc[ii-1,1]
    db= stairCase2.iloc[ii-1,0]
    print(file)
    data, fs = sf.read(stairCase2.iloc[ii-1,1], dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing
    while ratingScale.noResponse:
        rateSound.draw()
        ratingScale.draw()
        mywin.flip()
    Rating= ratingScale.getRating()
    ratingScale.reset()
    Rate2.iloc[ii-1] = Rating
    sounds2.iloc[ii-1] = file
    dbs2.iloc[ii-1] = db
    print(Rate1[ii-1])
    fdbk = visual.TextStim(win=mywin, text=(str(Rate2.iloc[ii-1])),font='', pos=(0, 0))
    fdbk.draw()
    mywin.flip()
    core.wait(2.0)
    

thresh1 = Rate1.iloc[i-1].astype('int')
threshFile1= stairCase1.iloc[thresh1,1]
threshDB = stairCase1.iloc[thresh1,0]
threshI1 = i-1

thresh2 = Rate2.iloc[ii-1].astype('int')
threshFile2= stairCase2.iloc[thresh2,1]
threshDB2 = stairCase2.iloc[thresh2,0]
threshI2 = ii -2

Reversals = np.zeros([9,1])
#Reversals2 = np.zeros([9,1])

i = threshI1
l = threshI1

ii = threshI2
ll = threshI2

tic = time.time()


for k in range (0,8):
    while Rate1.iloc[l] != 5 and Rate2.iloc[ll] != 5 and i <= 15:
        i += 1
        l += 1
        ii += 1
        ll += 1
        if Rate1.iloc[l-1] == 5:
            file= stairCase1.iloc[i-1,1]
            db= stairCase1.iloc[i-1,0]
            print(file)
            data, fs = sf.read(stairCase1.iloc[i-1,1], dtype='float32')  
            sd.play(data, fs)
            status = sd.wait()  # Wait until file is done playing
        else:
            file= stairCase1.iloc[i,1]
            db= stairCase1.iloc[i,0]
            print(file)
            data, fs = sf.read(stairCase1.iloc[i,1], dtype='float32')  
            sd.play(data, fs)
            status = sd.wait()  # Wait until file is done playing
        while ratingScale.noResponse:
            rateSound.draw()
            ratingScale.draw()
            mywin.flip()
        Rating= ratingScale.getRating()
        ratingScale.reset()
        Rate1.iloc[l] = Rating
        sounds1.iloc[l] = file
        dbs1.iloc[l] = db
        print(Rate1[l])
        fdbk = visual.TextStim(win=mywin, text=(str(Rate1.iloc[l])),font='', pos=(0, 0))
        fdbk.draw()
        mywin.flip()
        core.wait(2.0)
        if Rate2.iloc[ll-1] == 5:
            file= stairCase2.iloc[ii-1,1]
            db= stairCase2.iloc[ii-1,0]
            print(file)
            data, fs = sf.read(stairCase2.iloc[ii-1,1], dtype='float32')  
            sd.play(data, fs)
            status = sd.wait()  # Wait until file is done playing    
        else:
            file= stairCase2.iloc[ii,1]
            db= stairCase2.iloc[ii,0]
            print(file)
            data, fs = sf.read(stairCase2.iloc[ii,1], dtype='float32')  
            sd.play(data, fs)
            status = sd.wait()  # Wa   
        while ratingScale.noResponse:
            rateSound.draw()
            ratingScale.draw()
            mywin.flip()
        Rating= ratingScale.getRating()
        ratingScale.reset()
        Rate2.iloc[ll] = Rating
        sounds2.iloc[ll] = file
        dbs2.iloc[ll] = db
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
            file= stairCase1.iloc[i+1 -1 -1,1]
            db= stairCase1.iloc[i+1 -1 -1,0]
            print(file)
            data, fs = sf.read(stairCase1.iloc[i+1-1 -1,1], dtype='float32')  
            sd.play(data, fs)
            status = sd.wait()  # Wait until file is done playing
        else:
            file= stairCase1.iloc[i+1 -1,1]
            db= stairCase1.iloc[i+1 -1,0]
            print(file)
            data, fs = sf.read(stairCase1.iloc[i+1 -1,1], dtype='float32')  
            sd.play(data, fs)
            status = sd.wait()  # 
        while ratingScale.noResponse:
            rateSound.draw()
            ratingScale.draw()
            mywin.flip()
        Rating= ratingScale.getRating()
        ratingScale.reset()
        Rate1.iloc[l] = Rating
        sounds1.iloc[l] = file
        dbs1.iloc[l] = db
        print(Rate1[l])
        fdbk = visual.TextStim(win=mywin, text=(str(Rate1.iloc[l])),font='', pos=(0, 0))
        fdbk.draw()
        mywin.flip()
        core.wait(2.0)
        if Rate2.iloc[l-1] == 0:
            file= stairCase2.iloc[ii+1 -1 -1,1]
            db= stairCase2.iloc[ii+1 -1 -1,0]
            print(file)
            data, fs = sf.read(stairCase2.iloc[ii+1-1 -1,1], dtype='float32')  
            sd.play(data, fs)
            status = sd.wait()  # Wait until file is done playing
        else:
            file= stairCase1.iloc[i+1 -1 -1,1]
            db= stairCase1.iloc[i+1 -1 -1,0]
            print(file)
            data, fs = sf.read(stairCase1.iloc[i+1 -1 -1,1], dtype='float32')  
            sd.play(data, fs)
            status = sd.wait()  #   
        while ratingScale.noResponse:
            rateSound.draw()
            ratingScale.draw()
            mywin.flip()
        Rating= ratingScale.getRating()
        ratingScale.reset()
        Rate2.iloc[ll] = Rating
        sounds2.iloc[ll] = file
        dbs2.iloc[ll] = db
        print(Rate1[ll])
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
out2 = pd.concat([dbs1, dbs2], axis = 0)
outAll = pd.concat([out1, out2], axis = 1)
outAll = outAll.reset_index(drop=True)
outAll = outAll.drop(outAll.index[ll+1:len(outAll)])

outAll.columns = {'Rating', 'db'}

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
    
trudbs1 = np.negative(dbs1[dbs1 != 0])
trudbs2 =np.negative(dbs2[dbs2 != 0])

plt.plot(trudbs1)
plt.plot(trudbs2)
plt.xlabel(['Trials'])
plt.ylabel(['dB'])
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
