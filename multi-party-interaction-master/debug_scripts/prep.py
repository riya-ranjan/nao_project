from naoqi import ALProxy


IP = "192.168.7.114"
PORT = 9559
VOLUME = 50

def main():
    # initialize proxy objects
    audio_device = ALProxy("ALAudioDevice", IP, PORT)
    body_temprature = ALProxy("ALBodyTemperature", IP, PORT)
    motion = ALProxy("ALMotion", IP, PORT)

    # default volume is 50
    audio_device.setOutputVolume(VOLUME)

    # enable temprature notifications
    body_temprature.setEnableNotifications(True)

    # turn on motors
    motion.wakeUp()

    # stop motion
    motion.stopMove()

    # Go to rest position
    motion.rest()

if __name__ == "__main__":
    main()