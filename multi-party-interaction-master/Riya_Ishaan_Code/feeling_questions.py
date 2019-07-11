from naoqi import ALProxy
import random
from collections import defaultdict
import time
import almath
import os
import math
import csv
import sys
import json
import datetime
import keyboard
from multiprocessing.dummy import Pool

sys.path.append("..")

import config


IP = config.ROBOT_IP
PORT = config.ROBOT_PORT

def main():
    global tts = ALProxy("ALTextToSpeech", IP, 9559)

    while not keyboard.is_pressed('q'):
        try:
            if keyboard.is_pressed('w'):
                tts.say("What are you feeling?")
            elif keyboard.is_pressed('a'):
                tts.say("Why do you feel that way?")
            elif keyboard.is_pressed('s'):
                tts.say("What would you change to improve how you feel?")
            elif keyboard.is_pressed('d'):
                tts.say("What can you control in the situation to improve how you feel?")
            elif keyboard.is_pressed('f'):
                tts.say("How do you think the other person is feeling")
            else:
                pass
        except:
            break