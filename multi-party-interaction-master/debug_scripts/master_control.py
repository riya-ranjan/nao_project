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
from multiprocessing.dummy import Pool

sys.path.append("..")

import config

interrupt = 0
inprogress = 0


# TODO: Questions by sensitivity motion
# IP = "192.168.7.127"
# PORT = 9559
IP = config.ROBOT_IP
PORT = config.ROBOT_PORT

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

# classify commands
SUPPORTED_COMMANDS = ["Clarification", "Question Low", "Question Medium", "Question High",
                      "Feelings", "Thoughts", "Experiences", "Practical", "Humor", "Agreement", "Disagreement",
                      "Acknowledgement", "Warning", "Follow-Up", "Disclosure Low", "Disclosure Medium", "Disclosure High"]
FILE_BANK = ["advice.txt", "disclosures.txt", "questions.txt", "responses.txt"]
COMMAND_MAP = defaultdict(list)

# just for ease
text_to_speech = ALProxy("ALTextToSpeech", IP, PORT)
m = ALProxy("ALMotion", IP, PORT)
b = ALProxy("ALBehaviorManager", IP, PORT)
muted = False
pool = Pool(10)
id = 0

# consider mood and tone as a simple variable

# data variables (use to manage global reference points)
def pop_source(dir_name="nao_mvt_data"):
    # called in main
    populate_joint_range(os.path.join(dir_name, "ranges.txt"))
    populate_command_map(dir_name)
    pop_motions(dir_name)
    populate_behaviors()


def populate_behaviors():
    bt = ALProxy("ALBehaviorManager", IP, PORT)
    global TAG_LIST
    global BEHAVIOR_LIST
    TAG_LIST = bt.getTagList()
    BEHAVIOR_LIST = bt.getLoadedBehaviors()


def populate_joint_range(file):
    f = open(file, 'r')
    count = -1
    cache = ""
    global JOINT_RANGE
    for line in f:
        # print(line)
        line = line.strip('\n')
        if (count == -1):
            cache = line
            JOINT_RANGE[line] = []
        elif count <= 1:
            JOINT_RANGE[cache].append(float(line))
        count = count + 1
        if (count > 1):
            count = -1


def populate_command_map(dir_name):
    global FILE_BANK
    global COMMAND_MAP
    for f in FILE_BANK:
        # f = "../speech/" + f
        f = os.path.abspath(os.path.join(dir_name, "../..", "speech", f))
        with open(f) as file:
            content = file.readlines()
            content = [x.strip() for x in content]
            file_to_command_map(content)


def file_to_command_map(content):
    global COMMAND_MAP
    # clean check
    for lines in content:
        firstword = lines.split(' ', 1)[0]
        if not (firstword == "*KEY*"):
            normal_command(lines)


#logging
def log_speech(speech,motion,time,participant):
    global id
    rowsyntax = ["id","speech","motion","participant","duration","timestamp"]
    #every new speech should be it's own id
    id = id + 1
    currDT = datetime.datetime.now()
    print("LOGGING SPEECH: ", id, " says ", motion, " with motion ", motion, " at ", str(currDT))
    newRow = [id,speech,motion,participant,time,str(currDT)]
    with open('outputDir/motion_log.csv','a') as fd:
        writer = csv.writer(fd)
        if (id==1):
            writer.writerow(rowsyntax)
        writer.writerow(newRow)

def log_mvt(submotion_name, time):
    global id
    rowsyntax = ["id","submotion","duration","timestamp"]
    #now real interaction
    currDT = datetime.datetime.now()
    print("LOGGING MOVEMENT: ",id, " with motion ", submotion_name, " for ", time, " at ", str(currDT))
    newRow = [id,submotion_name,time,str(currDT)]
    with open('outputDir/mvt_log.csv','a') as fd:
        writer = csv.writer(fd)
        if (id==1):
            writer.writerow(rowsyntax)
        writer.writerow(newRow)
#control
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
    # once line is finished parsing
    # remove initial space
    classify = classify[1:]
    speech = speech[1:]

    COMMAND_MAP[classify.lower()].append(speech)

def split_sent(s):
     words = []
     inword = 0
     for c in s:
         if c in " \r\n\t": # whitespace
             inword = 0
         elif not inword:
             words = words + [c]
             inword = 1
         else:
             words[-1] = words[-1] + c
     return words

