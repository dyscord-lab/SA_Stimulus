
# Virtual Ball Toss Game 
# version of 'Cyberball' - https://www.ncbi.nlm.nih.gov/pubmed/16817529
# for PsychoPy (using Python2.7) 

# developed by for use as an fMRI task by the Communication Neuroscience Lab
# original Matlab implementation by Josh Carp
# PsychoPy Python version by Matt O'Donnell (mbod@asc.upenn.edu)

from psychopy import visual, core, logging, event, data, gui
import sys
import random
import csv
import serial
import os
import time
from random import shuffle


#################
#  PARAMETERS #
#################

maxTime=25 #length of time that player is allowed to hold ball before round ends
maxTrials=10 #number of throws allowed per round
incRounds=1 #number of inclusive rounds
exRounds=1 #number of exclusive rounds
#set variables below vvv
holder=1
round=1
trialCnt=0
rndCnt=0
condition="FBALL"

# these instructions aren't displayed anywhere when run??
instructions1 = '''
In the upcoming task, we will test the effects of practicing mental visualization on task performance. Thus, we need you to practice your mental visualization skills. We have found that the best way to do this is to have you play an on-line ball tossing game with other participants who are logged on to the system at the same time.

In a few moments, you will be playing a ball-tossing game with other students over our network. Several universities in the state of Michigan are taking part in a collaborative investigation of the effects of mental visualization on task performance, with high school students participating at several different Universities around the state of Michigan.
'''

instructions2 = '''
The game is very simple. When the ball is tossed to you, simply press either the "2" key (pointer finger) to throw to the player on your left or the "3" key (middle finger) for to throw to the player on your right. When the game is over, the experimenter will give you additional instructions.

What is important is not your ball tossing performance, but that you MENTALLY VISUALIZE the entire experience. Imagine what the others look like. What sort of people are they? Where are you playing? Is it warm and sunny or cold and rainy? Create in your mind a complete mental picture of what might be going on if you were playing this game in real life.
'''


# get subjID
subjDlg = gui.Dlg(title="App Task")
subjDlg.addField('Enter Subject ID:')
subjDlg.addField('Player name:')
subjDlg.addField("Room:")
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
    player_name=subjDlg.data[1]
    round_number=subjDlg.data[2] #add round input
    try:
        room = int(subjDlg.data[2])-1
    except:
        room=0
else:
    sys.exit()
 
 
players=[["Justin", "Will"], #assigned through room number
                ["Nick", "Robin"], 
                ["John", "Andrew"]]

player1_name = players[room][0]
player3_name = players[room][1]

  
################
# Set up images (for players) #
################
paths = [d for d in os.listdir('images') if d[1:3]=='to']
throw={}
for p in paths:
    throw[p]=[f for f in os.listdir('images/%s' % p) if f.endswith('.bmp')]

 
################
# Set up window #
################

useFullScreen=True #Set to true for full screen
win = visual.Window([1680,1050], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False, color="#FFFFFF")

################
# Set up stimuli #
################ 

title=visual.TextStim(win,text="Welcome to the Virtual Ball-Tossing Game, an Interactive Task Used for Mental Visualization!", height=0.8, pos=(0,7),color="#000000")
instrText = visual.TextStim(win, text="",height=0.6, color="#000000", wrapWidth=16) #empty text, optional to fill
instrKey = visual.TextStim(win, text="", height=0.6, color="#000000", pos=(0,-5))
instr_p1 = visual.TextStim(win, text="",color="#000000", pos=(-6,3), height=0.6, alignHoriz="left")
instr_p2 = visual.TextStim(win, text="",color="#000000", pos=(-6, 0), height=0.6, alignHoriz="left")
instr_p3 = visual.TextStim(win, text="",color="#000000", pos=(-6, -3), height=0.6, alignHoriz="left")
p1_tick = visual.TextStim(win,text="", color="#000000", pos=(3.5,3.15), alignHoriz="left")
p3_tick = visual.TextStim(win,text="", color="#000000", pos=(3.5,-2.85), alignHoriz="left")

