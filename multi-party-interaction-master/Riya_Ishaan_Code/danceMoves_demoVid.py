from naoqi import ALProxy
import random 
import config


IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
tts = ALProxy("ALTextToSpeech", IP, 9559)

def main():

    questions = ["I can do cool things like dance!", "whip and nae nae!", "and dab!"]
    while(True):
        num = input ("Enter a number between 1-3: ")
        tts.say(questions[num-1])


if __name__ == "__main__":
    main()