def simple_mvt(names, pct, fraction_max_speed=0.3, sync=True, motion_proxy=None):
    motion_proxy = m
    global JOINT_RANGE
    # sample input ("HeadYaw", 45%) --> turn 45 % movement positive
    # sample input 2 ("HeadYaw", -45%) --> turn 45 % movement negative
    angles = []
    motion_proxy.setStiffnesses("Body", 1.0)
    count = -1
    for p in pct:
        count = count + 1
        if p > 100 or p < -100:
            print("Invalid input range. Please input between 1 and 100")
            return False

        if names[count] in JOINT_RANGE:
            if p > 0:
                angles.append(math.radians((p * 0.01) * JOINT_RANGE[names[count]][1]))
            else:
                angles.append(math.radians((p * -0.01) * JOINT_RANGE[names[count]][0]))
    print(angles)
    print(names)
    # angles = angles*almath.TO_RAD
    if sync:
        motion_proxy.post.setAngles(names, angles, fraction_max_speed)
    else:
        motion_proxy.setAngles(names, angles, fraction_max_speed)
    return True


def deg_to_name(p):
    if (p == P_1):
        return -45
    elif (p == P_2):
        return -15
    elif (p == P_3):
        return 0
    elif (p == P_4):
        return 15
    elif (p == P_5):
        return 45
    else:
        return 0


def pop_motions(dir_name):
    global MAIN_MOTION
    global SUB_MOTION

    with open(os.path.abspath(os.path.join(dir_name, "..", 'main_motion.json'))) as data_file:
        data = json.load(data_file)
        # print("General Print: ", data)
        MAIN_MOTION = data
    with open(os.path.abspath(os.path.join(dir_name, "..", 'sub_motion.json'))) as data_file:
        data = json.load(data_file)
        SUB_MOTION = data


# Abstract calls:
def playFile(f):
    aup = ALProxy("ALAudioPlayer", IP, PORT)
    aup.playFile("/home/nao/audio/" + f)
    # aup.playFile(file_id)


def look(participant):
    m.setStiffnesses("Head", 1.0)
    # Left elbow movement basic motion
    print("Look at " + participant)
    names = "HeadYaw"
    if (participant == "group"):
        print("Looking at whole group")
        exec_keyframe("None", 2.0, "look_around", "")
    else:
        angles = deg_to_name(participant) * almath.TO_RAD
        fractionMaxSpeed = 0.1
        # say(participant+ " turning to " +  str(deg_to_name(participant)))
        m.setAngles(names, angles, fractionMaxSpeed)
        time.sleep(1.5)
        if (participant != "none"):
            print(participant)
        # m.setStiffnesses("Head",0.0)


def say(speech):
    text_to_speech = ALProxy("ALTextToSpeech", IP, PORT)
    text_to_speech.say("\\vct=80\\"+speech)
    print(speech)


def do_behavior(behavior, wait_time=-1.0, sync=True):
    bh = ALProxy("ALBehaviorManager", IP, PORT)
    m = ALProxy("ALMotion", IP, PORT)
    m.setStiffnesses("Body", 1)
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
            # if wait time is specified
            time.sleep(wait_time)
            bh.stopBehavior(behavior)
            print(behavior, ": behavior killed")
    else:
        print("Behavior failed to executes")


def kill_behavior(behavior):
    # not sure if this wll be used; may delete later
    bh = ALProxy("ALBehaviorManager", IP, PORT)
    if (bh.stopBehavior(behavior)):
        print(behavior, ": behavior killed")
    else:
        print(behavior, ": behavior issue")


def default_sit( t=2.5):
    simple_mvt(["LShoulderPitch", "RShoulderPitch"], [50, 50], 0.3, False)
    time.sleep(t*(1/2.5))
    simple_mvt(["HeadPitch"], [15], 0.8,False)
    do_behavior('animations/Sit/BodyTalk/Speaking/BodyTalk_7', t*(1.5/2.5))

def setInterrupt():
    global interrupt
    interrupt = 1
    return

