import sys
from naoqi import ALProxy
import time
import almath
import config

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT

def main(IP):
    motion = ALProxy("ALMotion", IP, PORT)

    #shoulder pitch(up)
    motion.setStiffnesses("RArm", 1.0) #stiffness must be >1 for robot to move
    motion.setStiffnesses("LArm", 1.0) #stiffness must be >1 for robot to move
    shoulder = ["LShoulderPitch", "RShoulderPitch"]
    motion.openHand("RHand")
    motion.openHand("LHand")
    shoulderAngles = [0.0, 0.0]
    fractionMaxSpeedShoulder = 0.1
    motion.setAngles(shoulder, shoulderAngles, fractionMaxSpeedShoulder)

    #elbow yaw(tilt)
    time.sleep(0.1)
    elbowYaw = ["LElbowYaw","RElbowYaw"]
    elbowYawAngle = [-0.75, -0.75]
    fractionMaxSpeedElbowYaw = 0.1
    motion.setAngles(elbowYaw, elbowYawAngle, fractionMaxSpeedElbowYaw)

    #elbow roll(move inwards)
    time.sleep(0.1)
    elbowRoll = ["LElbowRoll","RElbowRoll"]
    elbowRollAngle = [-1.0, 1.0]
    fractionMaxSpeedElbowRoll = 0.1
    motion.setAngles(elbowRoll, elbowRollAngle, fractionMaxSpeedElbowRoll)


if __name__=="__main__":
     main(IP)