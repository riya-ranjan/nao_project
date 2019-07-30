from naoqi import ALProxy
import config

IP = config.ROBOT_IP

tts = ALProxy("ALTextToSpeech", IP, 9559)
tts.say("Hello everyone! I am NAO and am from the Interaction Lab at USC! I am here to help you resolve conflicts!")
