'''
@author Ishaan Chandra
@date  7/16/19
@descr  makes Nao's hand reach up in the high five position and says high five
'''

import sys
from naoqi import ALProxy
import time
import almath
import config

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT

def main(IP):
    motion = ALProxy("ALMotion", IP, PORT)
    motion.setStiffnesses("RArm", 1.0) #stiffness must be >1 for robot to move
    shoulder = "RShoulderPitch"
    shoulderAngle = -1.0
    fractionMaxSpeedShoulder = 0.1
    motion.setAngles(shoulder, shoulderAngle, fractionMaxSpeedShoulder)

    motion.openHand("RHand")

    tts = ALProxy("ALTextToSpeech", IP, 9559)
    tts.say("High five!")

    time.sleep(3.0)
    motion.setAngles(shoulder, 1.5, fractionMaxSpeedShoulder)

if __name__=="__main__":
     main(IP)