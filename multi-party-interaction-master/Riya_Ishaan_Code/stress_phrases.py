from naoqi import ALProxy
import random 


import config


IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
tts = ALProxy("ALTextToSpeech", IP, 9559)

def main():

    questions = ["I understand", "Take a deep breath", "I am proud of you", "You are loved", "Remember how you have gotten through tough times before", "You are important"]
    while(True):
        num = input ("Enter a number between 1-6: ")
        tts.say(questions[num-1])


if __name__ == "__main__":
    main()