import sys
import time
import os
from naoqi import ALProxy
import random


def play_file(filepath, ip_address, port=9559):
    try:
        aup = ALProxy("ALAudioPlayer", ip_address, port)
    except Exception, e:
        print "Could not create proxy to ALAudioPlayer"
        print "Error was: ", e
        return

    # Loads a file and launch the player 2 seconds later
    # the file path is the path in robot
    file_id = aup.loadFile(filepath)
    time.sleep(2)
    aup.play(file_id)
