from naoqi import ALProxy
import config

IP = config.ROBOT_IP

tts = ALProxy("ALTextToSpeech", IP, 9559)
tts.say("Hello world")