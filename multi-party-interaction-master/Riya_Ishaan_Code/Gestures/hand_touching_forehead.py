'''
@author: Riya Ranjan
@date: 7/16/19
@desc: make nao touch its forehead as if it is thinking about something
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
    leftShoulderPitch = "LShoulderPitch"
    angle = 