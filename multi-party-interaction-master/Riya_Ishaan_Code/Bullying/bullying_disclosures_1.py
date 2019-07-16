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
    disclosure_arr = ["Sometimes I say things during an argument that I later regret. Do any of you feel the same way?"]
    
    while(True):
        num = input("Click 1 to see nao's comment")
        tts.say(disclosure_arr[num-1])
        time.sleep(0.1)

if __name__=="__main__":
    main()