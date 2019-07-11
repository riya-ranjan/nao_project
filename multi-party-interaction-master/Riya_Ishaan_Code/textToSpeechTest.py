from naoqi import ALProxy
import config

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT

tts = ALProxy("ALTextToSpeech", IP, 9559)
tts.say("Hello World!")