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

    config_beginning()
    time.sleep(3.0)
    config_shoulders()
    time.sleep(2.0)
    config_head()

def config_beginning():
    shoulderPitchBegin = ["LShoulderPitch", "RShoulderPitch"]
    angleShoulderPitch = [1.5, 1.5]
    fractionMaxSpeed = 0.1
    motion.setAngles(shoulderPitchBegin,angleShoulderPitch,fractionMaxSpeed)

    shoulderRollBegin = ["LShoulderRoll", "RShoulderRoll"]
    angleShoulderRoll = [0.5,0]
    motion.setAngles(shoulderRollBegin, angleShoulderRoll, fractionMaxSpeed)

    elbowYawBegin = ["LElbowYaw", "RElbowYaw"]
    angleElbowYaw = [0,0]
    motion.setAngles(elbowYawBegin,angleElbowYaw,fractionMaxSpeed)

    elbowRollBegin = ["LElbowRoll", "RElbowRoll"]
    angleElbowRoll = [0,0]
    motion.setAngles(elbowRollBegin,angleElbowRoll,fractionMaxSpeed)

    headBegin = ["HeadPitch", "HeadYaw"]
    angleHead = [0,0]
    motion.setAngles(headBegin,angleHead,fractionMaxSpeed)

    wristYawBegin = ["LWristYaw", "RWristYaw"]
    angleWristYaw = [0,0]
    motion.setAngles(wristYawBegin,angleWristYaw,fractionMaxSpeed)
def config_shoulders():
    #shoulder has to move to the 90 degree pos
    shoulderPitch = ["LShoulderPitch", "RShoulderPitch"]
    shoulderAngles = [[0,-0.8],[0, -1]]
    times = [[1, 1.4], [1, 1.4]]   
    isAbsolute = True
    motion.angleInterpolation(shoulderPitch, shoulderAngles, times, isAbsolute)

    shoulderRoll = ["LShoulderRoll", "RShoulderRoll"]
    shoulderAngles2 = [[-0.2],[-0.9]]
    times = [[1],[1]]
    motion.angleInterpolation(shoulderRoll, shoulderAngles2, times, isAbsolute)

    elbowRoll = "LElbowRoll"
    elbowAngles = -1.54
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