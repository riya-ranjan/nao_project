from naoqi import ALProxy
import random 


import config


IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
tts = ALProxy("ALTextToSpeech", IP, 9559)

def main():

    questions = ["What are you feeling?","Why do you feel that way?","What would you change to improve how you feel?","What can you control in the situation to improve how you feel?","How do you think the other person is feeling"]
    while(True):
        num = input ("Enter a number between 1-5: ")
        tts.say(questions[num-1])


if __name__ == "__main__":
    main()