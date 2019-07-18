'''
UNFINISHED
@author: Riya Ranjan
@date: 7/16/19
@desc: make nao touch its forehead as if it is thinking about something
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
    config_shoulders()
    time.sleep(1.0)
    config_head()

def config_head():
    names = ["HeadYaw", "HeadPitch"]
    angles = [-0.4, 0.4]
    fractionMaxSpeed = 0.1
    motion.setAngles(names, angles, fractionMaxSpeed)

def config_shoulders():
    names = ["RShoulderPitch", "RShoulderRoll"]
    angles = [-1.0, 0.01]
    fractionMaxSpeed = 0.1
    motion.setAngles(names, angles, fractionMaxSpeed)
    '''
    time.sleep(0.5)
    elbowYaw = "RElbowYaw"
    angles = 1
    motion.setAngles(elbowYaw, angles, fractionMaxSpeed)
    '''
    time.sleep(1.0)
    motion.openHand("RHand")

if __name__=="__main__":
    main(IP)