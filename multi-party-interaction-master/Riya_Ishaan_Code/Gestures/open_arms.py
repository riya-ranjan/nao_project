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
    
    config_shoulders()
    time.sleep(1.0)
    config_wrists()
    time.sleep(1.0)

def config_shoulders():
    names = ["RShoulderPitch", "LShoulderPitch", "RShoulderRoll", "LShoulderRoll"]
    fractionMaxSpeed = 0.1
    angles = [1, 1, 0, 0]
    motion.setAngles(names, angles, fractionMaxSpeed)

def config_wrists():
    
    isAbsolute = True
    #wrists upwards
    names = ["RWristYaw", "LWristYaw"]
    fractionMaxSpeed = 0.1
    angles = [-1.8, -1.8]
    motion.setAngles(names, angles, fractionMaxSpeed)
    
    time.sleep(1.0)
    joints = ["LElbowRoll", "RElbowRoll"]
    angleList = [[-1, -0.5, -0.03], [1, 0.5, 0.03]]
    times = [[1, 1.2, 1.4], [1, 1.2, 1.4]]
    motion.angleInterpolation(joints, angleList, times, isAbsolute)

    time.sleep(1.0)
    elbowYaws = ["RElbowYaw", "LElbowYaw"]
    elbowAngles = [-2, -2]
    motion.setAngles(elbowYaws, elbowAngles, fractionMaxSpeed)

    time.sleep(1.0)
    num = input('enter 1, 2, or 3')
    time.sleep(1.0)
    config_elbows(num)

def config_elbows(numEntered):
    #open hands
    isAbsolute = True
    if(numEntered == 1):
        motion.openHand("RHand")
        time.sleep(1.0)

        joint = "RElbowRoll"
        angles = [1, 0.5, 0.03]
        times = [1, 1.2, 1.4]
        motion.angleInterpolation(joint, angles, times, isAbsolute)
    elif(numEntered == 2):
        motion.openHand("LHand")
        time.sleep(1.0)
        
        joint = "LElbowRoll"
        angles = [-1, -0.5, -0.03]
        times = [1, 1.2, 1.4]
        motion.angleInterpolation(joint, angles, times, isAbsolute)
    elif(numEntered == 3):
        motion.openHand("RHand")
        motion.openHand("LHand")
        time.sleep(1.0)

        joints = ["LElbowRoll", "RElbowRoll"]
        angleList = [[-1, -0.5, -0.03], [1, 0.5, 0.03]]
        times = [[1, 1.2, 1.4], [1, 1.2, 1.4]]
        motion.angleInterpolation(joints, angleList, times, isAbsolute)
    else:
        num = input('enter 1, 2, or 3')
        config_elbows(num)

if __name__=="__main__":
     main(IP)