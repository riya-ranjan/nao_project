from naoqi import ALProxy
import time
import random 
import config


IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
tts = ALProxy("ALTextToSpeech", IP, 9559)
motion = ALProxy("ALMotion", IP, PORT)

def main():
    
    speech = ["I noticed an issue here", "How are you feeling?", "Does anybody else want to share?", "Thanks for sharing with me today. Good job!", "Goodbye","I can also help resolve issues in groups with my dialogue.", "I can also detect and follow faces.", "I try to show my understanding of problems."]
    while(True):
        num = input ("Enter a number between 1-7: ")
        if(num == 3):
                motion.setStiffnesses("RArm", 1.0)
                motion.setStiffnesses("LArm", 1.0)
                motion.post.openHand("RHand")
                motion.post.openHand("LHand")
                time.sleep(0.1)
                config_shoulders()
                time.sleep(0.1)
                config_elbows()
                time.sleep(0.1)
                config_wrists()
        tts.post.say(speech[num-1])


def config_shoulders():
    shoulderPitch = ["LShoulderPitch", "RShoulderPitch"]
    angles = [0.8,0.8]
    fractionMaxSpeed = 0.1
    motion.setAngles(shoulderPitch,angles,fractionMaxSpeed)
    
    shoulderRoll = ["LShoulderRoll", "RShoulderRoll"]
    anglesRoll = [-0.3, 0.3]
    motion.post.setAngles(shoulderRoll,anglesRoll,fractionMaxSpeed)

def config_elbows():
    elbowYaw = ["LElbowYaw", "RElbowYaw"]
    angles = [0,0]
    fractionMaxSpeed = 0.1
    motion.post.setAngles(elbowYaw, angles, fractionMaxSpeed)
    time.sleep(1.0)
    names = ["LElbowRoll", "RElbowRoll"]
    angleLists = [ -1.5,  1.5]
    motion.post.setAngles(names, angleLists, fractionMaxSpeed)

    time.sleep(1.0)
    angles = [-2, 2]
    motion.post.setAngles(elbowYaw, angles, fractionMaxSpeed)

    time.sleep(1.0)
    shoulderRoll = ["LShoulderRoll", "RShoulderRoll"]
    anglesRoll = [0.5, -0.5]
    motion.post.setAngles(shoulderRoll,anglesRoll,fractionMaxSpeed)

def config_wrists():
    names = ["LWristYaw", "RWristYaw"]
    angleLists = [-1.8, 1.8]
    fractionMaxSpeed = 0.1
    motion.post.setAngles(names, angleLists, fractionMaxSpeed)
    time.sleep(1.0)


if __name__ == "__main__":
    main()