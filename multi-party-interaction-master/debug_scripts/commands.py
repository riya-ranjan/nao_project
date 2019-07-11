from naoqi import ALProxy
from random import randint
import time
import almath
import argparse
import os
import sys

IP = "192.168.7.114"
PORT = 9559
P_1 = "Participant 1"
P_2 = "Participant 2"
P_3 = "Participant 3"
P_4 = "Participant 4"
P_5 = "Participant 5"
P_6 = "Participant 6"
JOINT_RANGE = {}
TAG_LIST = []
BEHAVIOR_LIST = []
text_to_speech = ALProxy("ALTextToSpeech", IP, PORT)
m = ALProxy("ALMotion",IP,PORT)

#consider mood and tone as a simple variable
#data variables (use to manage global reference points)
def populate_behaviors():
    bt = ALProxy("ALBehaviorManager", IP, PORT)
    TAG_LIST= bt.getTagList()
    BEHAVIOR_LIST = bt.getLoadedBehaviors()
def populate_joint_range(file):
    f = open(file,'r')
    count = -1
    cache = ""
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
    print(JOINT_RANGE)
def deg_to_name(p):
    if (p == P_1):
        return -35;
    elif (p == P_2):
        return -15
    elif (p == P_3):
        return 0
    elif (p == P_4):
        return 15
    elif (p == P_5):
        return 35
    else:
        return 0
#DECOMPOSITION FUNCTIONS
def simple_mvt(names, pct, fractionMaxSpeed = 0.3, sync = True):
    #sample input ("HeadYaw", 45%) --> turn 45 % movement positive
    #sample input 2 ("HeadYaw", -45%) --> turn 45 % movement negative
    m = ALProxy("ALMotion", IP, PORT)
    m.setStiffnesses("Body",1.0)
    if (pct > 100 or pct < -100):
        print("Invalid input range. Please input between 1 and 100")
        return False
    if names in JOINT_RANGE:
        angles = 0
        if pct > 0:
            angles = (pct*0.01)*JOINT_RANGE[names][1]
        else:
            angles = (pct*-0.01)*JOINT_RANGE[names][0]
        angles = angles*almath.TO_RAD
        if (sync):
            m.post.setAngles(names,angles,fractionMaxSpeed)
        else:
            m.setAngles(names,angles,fractionMaxSpeed)
        return True
    else:
        print(names, "is not a valid part movement. Please try again!")
        return False
def default_sit():
    do_behavior('animations/Sit/BodyTalk/Speaking/BodyTalk_7',3.0)

def return_def ():
    #use this function after a function is called
    m = ALProxy("ALMotion",IP,PORT)
    m.setStiffnesses("Head",1.0)
    #code of movment starts here
    print("Left elbow up")
    m.setStiffnesses("LArm",1.0)
    m.setStiffnesses("RArm",1.0)
    look("none")
    #Left elbow movement basic motion
    names = ["LElbowRoll","LShoulderPitch", "LShoulderRoll", "LHipYawPitch"]
    angles = [-20*almath.TO_RAD, 80 * almath.TO_RAD, 0 * almath.TO_RAD , 0 * almath.TO_RAD]
    fractionMaxSpeed = 0.3
    m.setAngles(names,angles,fractionMaxSpeed)
    names = ["RElbowRoll","RShoulderPitch", "RShoulderRoll"]
    angles = [-20*almath.TO_RAD, 80 * almath.TO_RAD, 0 * almath.TO_RAD]
    fractionMaxSpeed = 0.3
    m.setAngles(names,angles,fractionMaxSpeed)
    time.sleep(2.0)
    simple_mvt("HeadYaw",0)
    time.sleep(0.0)
    m.setStiffnesses("LArm",0.0)
    m.setStiffnesses("RArm",0.0)
    m.setStiffnesses("Body",0.0)
def playFile(f):
    aup = ALProxy("ALAudioPlayer", IP, PORT)
    aup.playFile("/home/nao/audio/" + f)
    #aup.playFile(file_id)
def look (participant):
    m = ALProxy("ALMotion", IP, PORT)
    text_to_speech = ALProxy("ALTextToSpeech", IP, PORT)
    m.setStiffnesses("Head",1.0)
    #Left elbow movement basic motion
    names = "HeadYaw"
    angles = deg_to_name(participant)*almath.TO_RAD
    fractionMaxSpeed = 0.1
    #say(participant+ " turning to " +  str(deg_to_name(participant)))
    m.setAngles(names,angles,fractionMaxSpeed)
    time.sleep(1.5)
    if (participant != "none"):
        print(participant)
    m.setStiffnesses("Head",0.0)
