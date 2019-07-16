import sys
from naoqi import ALProxy
import time
import almath
import config

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT

def main(IP):
    motion = ALProxy("ALMotion", IP, Port)

    motion = ALProxy("ALMotion", IP, PORT)
    motion.setStiffnesses("RArm", 1.0) #stiffness must be >1 for robot to move
    shoulder = "RShoulderPitch"
    shoulderAngle = -2.0857
    fractionMaxSpeedShoulder = 0.1
    motion.setAngles(shoulder, shoulderAngle, fractionMaxSpeedShoulder)

    motion.openHand("RHand")

    tts = ALProxy("ALTextToSpeech", IP, 9559)
    tts.say("High five!")