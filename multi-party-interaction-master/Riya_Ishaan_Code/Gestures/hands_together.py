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

def config_beginning():
   
    shoulderRollBegin = ["LShoulderRoll", "RShoulderRoll"]
    angleShoulderRoll = [0.5,0.5]
    fractionMaxSpeed = 0.1
    motion.setAngles(shoulderRollBegin, angleShoulderRoll, fractionMaxSpeed)

    shoulderPitchBegin = ["LShoulderPitch", "RShoulderPitch"]
    angleShoulderPitch = [1.5, 1.5]
    
    motion.setAngles(shoulderPitchBegin,angleShoulderPitch,fractionMaxSpeed)


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