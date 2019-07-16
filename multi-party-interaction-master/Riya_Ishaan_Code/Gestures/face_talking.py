'''
@author: Riya Ranjan
@date: 7/16/19
@desc: Robot should turn and face whoever is talking when certain buttons are pressed (not autonomous)
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
    motion.setStiffnesses("Head", 1.0)
    angles = [-1, -0.5, 0, 0.5, 1] #possible angles where the robot can direct its gaze
    headYaw = "HeadYaw"
    fractionMaxSpeed = 0.1

    while(True):
        num = input("Enter person num to look at")
        print(num)
        motion.setAngles(headYaw, angles[num-1], fractionMaxSpeed)
        time.sleep(1.0)
        nod()
        time.sleep(1.0)

def nod():
    headPitch = "HeadPitch"
    angleLists = [0, 0.4, 0, 0.4, 0]
    times = [1, 1.4, 1.8, 2.2, 2.6]
    isAbsolute = True
    motion.angleInterpolation(headPitch, angleLists, times, isAbsolute)

if __name__=="__main__":
     main(IP)