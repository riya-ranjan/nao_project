from naoqi import ALProxy
import config

IP = config.ROBOT_IP
motion = ALProxy("ALMotion", IP, 9559)
motion.setStiffnesses("Body", 1.0)
motion.moveInit()
motion.moveTo(0.5, 0, 0)