instr1 = visual.TextStim(win, text="Welcome to the experiment. First, you are going to play and interactive ball tossing game. Press any key to continue." , color="#000000")
instr2= visual.TextStim(win, text="Look at some pictures. intructions instructions" , color="#000000")
instr3= visual.TextStim(win, text="final bullshit. press any key to continue" , color="#000000")
imagestart= visual.TextStim(win, text="You will now view a series of images. Try to visualize yourself actually being in each scene." , color="#000000")

players = visual.SimpleImageStim(win, image='images/start.bmp')

round_fix = visual.TextStim(win, text="", height=1.5, color="#000000")

fixation = visual.TextStim(win, text="Please wait...", height=2, color="#000000")

goodbye = visual.TextStim(win,text="",color="#000000")

p1name = visual.TextStim(win,text=player1_name,color="#000000", pos=(-6,2), height=0.5)
p2name = visual.TextStim(win,text=player_name,color="#000000", pos=(0,-5), height=0.5)
p3name = visual.TextStim(win,text=player3_name,color="#000000", pos=(6,2), height=0.5)

ready_screen = visual.TextStim(win, text="Ready.....", height=1.2, color="#000000")

#intro questions
q1="I feel interested"
q2= "I feel distressed"
q3= "I feel excited"
q4= "I feel upset"
q5="I feel strong"
q6="I feel guilty"
q7="I feel scared"
q8="I feel hostile"
q9="I feel enthusiastic"
q10="I feel proud"
q11="I feel irritable"
q12="I feel alert"
q13="I feel ashamed"
q14="I feel inspired"
q15="I feel nervous"
q16="I feel determined"
q17="I feel attentive"
q18="I feel jittery"
q19="I feel active"
q20="I feel afraid"
#create question library
qlibrary = {1:q1, 2:q2, 3:q3, 4:q4, 5:q5, 6:q6, 7:q7, 8:q8, 9:q9, 10:q10, 11:q11, 12:q12, 13:q13, 14:q14, 15:q15, 16:q16, 17:q17, 18:q18, 19:q19, 20:q20} 
questions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] #list of qs

piktures = 58 #numbers of pictures in folder
pix = list(range(0, piktures))
shuffle(pix) #randomized order of pictures

def survey_intro():
    shuffle(questions) #randomize order of questions
    event.clearEvents()
    instr1.draw()
    win.flip()
    if 'escape' in event.waitKeys():
        core.quit()
    for i in questions:
        myRatingScale = visual.RatingScale(win, choices=['      1:\nvery slightly/\nnot at all', '    2:\na little', '       3:\nmoderately', '        4:\nquite a bit', '      5:\nextremely'], stretch=2.4, textColor='Black', lineColor='Black', showValue=False, acceptText='continue')
        myItem = visual.TextStim(win, text=qlibrary[i], height=.12, units='norm', color="#000000")
        event.clearEvents()
        while myRatingScale.noResponse:  # show & update until a response has been made
            myItem.draw()
            myRatingScale.draw()
            win.flip()
            if event.getKeys(['escape']):
                core.quit()
        response = myRatingScale.getRating()
        logging.log(level=logging.DATA, msg="Question Number: %i , Response: %s" % (i, response))

# show the stimulus images
def show_images():
    event.clearEvents()
    instr2.draw()
    instrKey.setText("PRESS 2 [pointer finger] to continue")
    instrKey.draw()
    win.flip()
    event.waitKeys(keyList=['2'])
    imagestart.draw()
    win.flip()
    core.wait(9)
    event.clearEvents()
    for k in pix:    # need to resize images HERE
        pic = visual.ImageStim(win, image='showpics/%i.png' % (k+1))
        print(k+1)
        pic.size*=(0.5, 0.5)
        pic.draw()
        pic.draw()
        win.flip()
        core.wait(1) #set how long images stay
    win.flip()

