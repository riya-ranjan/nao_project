'''
@author Ishaan Chandra
@date  7/17/19
@description 
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
    motion.setStiffnesses("RArm", 1.0) #stiffness must be >1 for robot to move
    shoulder = "RShoulderPitch"
    shoulderAngle = -0.75
    fractionMaxSpeedShoulder = 0.1
    motion.setAngles(shoulder, shoulderAngle, fractionMaxSpeedShoulder)

    motion.openHand("RHand")

    elbowYaw = "RElbowYaw"
    elbowYawAngle =  0.0
    fractionMaxSpeedElbow = 0.1
    motion.setAngles(elbowYaw, elbowYawAngle, fractionMaxSpeedElbow)
    
    time.sleep(2)

''' Option 1: wave with elbow movement
    elbowRoll = "RElbowRoll"
    angleLists = [1, 0.5, 0.03, 0.5, 1, 0.5, 0.03]
    times = [1, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8]
    isAbsolute = True
    motion.angleInterpolation(elbowRoll, angleLists, times, isAbsolute)
'''

#Option 2 wave with wrist movement
    wrist = "RWristYaw"
    wristAngleLists = [-1.5, -0.5, 0.03, 0.5, 1.5, 0.5, 0]
    wristTimes = [1, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8]
    isAbsolute = True
    motion.angleInterpolation(wrist, wristAngleLists, wristTimes, isAbsolute)


if __name__=="__main__":
     main(IP)
