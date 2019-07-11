from naoqi import ALProxy
import time
import almath
import argparse
import os
import sys
IP = "192.168.5.179"
PORT = 9559
#ALL TEST FUNCTIONS
def behavior_test ():
    bt = ALProxy("ALBehaviorManager", IP, PORT)
    tag_list= bt.getTagList()
    print("All Tags ", tag_list)
    behavior_list = bt.getLoadedBehaviors()
    print("All Behaviors ", behavior_list)
    print("Behaviors by vie en rose tag", bt.getBehaviorsByTag('vie en rose'))
    print("start_behavior")
    m = ALProxy("ALMotion",IP,PORT)
    m.setStiffnesses("Body",1)
    comm = 'animations/Sit/Emotions/Positive/Winner_1'
    print(bt.startBehavior(comm))
    time.sleep(3)
    print(bt.stopBehavior(comm))
    m.setStiffnesses("Body",0)

    print("end_behavior")

def hands_test(ip_address, port=9559):
    m = ALProxy("ALMotion",ip_address, port)
    m.openHand("LHand");
    m.closeHand("LHand");
    m.openHand("RHand");
    m.closeHand("RHand");
    print("finished Open Close operations")
def arm_test(ip_address, port=9559):
    m = ALProxy("ALMotion",ip_address, port)
    #first check that the arms are even enabled
    #print("LeftArmEnabled: ", m.getMoveArmsEnabled("LArm"))
    #print("RightArmEnaled: " + m.getMoveArmsEnabled("RArm"))
    #print("ArmEnaled: " + m.getMoveArmsEnabled("Arms"))
    if (m.getMoveArmsEnabled("Arms") == True):
        #continue
        print("All Ready!")
    else:
        m.setMoveArmsEnabled(True,True)
        print("Move arms enabled")
    #code of movment starts here
    print("Left elbow up")
    m.setStiffnesses("LArm",1.0)
    #Left elbow movement basic motion
    names = "LElbowRoll"
    angles = -88*almath.TO_RAD
    fractionMaxSpeed = 0.1
    m.setAngles(names,angles,fractionMaxSpeed)

    time.sleep(3.0)
    print("Left elbow down")
    names = "LElbowRoll"
    angles = -20*almath.TO_RAD
    fractionMaxSpeed = 0.1
    m.setAngles(names,angles,fractionMaxSpeed)
    time.sleep(1.5)
    m.setStiffnesses("LArm", 0.0)
def speech_test(ip_address, port=9559):
    text_to_speech = ALProxy("ALTextToSpeech", ip_address, port)
    print("successfully in the function. Speak")
    text_to_speech.say("\\vol=3\\ Hello!")
    print("Hello function terminated")
def speech_test(ip_address, port=9559):
    text_to_speech = ALProxy("ALTextToSpeech", ip_address, port)
    print("successfully in the function. Speak")
    m = ALProxy("ALMotion",ip_address, port)
    m.setStiffnesses("LLeg",0.0)
    m.setStiffnesses("RLeg",0.0)

    text_to_speech.say("\\vol=10\\ o!")
    print("Hello function terminated")

def hands_test(ip_address, port=9559):
    m = ALProxy("ALMotion",ip_address, port)
    m.openHand("LHand");
    m.closeHand("LHand");
    m.openHand("RHand");
    m.closeHand("RHand");
    print("finished Open Close operations")
def say_audio (address):
    aup = ALProxy("ALAudioPlayer", "127.0.0.1", 54710)
    fileId = aup.loadFile("C:/home/interaction/Downloads/bensound-buddy.mp3")
    time.sleep(5)
    aup.play(fileId)
def arm_test(ip_address, port=9559):
    m = ALProxy("ALMotion",ip_address, port)
    #first check that the arms are even enabled
    #print("LeftArmEnabled: ", m.getMoveArmsEnabled("LArm"))
    #print("RightArmEnaled: " + m.getMoveArmsEnabled("RArm"))
    #print("ArmEnaled: " + m.getMoveArmsEnabled("Arms"))
    if (m.getMoveArmsEnabled("Arms") == True):
        #continue
        print("All Ready!")
    else:
        m.setMoveArmsEnabled(True,True)
        print("Move arms enabled")
    #code of movment starts here
    print("Left elbow up")
    m.setStiffnesses("LArm",1.0)
    #Left elbow movement basic motion
    names = "LElbowRoll"
    angles = -88*almath.TO_RAD
    fractionMaxSpeed = 0.1
    m.setAngles(names,angles,fractionMaxSpeed)
    time.sleep(3.0)
    print("Left elbow down")
    names = "LElbowRoll"
    angles = -40*almath.TO_RAD
    fractionMaxSpeed = 0.1
    m.setAngles(names,angles,fractionMaxSpeed)
    m.setStiffnesses("LArm", 0.0)

def main():
    behavior_test()


if __name__ == "__main__":
    main()