def survey_outro():
    shuffle(questions) #randomize order of questions
    event.clearEvents()
    instr3.draw()
    win.flip()
    if 'escape' in event.waitKeys():
        core.quit()
    for i in questions:
        myRatingScale = visual.RatingScale(win, choices=['      1:\nvery slightly/\nnot at all', '    2:\na little', '       3:\nmoderately', '        4:\nquite a bit', '      5:\nextremely'], stretch=2.4, textColor='Black', lineColor='Black', showValue=False, acceptText='continue')
        myItem = visual.TextStim(win, text=qlibrary[i], height=.12, units='norm', color="#000000")
        event.clearEvents()
        while myRatingScale.noResponse:  # show & update until a response has been made
            myItem.draw()
            myRatingScale.draw()
            win.flip()
            if event.getKeys(['escape']):
                core.quit()
        response = myRatingScale.getRating()
        logging.log(level=logging.DATA, msg="Question Number: %i , Response: %s" % (i, response))

def show_instructions():
    title.setAutoDraw(True)
    instrText.setText(instructions1)
    instrText.setAutoDraw(True)
    win.flip()
    #core.wait(20)
    instrKey.setText("PRESS 2 [pointer finger] to continue")
    instrKey.draw()
    win.flip()
    event.waitKeys(keyList=['2'])
    instrText.setText(instructions2)
    win.flip()
    #core.wait(20)
    instrKey.setText("PRESS 3 [middle finger] to begin...")
    instrKey.draw()
    win.flip()
    event.waitKeys(keyList=['3'])
    instrText.setAutoDraw(False)
    
    p1_ticker="."
    p3_ticker="."
    p1_ticker_end=45 #time to load players: make longer for more realistic interactive game
    p3_ticker_end=125
    
    title.setText('Joining VBT Game Room')
    instr_p1.setText("PLAYER 1: Wating for player to join") #loading screen
    instr_p2.setText("PLAYER 2: Welcome %s" % player_name)
    instr_p3.setText("PLAYER 3: Wating for player to join")
    instr_p1.setAutoDraw(True)
    instr_p2.setAutoDraw(True)
    instr_p3.setAutoDraw(True)
    p1_tick.setAutoDraw(True)
    p3_tick.setAutoDraw(True)
    win.flip()
    for tick in range(400):
        if tick == p1_ticker_end:
            instr_p1.setText("PLAYER 1: Welcome %s" % player1_name)
            p1_tick.setAutoDraw(False)
        elif tick == p3_ticker_end:
            instr_p3.setText("PLAYER 3: Welcome %s" % player3_name)
            p3_tick.setAutoDraw(False)
        else:
            if tick % 10 == 0:
                p1_ticker = p1_ticker + "."
                if len(p1_ticker)>6:
                    p1_ticker=""
            if tick % 12 == 0:
                p3_ticker = p3_ticker + "."
                if len(p3_ticker)>6:
                    p3_ticker=""
            if tick < p1_ticker_end:
                p1_tick.setText(p1_ticker)
            if tick < p3_ticker_end:
                p3_tick.setText(p3_ticker)
        win.flip()
    core.wait(2)
    
    title.setAutoDraw(False)
    instr_p1.setAutoDraw(False)
    instr_p2.setAutoDraw(False)
    instr_p3.setAutoDraw(False)

def player_names(state=True):
    p1name.setAutoDraw(state)
    p2name.setAutoDraw(state)
    p3name.setAutoDraw(state)

def throw_ball(fromP, toP): #log the throw and add counters to roundcount and trialcount
    global trialCnt, holder, rndCnt
    key = "%ito%i" % (fromP,toP)
    
    logging.log(level=logging.DATA, msg="round %i - trial %i - throw: %s - %s" % (round, trialCnt, key, condition))
    
    logging.log(level=logging.DATA, msg="throw variable: %s" % (throw))
    logging.log(level=logging.DATA, msg="key variable: %s" % (key))
    
    sorted_images = []
    for next_image in throw[key]:
        sorted_images.append(next_image)
    sorted_images.sort()
    
    for s in sorted_images:
        logging.log(level=logging.DATA, msg="current s variable: %s" % (s))
        players.setImage('images/%s/%s' % (key,s))
        players.draw()
        win.flip()
        core.wait(0.15)
    
    # update trial and round counters
    trialCnt+=1
    rndCnt+=1
    
    # set the new holder to be the person to whom it was thrown
    holder=toP # not the issue with images
    logging.flush()
    select_throw()

