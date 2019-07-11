'''
this code tries to make the robot move its left elbow joint in an outward motion
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
    motion.setStiffnesses("LArm", 1.0) #stiffness must be >1 for robot to move
    shoulder = "LShoulderPitch"
    shoulderAngle = -2.0857
    fractionMaxSpeedShoulder = 0.1
    motion.setAngles(shoulder, shoulderAngle, fractionMaxSpeedShoulder)

    whipJoints = ["LElbowYaw","LWristYaw"]
    angleLists = [[-2.0857, -2, -1.2, -0.6, 0],[-1.8238, -1, -0.2, 0.4, 1]]
    times = [[1, 1.4, 1.8, 2.2, 2.6],[1, 1.4, 1.8, 2.2, 2.6]]
    isAbsolute = True;
    motion.angleInterpolation(whipJoints, angleLists, times, isAbsolute)

    '''
    elbow = "LElbowYaw" #moves joint across x plane
    elbowAngle = -119.5*almath.TO_RAD
    fractionMaxSpeedElbow = 0.1

    motion.setAngles(elbow, elbowAngle, fractionMaxSpeedElbow)

    wrist = "LWristYaw"
    wristAngles = [-1.8238, -1, 0, 1, 1.8238]
    times = [1, 1.2, 1.4, 1.6, 1.8];
    isAbsolute = True;
    motion.angleInterpolation(wrist, wristAngles, times, isAbsolute)
    '''
if __name__=="__main__":
    main(IP)