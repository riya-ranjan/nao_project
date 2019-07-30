'''
@author Ishaan Chandra
@date  7/30/19
@description touches Nao's hands and fingers together while nodding
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
    motion.setStiffnesses("LArm", 1.0) #stiffness must be >1 for robot to move
    #shoulder pitch(up)
    shoulder = ["LShoulderPitch", "RShoulderPitch"]
    motion.openHand("RHand")
    motion.openHand("LHand")
    shoulderAngles = [0.75, 0.85]
    fractionMaxSpeedShoulder = 0.1
    motion.setAngles(shoulder, shoulderAngles, fractionMaxSpeedShoulder)
    time.sleep(1.0)

    #shoulder roll
    shoulderRoll = ["LShoulderRoll", "RShoulderRoll"]
    shoulderRollAngles = [0.0, 0.0]
    motion.setAngles(shoulderRoll, shoulderRollAngles, fractionMaxSpeedShoulder)

    #elbow yaw(tilt)
    time.sleep(0.1)
    elbowYaw = ["LElbowYaw","RElbowYaw"]
    elbowYawAngle = [-0.5, 0.75]
    fractionMaxSpeedElbowYaw = 0.1
    motion.setAngles(elbowYaw, elbowYawAngle, fractionMaxSpeedElbowYaw)

    #elbow roll(move inwards)
    time.sleep(0.1)
    elbowRoll = ["LElbowRoll","RElbowRoll"]
    elbowRollAngle = [-1.25, 1.25]
    fractionMaxSpeedElbowRoll = 0.1
    motion.setAngles(elbowRoll, elbowRollAngle, fractionMaxSpeedElbowRoll)

    #wrist yaw(tilt)
    time.sleep(0.1)
    wristYaw = ["LWristYaw","RWristYaw"]
    wristYawAngle = [-1.25, 1.0]
    fractionMaxSpeedWristYaw = 0.1
    motion.setAngles(wristYaw, wristYawAngle, fractionMaxSpeedWristYaw)

    #head
    head = "HeadPitch"
    headAngleLists = [0.25, 0.35, 0.15, -0.15, -.35, -0.25, 0, 0.15, 0.35, 0.15, 0]
    times = [1, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0, 5.3, 5.6]
    isAbsolute = True
    motion.angleInterpolation(head, headAngleLists, times, isAbsolute)

    
if __name__=="__main__":
     main(IP)