def say (speech):
    text_to_speech = ALProxy("ALTextToSpeech", IP, PORT)
    #text_to_speech.post.say("\\vol=55\\" + speech)
    print(speech)

def do_behavior(behavior, wait_time= -1.0, sync = True):
    bh = ALProxy("ALBehaviorManager", IP, PORT)
    m = ALProxy("ALMotion",IP,PORT)
    m.setStiffnesses("Body", 1)
    print(BEHAVIOR_LIST)
    success = False
    if (sync):
        if (bh.post.startBehavior(behavior)):
            success = True
    else:
        if (bh.startBehavior(behavior)):
            success = True
    if (success):
        print(behavior, ": behavior started")
        if ((wait_time != -1.0) and (wait_time > 0)):
            #if wait time is specified
            time.sleep(wait_time)
            bh.stopBehavior(behavior)
            print(behavior, ": behavior killed")
    else:
        print("Behavior failed to executes")
def kill_behavior(behavior):
    #not sure if this wll be used; may delete later
    bh = ALProxy("ALBehaviorManager", IP, PORT)
    if(bh.stopBehavior(behavior)):
        print(behavior,": behavior killed")
    else:
        print(behavior, ": behavior issue")
#Specific movements used for commands (more specific than behavior)
def wave ():
    m = ALProxy("ALMotion", IP, PORT)
    #shoulder up and elbow up
    m.setStiffnesses("RArm", 1.0)
    names = ["RShoulderPitch","RShoulderRoll", "RElbowRoll", "RWristYaw", "RElbowYaw"]
    angles = [-30 * almath.TO_RAD,-50 * almath.TO_RAD, -50 * almath.TO_RAD, 0 * almath.TO_RAD, 50 * almath.TO_RAD]
    fractionMaxSpeed = 0.5
    m.post.setAngles(names, angles, fractionMaxSpeed)
    m.post.openHand("RHand")
    time.sleep(0.5)
    names=["RElbowRoll","RShoulderPitch"]
    for i in range(0,3):
        print (names," turn by ", (((-1) ** i) *100))
        angles = [((-1) ** i) *100* almath.TO_RAD,((-1) ** i) *10* almath.TO_RAD]
        fractionMaxSpeed = 0.5
        m.post.setAngles(names, angles, fractionMaxSpeed)
        time.sleep(0.5)
    #time.sleep(4.0)
    print("Done")
    m.setStiffnesses("RArm", 0.0)
    m.post.closeHand("RHand");
    print("wave function finished")
def lean_forward():
    m = ALProxy("ALMotion",IP,PORT)
    simple_mvt("RElbowRoll",-30)
    simple_mvt("LElbowRoll"-30)
    time.sleep(2.0)
    simple_mvt("RShoulderRoll", -50)
    simple_mvt("LShoulderRoll", -50)
    m.setStiffnesses("LLeg",1)
    m.setStiffnesses("Head",1)
    names = ["LHipYawPitch", "HeadPitch"]
    angles= [-40 * almath.TO_RAD, -10 * almath.TO_RAD]
    fractionMaxSpeed = 0.1
    print("leaning forward")
    m.post.setAngles(names,angles,fractionMaxSpeed)
    time.sleep(3.5)
    print("finished lean")

    m.setStiffnesses("LLeg",0)
#Commands
def command_hello (participant):
    look (participant)
    text_to_speech.post.say("\\vol=55\\Hi how are you?")
    wave()
    #return_def()
def command_how_feeling (participant):
    look(participant)
    text_to_speech.post.say("\\vol=55\\How does that make you feel?")
    time.sleep(1.0)
    do_behavior('animations/Sit/BodyTalk/Listening/Listening_' + str(randint(1,4)),5.0)
    #lean_forward()
    #simple_mvt("LHipYawPitch",5)
    consider()
    #return_def()
def consider():
    #make sure to load these behaviors on later!
    print("Think behaviors not installed")
    #do_behavior('animations/Sit/BodyTalk/Listening/Think_' + str(randint(1,3)),3.0)
def command_thank_sharing(participant):
    look(participant)
    #text_to_speech.post.say("Thank you for sharing!")
    do_behavior('animations/Sit/BodyTalk/Speaking/BodyTalk_'+str((randint(8,11))),3.0)
    default_sit()
def main():
    #populate global variables
    populate_joint_range("debug_scripts/nao_mvt_data/ranges.txt")
    populate_behaviors()
    #return to default state
    #m.setStiffnesses("RArm",0.0)
    #m.setStiffnesses("Body",0.0)
    #return_def()
    #run functions
    playFile("hello.mp3")
    default_sit()
if __name__ == "__main__":
    main()