from naoqi import ALProxy


def reset_robot_settings(ip_address, port=9559, volume=50):
    # initialize proxy objects
    audio_device = ALProxy("ALAudioDevice", ip_address, port)
    body_temprature = ALProxy("ALBodyTemperature", ip_address, port)
    motion = ALProxy("ALMotion", ip_address, port)

    # default volume is 50
    audio_device.setOutputVolume(volume)

    # enable temprature notifications
    body_temprature.setEnableNotifications(True)

    # turn on motors
    motion.wakeUp()

    # stop motion
    motion.stopMove()

    # Go to rest position
    motion.rest()


if __name__ == "__main__":
    import sys

    sys.path.append("../..")
    from config import ROBOT_IP, ROBOT_PORT
    reset_robot_settings(ROBOT_IP, ROBOT_PORT, volume=50)
