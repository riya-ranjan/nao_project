''''
@author Ishaan Chandra
@date  7/17/19
@description 
''''
import sys
from naoqi import ALProxy
import time
import almath
import config

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
motion = ALProxy("ALMotion", IP, PORT)

def main(IP):
    motion = ALProxy("ALMotion", IP, PORT)
    motion.setStiffnesses("RArm", 1.0) #stiffness must be >1 for robot to move
    shoulder = "RShoulderPitch"
    shoulderAngle = -1.0
    fractionMaxSpeedShoulder = 0.1
    motion.setAngles(shoulder, shoulderAngle, fractionMaxSpeedShoulder)

    motion.openHand("RHand")

    time.sleep(3.0)
    motion.setAngles(shoulder, 1.5, fractionMaxSpeedShoulder)

    time.sleep(1)
    naeJoints = ["RElbowRoll"]
    angleLists2 = [-1, -0.5, -0.03, -0.5, -1, -0.5, -0.03]
    times2 = [1, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8]
    motion.angleInterpolation(naeJoints, angleLists2, times2, isAbsolute)

if __name__=="__main__":
     main(IP)
