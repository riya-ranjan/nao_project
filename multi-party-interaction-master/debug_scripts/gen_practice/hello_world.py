from naoqi import ALProxy
import time
import os
import sys

def say_hello(ip_address, port=9559):
    text_to_speech = ALProxy("ALTextToSpeech", ip_address, port)
    print("successfully in the function. Should say Hello")
    text_to_speech.say("Hi! What's up!")
    print("Hello function terminated")

if __name__ == "__main__":
    say_hello("192.168.7.241",9559)
