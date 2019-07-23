'''
@author: Riya Ranjan
@date: 7/11/19
@desc: All questions/method calls pertaining to questions asked about bullying for the middle school students will be stored/coded here
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
    motion.setStiffnesses("LArm", 1.0)
    motion.setStiffnesses("RArm", 1.0)
    motion.setStiffnesses("Head",1.0)

    config_shoulders()
    time.sleep(2.0)
    config_head()

def config_shoulders():
    #shoulder has to move to the 90 degree pos
    shoulderPitch = ["LShoulderPitch", "RShoulderPitch"]
    shoulderAngles = [[0,-0.8],[0, -1]]
    times = [[1, 1.4], [1, 1.4]]
    isAbsolute = True
    motion.angleInterpolation(shoulderPitch, shoulderAngles, times, isAbsolute)

    time.sleep(0.1)
    shoulderRoll = ["LShoulderRoll", "RShoulderRoll"]
    shoulderAngles2 = [[0.1],[-0.9]]
    times = [[1],[1]]
    motion.angleInterpolation(shoulderRoll, shoulderAngles2, times, isAbsolute)
    time.sleep(0.1)
    elbowYaw = ["LElbowYaw", "RElbowYaw"]
    elbowYawAngles = [0,0]
    fractionMaxSpeed = 0.1
    motion.setAngles(elbowYaw, elbowYawAngles, fractionMaxSpeed)
    time.sleep(0.1)

    elbowRoll = ["LElbowRoll","RElbowRoll"]
    elbowAngles = [-1.54,0.03]
    fractionMaxSpeed = 0.1
    motion.setAngles(elbowRoll, elbowAngles, fractionMaxSpeed)

def config_head():
    name = ["HeadPitch","HeadYaw"]
    angle = [0.5129, 0.85]
    fractionMaxSpeed = 0.1
    motion.setAngles(name, angle, fractionMaxSpeed)
    print('shoulder configuration finished')

if __name__=="__main__":
    main(IP)