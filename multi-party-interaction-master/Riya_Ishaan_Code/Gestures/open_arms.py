'''
@author: Riya Ranjan
@date: 7/16/19
@desc: make nao open its arm to invite others to speak up
'''
import sys
from naoqi import ALProxy
import time
import almath
import config

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
motion = ALProxy("ALMotion", IP, PORT)


def main(IP):
    motion.setStiffnesses("RArm", 1.0)
    motion.setStiffnesses("LArm", 1.0)
    motion.openHand("RHand")
    motion.openHand("LHand")
    time.sleep(1.0)
    config_shoulders()
    time.sleep(1.0)
    config_elbows()
    time.sleep(1.0)
    config_wrists()

def config_shoulders():
    shoulderPitch = ["LShoulderPitch", "RShoulderPitch"]
    angles = [0.8,0.8]
    fractionMaxSpeed = 0.1
    motion.setAngles(shoulderPitch,angles,fractionMaxSpeed)
    
    shoulderRoll = ["LShoulderRoll", "RShoulderRoll"]
    anglesRoll = [-0.3, 0.3]
    motion.setAngles(shoulderRoll,anglesRoll,fractionMaxSpeed)
'''
configure elbows so that NAO's arms are in the correct position
'''

def config_elbows():
    elbowYaw = ["LElbowYaw", "RElbowYaw"]
    angles = [0,0]
    fractionMaxSpeed = 0.1
    motion.setAngles(elbowYaw, angles, fractionMaxSpeed)
    time.sleep(1.0)
    names = ["LElbowRoll", "RElbowRoll"]
    angleLists = [ -1.5,  1.5]
    motion.setAngles(names, angleLists, fractionMaxSpeed)

    time.sleep(1.0)
    angles = [-2, 2]
    motion.setAngles(elbowYaw, angles, fractionMaxSpeed)

    time.sleep(1.0)
    shoulderRoll = ["LShoulderRoll", "RShoulderRoll"]
    anglesRoll = [0.5, -0.5]
    motion.setAngles(shoulderRoll,anglesRoll,fractionMaxSpeed)

def config_wrists():
    names = ["LWristYaw", "RWristYaw"]
    angleLists = [-1.8, 1.8]
    fractionMaxSpeed = 0.1
    motion.setAngles(names, angleLists, fractionMaxSpeed)
    time.sleep(1.0)

if __name__=="__main__":
     main(IP)