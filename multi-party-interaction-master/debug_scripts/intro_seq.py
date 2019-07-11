from naoqi import ALProxy
from random import randint
import random
from collections import defaultdict
import time
import almath
import argparse
import os
import math
import sys
import json
from master_control import *

#made sense to put intro_seq in its own file because it will be most hard-coded
 #integrating it deeply with master_control would overcomplicate tings

#TO-DO: Questions by sensitivity motion

IP = "192.168.7.241"
PORT = 9559
JOINT_RANGE = {}
TAG_LIST = []
BEHAVIOR_LIST = []
MAIN_MOTION = json.dumps({})
SUB_MOTION = json.dumps({})
P_1 = "Participant 1"
P_2 = "Participant 2"
P_3 = "Participant 3"
P_4 = "Participant 4"
P_5 = "Participant 5"
P_6 = "Participant 6"

#classify commands
SUPPORTED_COMMANDS = ["Individual Clarification", "Question Low","Question Medium", "Question High",
"Feelings", "Thoughts", "Experiences", "Practical", "Humor", "Agreement", "Disagreement",
"Acknowledgement", "Warning"]
FILE_BANK = ["advice.txt","disclosures.txt","questions.txt","responses.txt"]
COMMAND_MAP = defaultdict(list)

#just for ease
text_to_speech = ALProxy("ALTextToSpeech", IP, PORT)
#m = ALProxy("ALMotion",IP,PORT)
b = ALProxy("ALBehaviorManager",IP,PORT)



def pop_source():
    #called in main
    populate_joint_range("nao_mvt_data/ranges.txt")
    populate_command_map()
    pop_motions()
    populate_behaviors()
def populate_behaviors():
    bt = ALProxy("ALBehaviorManager", IP, PORT)
    global TAG_LIST
    global BEHAVIOR_LIST
    TAG_LIST= bt.getTagList()
    BEHAVIOR_LIST = bt.getLoadedBehaviors()
def pop_motions():
    with open ('main_motion.json') as data_file:
        data = json.load(data_file)
        #print("General Print: ", data)
        global MAIN_MOTION
        MAIN_MOTION = data
    with open ('sub_motion.json') as data_file:
        global SUB_MOTION
        data = json.load(data_file)
        SUB_MOTION = data
def populate_joint_range(file):
    f = open(file,'r')
    count = -1
    cache = ""
    global JOINT_RANGE
    for line in f:
        #print(line)
        line = line.strip('\n')
        if (count == -1):
            cache = line
            JOINT_RANGE[line] = []
        elif count <= 1:
            JOINT_RANGE[cache].append(float(line))
        count = count + 1
        if (count > 1):
            count = -1
def populate_command_map():
    global FILE_BANK
    global COMMAND_MAP
    for f in FILE_BANK:
        f = "../speech/" + f;
        with open (f) as file:
            content = file.readlines()
            content = [x.strip() for x in content]
            file_to_command_map(content)
def file_to_command_map(content):
    global COMMAND_MAP
    #clean check
    for lines in content:
        firstword = lines.split(' ', 1)[0]
        if not (firstword == "*KEY*"):
            normal_command(lines)
def normal_command(line):
    global COMMAND_MAP
    done = False
    second = False
    classify = ""
    speech = ""
    for word in line.split():
        if (second):
            classify = classify + " " + word
        elif (word == "|"):
            second = True
        else:
            speech = speech + " " + word
    #once line is finished parsing
    #remove initial space
    classify = classify[1:]
    speech = speech[1:]

    COMMAND_MAP[classify].append(speech)

def main():
    pop_source()
    default_sit()
    say("Hello everyone")
    exec_keyframe(P_3, 5.0, "m_intro","Hello everyone!")
    say("Thank you for joining me here today. As you know, we are here today to talk about the stress we are feeling with school. It is my hope that we can each share our experiences and feelings of stress at school with each other. By sharing these feelings and experiences with each other we can grow and overcome them!")
    exec_keyframe(P_3, 5.0, "Excited Start","")
    exec_keyframe(P_3,7.5,"Question Medium", "In order for this to work, we are going to take turns sharing with each other. You can ask follow up questions and respond to each other, but please don't interrupt or talk over one another or I won't be able to understand.")
    say("Does that sound good?")
    exec_keyframe(P_3,5.0, "m_agree", "")
    exec_keyframe(P_3,5.0,"Question Medium", "To start, could you each introduce yourselves? Please share your name, major, and one interesting fact about yourself.")
    exec_keyframe(P_3,5.0,"Question Low","Now, let's start by talking about success. What does success look like for each of you?")
if __name__ == "__main__":
    main()