# allow the participant to throw the ball
def select_throw(): #runs if subject has ball
    global condition
    if holder==2: #if subject has ball
        
        # update logs to reflect participant ownership
        logging.log(level=logging.DATA,msg="PLAYER HAS BALL")
        got_ball_time = trialClock.getTime()
        
        choice=[]
        while len(choice)==0 or choice [0] not in ('2','3'): #waiting for subject to make choice
            core.wait(0.01)
            if trialCnt > maxTrials or trialClock.getTime() > maxTime: #end round if player takes too long/ there have been too many tosses
                return
            choice = event.getKeys(keyList=['2','3'])
        if choice[0]=='2':
            throwTo=1
        elif choice[0]=='3':
            throwTo=3
            
        logging.log(level=logging.DATA,msg="PLAYER THROWS TO %i - RT %0.4f" % (throwTo, trialClock.getTime()-got_ball_time))
    else:
        core.wait(random.randint(500,2000)/1000) #range for simulation to "decide" where to throw
    
        if round>incRounds and rndCnt>7: #start excluding player after 7 throws in exclusion round
            condition="UBALL"
            ft=0.3
        else:
            ft=0.0
        
        throwChoice = random.random() - ft #change equation so subject is less likely to recieve ball
        if throwChoice < 0.5:
            if holder==1:
                throwTo=3
            else:
                throwTo=1
        else:
            throwTo=2
    
    if trialCnt > maxTrials or trialClock.getTime() > maxTime:
        logging.log(level=logging.DATA,msg="RETURN with %i Trial Count and %i Trial Clock" % (trialCnt, trialClock.getTime()))
        return
    else:
        throw_ball(holder,throwTo)

# start 

def play_round():
    global rndCnt
    rndCnt=0
    logging.log(level=logging.DATA, msg="Displaying Round %i label" % round)
    round_fix.setText("Round %i" % round)
    round_fix.draw()
    win.flip()
    core.wait(2)
    logging.log(level=logging.DATA, msg="Starting Round %i" % round)
    trialClock.reset()
    players.draw()
    player_names(True)
    title.setText('Press "2" to throw to your left           Press "3" to throw to your right')
    title.setAutoDraw(True)
    win.flip()
    core.wait(0.2)
    select_throw()
    player_names(False)
    title.setText("")
    fixation.draw()
    win.flip()
    core.wait(5)


# ================================
# setup logging #
# ================================
log_file = logging.LogFile("logs/%s.log" % (subj_id),  level=logging.DATA, filemode="w")
logging.log(level=logging.DATA, msg="START")

logging.log(level=logging.DATA, msg="Intro Survey")
#survey_intro() #commented out for pupil testing
#show_instructions() #commented out for pupil testing
ready_screen.setText("Press Space to start")
ready_screen.draw()
win.flip()
event.waitKeys(keyList=['space'])

#################
# Trigger scanner #
#################
globalClock = core.Clock()
trialClock = core.Clock()
logging.setDefaultClock(globalClock)

# ADD TRIGGER CODE - 255 on serial port - if scanner is expecting to receive a 'start' trigger
# from task
# some scanners may send a trigger code (i.e. a '5' or a 't') on each TR 
# in which case code here should be adapted (or above where task waits for a space bar to start)
try:
    ser = serial.Serial('/dev/tty.KeySerial1', 9600, timeout=1)
    ser.write('0')
    time.sleep(0.1)
    ser.write('255')
    ser.close()
except:
    #print ("SCANNER NOT TRIGGERED")
    pass
# end of trigger code

# 8 sec disdaq
title.setText('')
fixation.setText("Please wait...")
fixation.draw()
win.flip()
core.wait(2)

while round<=incRounds:
    play_round()
    holder=1
    trialCnt=0
    round+=1
while (round-incRounds)<=exRounds:
    play_round()
    holder=1
    trialCnt=0
    round+=1

show_images() #show images
#survey_outro() #show survey again #commented out for pupil testing
goodbye.setText("You have completed this research study, congratulations!\nThank you for your participation. Please wait for the experimenter to come over and remove the eyetrackers")
goodbye.draw()
win.flip()
core.wait(7.5)
logging.log(level=logging.DATA, msg="END")
