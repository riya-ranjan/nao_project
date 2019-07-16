from naoqi import ALProxy
import random 


import config


IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
tts = ALProxy("ALTextToSpeech", IP, 9559)

def main():

    questions = ["How did you feel about the task you did in school today?", "What about the task contributed to your emotions?", "Talk about yourself, how do you relax and destress, how much sleep are you getting per night?", "How engaged do you feel while doing the task", "What about your academic environment would you change?", "How do external pressures affect your emoitions about academics?"]
    while(True):
        num = input ("Enter a number between 1-6: ")
        tts.say(questions[num-1])


if __name__ == "__main__":
    main()