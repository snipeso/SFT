# SFT

import logging
import os
import random
import time
import datetime
import sys
import math

from screen import Screen
from scorer import Scorer
from trigger import Trigger
from recorder import Recorder
from psychopy import core, event, sound
from psychopy.hardware import keyboard

from datalog import Datalog
from config.configSFT import CONF

from stimuli.sentences import sentences

#########################################################################

######################################
# Initialize screen, logger and inputs

logging.basicConfig(
    level=CONF["loggingLevel"],
    format='%(asctime)s-%(levelname)s-%(message)s',
)  # This is a log for debugging the script, and prints messages to the terminal

screen = Screen(CONF)

datalog = Datalog(OUTPUT_FOLDER=os.path.join(
    'output', datetime.datetime.now(
    ).strftime("%Y-%m-%d")), CONF=CONF)  # This is for saving data

kb = keyboard.Keyboard()

mainClock = core.MonotonicClock()  # starts clock for timestamping events

Alarm = sound.Sound(os.path.join('sounds', CONF["sounds"]["alarm"]),
                    stereo=True)
scorer = Scorer()

trigger = Trigger(CONF["trigger"]["serial_device"],
                  CONF["sendTriggers"], CONF["trigger"]["labels"])

logging.info('Initialization completed')

sentences = sentences[CONF["task"]["language"]]

# recorder = Recorder(CONF)


#########################################################################


def quitExperimentIf(shouldQuit):
    "Quit experiment if condition is met"

    if shouldQuit:
        trigger.send("Quit")
        scorer.getScore()
        logging.info('quit experiment')
        sys.exit(2)


def onFlip(stimName, logName):
    "send trigger on flip, set keyboard clock, and save timepoint"
    trigger.send(stimName)
    kb.clock.reset()  # this starts the keyboard clock as soon as stimulus appears
    datalog[logName] = mainClock.getTime()


##############
# Introduction
##############

screen.show_blank()

# # Display overview of session
# screen.show_overview()
# core.wait(CONF["timing"]["overview"])

# # Optionally, display instructions
# print(CONF["showInstructions"], CONF["version"])
# if CONF["showInstructions"]:
#     screen.show_instructions()
#     key = event.waitKeys()
#     quitExperimentIf(key[0] == 'q')

# # Blank screen for initial rest
# screen.show_blank()
# logging.info('Starting blank period')

# trigger.send("StartBlank")
# core.wait(CONF["timing"]["rest"])
# trigger.send("EndBlank")

# # Cue start of the experiment
# screen.show_cue("START")
# trigger.send("Start")
# core.wait(CONF["timing"]["cue"])


#################
# Main experiment
#################

# Loop through sentences

for indx, sentence in enumerate(sentences):

    logging.info("Sentence: %s", sentence)

    # trial trigger
    trigger.sendTriggerId()

    # show sentence
    screen.window.callOnFlip(onFlip, "Stim", "showSentence")
    screen.start_sentence(sentence)

    # wait for start key
    key = []
    while not key:
        key = kb.getKeys(waitRelease=False)
        if key:
            answer = key[0].name
            quitExperimentIf(answer == 'q')
            trigger.send("Response")
        core.wait(.1)

    datalog["sentence"] = sentence
    datalog["readingTime"] = key[0].rt

    # start recording for 10 seconds
    # datalog["filename"] = recorder.set_filename(indx)
    # recorder.play()

    trigger.send("StartRecording")
    trialTimer = core.CountdownTimer(CONF["task"]["duration"])
    now = 1
    while now > 0:
        now = trialTimer.getTime()
        percent = now / CONF["task"]["duration"]
        screen.shrink_time(percent)
        key = kb.getKeys(waitRelease=False)
        if key:
            answer = key[0].name
            quitExperimentIf(answer == 'q')

    trigger.send("EndTime")

    # show blank
    screen.show_blank()

    delayTimer = core.CountdownTimer(CONF["pause"]["duration"])

    while delayTimer.getTime() > 0:
        key = kb.getKeys(waitRelease=False)
        if key:
            answer = key[0].name
            quitExperimentIf(answer == 'q')


# End main experiment
screen.show_cue("DONE!")
trigger.send("End")
core.wait(CONF["timing"]["cue"])

# Blank screen for final rest
screen.show_blank()
logging.info('Starting blank period')

trigger.send("StartBlank")
core.wait(CONF["timing"]["rest"])
trigger.send("EndBlank")


logging.info('Finished')
scorer.getScore()
trigger.reset()
