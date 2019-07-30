from naoqi import ALProxy
import random 
import config


IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
tts = ALProxy("ALTextToSpeech", IP, 9559)

def main():
    
    speech = ["I noticed an issue here", "How are you feeling?", "Does anybody else want to share?", "Thanks for sharing with me toady. Good job!", "Bye, everybody"]
    while(True):
        num = input ("Enter a number between 1-3: ")
        tts.say(speech[num-1])


if __name__ == "__main__":
    main()