# keyframe manipulation
def exec_submotion(submotion, t, speed=0.3):
    # get properties from submotion file
    global SUB_MOTION
    sm_detail = SUB_MOTION[submotion]
    print("----NEW SUBMOTION---")
    print("time",t)
    global interrupt
    log_mvt(submotion,t)
    for keyframe in sm_detail:
        if (interrupt):
            print("INTERRUPT")
            return
        names = []
        angles = []
        for values in keyframe["motion"]:
            names.append(values["n"].encode("utf-8"))
            angles.append(values["angle"] * almath.TO_RAD)
            # set motion in action
            global m  # remember m is the motion proxy
            print(names)
            print(angles)
            m.post.setAngles(names, angles, speed)
            time.sleep(t * (keyframe["pct_time"] / 100.0))
            print("----keyframe end---")


def Texec_keyframe(participant, time, motion):
    # aup = ALProxy("ALAudioPlayer", IP, PORT)
    # look(participant)
    # aup.playFile("/home/nao/audio/" + MAIN_MOTION[motion]['sound'])
    global MAIN_MOTION
    for values in MAIN_MOTION[motion]["submotions"]:
        if ("submotion_name" in values):
            print(values["submotion_name"])
            total_time = time * (values["pct_time"] / 100.0)
            exec_submotion(values["submotion_name"], total_time)
        else:
            # this means we are looking at a pre-loaded submotion
            animation_submotion(values, time * (values["pct_time"] / 100))


def animation_submotion(kframe, time):
    anim_options = []
    if "animation_name" in kframe:
        for values in kframe["animation_name"]:
            anim_options.append(json.dumps(values)[1:-1])
    if "tags" in kframe:
        for t in kframe["tags"]:
            anim_options.extend(filter_sit(t))
    if anim_options:
        print(anim_options)
        dec = random.choice(anim_options)
        log_mvt("animation:" + dec, time)
        do_behavior(dec, time)
    else:
        print("no options")


def callback():
    print("async done")


def exec_keyframe(participant, time, motion, speech, is_intro=False):
    # TODO: fix multi-processing
    # p = Process(target=look, args=(participant))
    # p.start()
    look(participant)
    log_speech(speech,motion,time,participant)
    if(muted):
        print("SPEECH MUTED")
    else:
        if (len(speech) <= 10):
            text_to_speech.post.say("\\vct=80\\"+"\\rspd=70\\"+speech)
        else:
            text_to_speech.post.say("\\vct=80\\"+speech)
    global MAIN_MOTION
    global interrupt
    global inprogress
    print("___MOTION STARTED___________")
    print("time: ", time)
    print("speech: ", speech)
    for values in MAIN_MOTION[motion]["submotions"]:
        if (interrupt and not is_intro):
            default_sit(0.5)
            print("INTERRUPT")
            interrupt = 0
            inprogress = 0
            return
        if ("submotion_name" in values):
            total_time = time * (values["pct_time"] / 100.0)
            exec_submotion(values["submotion_name"], total_time)
        else:
            # this means we are looking at a general value
            animation_submotion(values, time * (values["pct_time"] / 100.0))
    print("___MOTION FINISHED____")
    if (interrupt and not is_intro):
        default_sit(0.5)
        print("INTERRUPT")
        interrupt = 0
        inprogress = 0
        return
    if ("Disclosure" in motion):
        #If the message is a disclosure. Add follow-up Question
        call_command("DiscFollow",participant)
    elif(not is_intro):
        default_sit(0.5)
        interrupt = 0
        inprogress = 0


def test():
    global interrupt
    print(interrupt)


# Connect UI to script
def call_command(command, participant="NONE"):
    global COMMAND_MAP
    if command.lower() in COMMAND_MAP:
        speech = random.choice(COMMAND_MAP[command.lower()])
        # find a way to better estimate time
        time = (len(speech) / 15.0) + 1.5
        time = 3.0
        exec_keyframe(participant, time, command, speech, )
        # print (command,speech)
    else:
        print("Unfortunately, this command is not supported")


def tag_fix():
    allTags = b.getTagList()
    validTags = []
    for tag in allTags:
        works = False
        for behavior in b.getBehaviorsByTag(tag):
            if "Sit/" in behavior:
                if not works:
                    works = True
                    validTags.append(tag)
    print(validTags)


def filter_sit(t):
    global b
    # dumb formatting stuff (Comes in the basic JSON format)
    t = json.dumps(t)
    t = t[1:-1]
    print(t)
    allBehaviors = b.getBehaviorsByTag(t)
    goodBehaviors = []
    for bh in allBehaviors:
        if "Sit/" in bh:
            goodBehaviors.append(bh)
    return goodBehaviors


