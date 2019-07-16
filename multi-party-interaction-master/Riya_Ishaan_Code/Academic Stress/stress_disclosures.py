from naoqi import ALProxy
import random 


import config


IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
tts = ALProxy("ALTextToSpeech", IP, 9559)

def main():

    questions = ["Sometimes I work too hard and do not sleep much or at all. Has this happened to any of you?"]
    while(True):
        num = input ("Enter 1 to see Nao's comment ")
        tts.say(questions[num-1])


if __name__ == "__main__":
    main()