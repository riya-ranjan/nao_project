from naoqi import ALProxy
import config

IP = config.ROBOT_IP
motion.setStiffnesses("RArm", 1.0) #stiffness must be >1 for robot to move
shoulder = "RShoulderPitch"
shoulderAngle = -0.75
fractionMaxSpeedShoulder = 0.5
motion.setAngles(shoulder, shoulderAngle, fractionMaxSpeedShoulder)

motion.openHand("RHand")

elbowYaw = "RElbowYaw"
elbowYawAngle =  0.0
fractionMaxSpeedElbow = 0.5
motion.setAngles(elbowYaw, elbowYawAngle, fractionMaxSpeedElbow)

time.sleep(0.1)

#Option 1: wave with elbow movement
joints = ["RElbowRoll","RWristYaw"]
angleLists = [[0.7, 0.5, 0.03, 0.5, 0.7, 0.5, 0.03],[-1.0, -0.5, 0.03, 0.5, 1.0, 0.5, 0]]
times = [[1, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4],[1, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4]]
isAbsolute = True
motion.angleInterpolation(joints, angleLists, times, isAbsolute)
tts = ALProxy("ALTextToSpeech", IP, 9559)
tts.say("Hello everyone! I am NAO and am from the Interaction Lab at USC! I am here to help you resolve conflicts!")\
