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
import keyboard
import config
import datetime
from multiprocessing.dummy import Pool
'''
@author: Riya Ranjan
@date: 7/11/19
@desc: All questions/method calls pertaining to questions asked about bullying for the middle school students will be stored/coded here
'''
IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
tts = ALProxy("ALTextToSpeech", IP, PORT)

def main():
    question_arr = ["Why did you act that way towards them?", "What was your goal in this conflict?", "Do you understand why your actions make them feel this way?", "How can you relate to how they feel", "What actions can you take to constructively resolve this conflict?", "What have you learned from this conversation?"]
    
    while(True):
        num = input("Enter number from 1-6")
        tts.say(question_arr[num-1])
        time.sleep(0.1)

if __name__=="__main__":
    main()