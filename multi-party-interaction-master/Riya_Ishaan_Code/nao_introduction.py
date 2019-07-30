from naoqi import ALProxy
import time
import config

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
tts = ALProxy("ALTextToSpeech", IP, 9559)
motion = ALProxy("ALMotion", IP, PORT)

def main(IP):
    wave_hand()
    tts.post.say("Hello everyone!\\pau=2000\\")
    tts.say("I am NAO. I am from the Interaction Lab at USC! I am here to help you resolve conflicts!")

def wave_hand():
    motion.setStiffnesses("RArm", 1.0) #stiffness must be >1 for robot to move
    shoulder = "RShoulderPitch"
    shoulderAngle = -0.75
    fractionMaxSpeedShoulder = 0.5
    motion.post.setAngles(shoulder, shoulderAngle, fractionMaxSpeedShoulder)
    joints = ["RElbowRoll","RWristYaw"]
    angleLists = [[0.7, 0.5, 0.03, 0.5, 0.7, 0.5, 0.03],[-1.0, -0.5, 0.03, 0.5, 1.0, 0.5, 0]]
    times = [[1, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4],[1, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4]]
    isAbsolute = True
    motion.post.openHand("RHand")

    elbowYaw = "RElbowYaw"
    elbowYawAngle =  0.0
    fractionMaxSpeedElbow = 0.5
    motion.post.setAngles(elbowYaw, elbowYawAngle, fractionMaxSpeedElbow)
    #Option 1: wave with elbow movement
    motion.post.angleInterpolation(joints, angleLists, times, isAbsolute)

if __name__=="__main__":
     main(IP)