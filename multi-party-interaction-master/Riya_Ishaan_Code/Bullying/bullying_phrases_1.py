from naoqi import ALProxy
import random
from collections import defaultdict
import time
import almath
import os
import math
import csv
import sys, termios, tty
import json
import keyboard
import config
import datetime
from multiprocessing.dummy import Pool
'''
@author: Riya Ranjan
@date: 7/11/19
@desc: The phrases that are used to mediate conversation about bullying are stored here.
'''
IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
tts = ALProxy("ALTextToSpeech", IP, PORT)

def main():
    question_arr = ["Let's discuss just one issue at a time.", "Try not to place blame. Discuss your personal feelings first.", "Let's pause for a moment."]
    
    while(True):
        num = input("Enter number from 1-3")
        tts.say(question_arr[num-1])
        time.sleep(0.1)

if __name__=="__main__":
    main()