def test_supported():
    for command in SUPPORTED_COMMANDS:
        print(command, " being tested")
        call_command(command)
        default_sit()
        print(command, " finished testing")
        print("__________________________")


def intro_seq():
    global interrupt
    global inprogress

    exec_keyframe(P_3, 1.5, "m_intro", "Hello everyone! Hope you're enjoying your \\emph=2\\day!",True)
    default_sit(1.5)
    if (interrupt):
            default_sit(0.5)
            print("INTERRUPT")
            interrupt = 0
            inprogress = 0
            return
    exec_keyframe(P_3, 2.5, "Me", "My name is Nao and I am from the Interaction Lab at USC!",True)
    if (interrupt):
            default_sit(0.5)
            print("INTERRUPT")
            interrupt = 0
            inprogress = 0
            return
    exec_keyframe(P_3, 5.0, "Question Medium",
                  "Thank you for joining me here. As you know, we are here today to talk about the stress we are feeling with school.",True)
    if (interrupt):
            default_sit(0.5)
            print("INTERRUPT")
            interrupt = 0
            inprogress = 0
            return
    exec_keyframe(P_3,5.5,"look_around","It is my hope that we can each share our experiences and feelings of stress at school with each other! \\pau=500\\ By sharing these feelings and experiences with each other we can grow and overcome them!",True)
    if (interrupt):
            default_sit(0.5)
            print("INTERRUPT")
            interrupt = 0
            inprogress = 0
            return
    exec_keyframe(P_3, 12.0, "Question Medium",
                  "In order for this to work, we are going to take turns sharing with each other. "
                  "You can ask follow up questions and respond to each other, but please don't interrupt"
                  " or talk over one another or I won't be able to understand.",True)
    default_sit()
    if (interrupt):
            default_sit(0.5)
            print("INTERRUPT")
            interrupt = 0
            inprogress = 0
            return
    say("Does that sound good?")
    exec_keyframe(P_3, 1.5, "m_agree", "",True)
    if (interrupt):
            default_sit(0.5)
            print("INTERRUPT")
            interrupt = 0
            inprogress = 0
            return
    exec_keyframe(P_3, 7.0, "Question Medium",
                  "To start, could you each introduce yourselves? Please share your name,"
                  " major, and one interesting fact about yourself.",True)
    default_sit()
    inprogress = 0
    interrupt = 0


def exit_seq():
    exec_keyframe(P_3, 8.0, "Question Medium","Alright everyone, looks like we are "
                                              "about out of time. I just wanted to say thank you all "
                                              "for sharing with me and I hope you found it a little "
                                              "bit helpful to talk out the stress.",True)
    exec_keyframe(P_3, 1.5, "m_intro", "See you all next time!")
    default_sit(3.0)
    inprogress = 0

def intro_ques():
    global interrupt
    global inprogress
    exec_keyframe(P_1, 2.0, "Question Medium", "Thanks for sharing! Let's get started!",True)
    if (interrupt):
            default_sit(0.5)
            print("INTERRUPT")
            interrupt = 0
            inprogress = 0
            return
    exec_keyframe(P_1, 3.0, "Question Low", "Let's start by talking about school. Looks like final exams are coming up",True)
    if (interrupt):
            default_sit(0.5)
            print("INTERRUPT")
            interrupt = 0
            inprogress = 0
            return
    exec_keyframe(P_1, 2.0, "Question Low", "What are some study strategies you use?",True)
    interrupt = 0
    inprogress = 0
def exit_ques():
    global interrupt
    global inprogress
    exec_keyframe(P_1, 2.0, "Question Medium", "Unfortunately looks like we are running out of time.",True)
    if (interrupt):
            default_sit(0.5)
            print("INTERRUPT")
            interrupt = 0
            inprogress = 0
            return
    exec_keyframe(P_1, 3.0, "Question Low", "What is something each of you, \\rspd=80\\ learned today?",True)
    interrupt = 0
    inprogress = 0
def main():
    # populate all basic features used to map
    pop_source()
    print(text_to_speech.getAvailableVoices())
    on = False
    if (on):
        intro_seq()
        # for general
        call_command("Acknowledge", P_1)
        # for question
        exec_keyframe(P_1, 6.0, "Question Low", "How was your day?")


if __name__ == "__main__":
    main()
