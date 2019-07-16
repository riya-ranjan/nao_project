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
    config_beginning()
    time.sleep(2.0)

    motion.setStiffnesses("LArm", 1.0) #stiffness must be >1 for robot to move
    shoulder = "LShoulderPitch"
    motion.closeHand('LHand')
    shoulderAngle = 0.2
    fractionMaxSpeedShoulder = 0.1
    motion.setAngles(shoulder, shoulderAngle, fractionMaxSpeedShoulder)

    time.sleep(0.5)
    whipJoints = ["LElbowYaw","LWristYaw"]
    angleLists = [[-2.0857, -2, -1.2, -0.6, 0],[-1.8238, -1, -0.2, 0.4, 1]]
    times = [[1, 1.4, 1.8, 2.2, 2.6],[1, 1.4, 1.8, 2.2, 2.6]]
    isAbsolute = True;
    motion.angleInterpolation(whipJoints, angleLists, times, isAbsolute)

    time.sleep(1)
    #nae nae
    shoulderAngle2 = [0, -0.8]
    shoulderTimes = [1, 1.4]
    motion.angleInterpolation(shoulder, shoulderAngle2, shoulderTimes, isAbsolute)

    time.sleep(1)
    motion.openHand('LHand')
    naeJoints = ["LElbowRoll", "LWristYaw"]
    angleLists2 = [[-1, -0.5, -0.03, -0.5, -1, -0.5, -0.03], [-0.5, 0, 0.2, 0.5, 0.2, 0, -0.5, 0, 0.2, 0.5]]
    times2 = [[1, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8], [1, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6]]
    motion.angleInterpolation(naeJoints, angleLists2, times2, isAbsolute)
    motion.openHand('LHand')
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

if __name__=="__main__":
    main(IP)