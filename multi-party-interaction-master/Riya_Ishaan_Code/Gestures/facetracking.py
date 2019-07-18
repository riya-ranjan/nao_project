from naoqi import ALProxy
import time
import sys
from MotionMaestro import MotionMaestro
import RegisterMaestro
import config

from naoqi import ALBroker
from naoqi import ALModule

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT





def set_nao_face_detection_tracking(IP, PORT, tracking_enabled):
    """Make a proxy to nao's ALFaceDetection and enable/disable tracking.
    """
    faceProxy = ALProxy("ALFaceDetection", IP, PORT)

    print "Will set tracking to '%s' on the robot ..." % tracking_enabled

    # Enable or disable tracking.
    faceProxy.setTrackingEnabled(tracking_enabled)

    # Just to make sure correct option is set.
    print "Is tracking now enabled on the robot?", faceProxy.isTrackingEnabled()


def main():

    myBroker = ALBroker("myBroker","0.0.0.0",0,IP,PORT)
    tracking_enabled = True
    set_nao_face_detection_tracking(IP, PORT, tracking_enabled)
    postureProxy=RegisterMaestro.registerPostureProxy()
    motionProxy=RegisterMaestro.registerMotionProxy()
    motionMaestro = MotionMaestro(postureProxy,motionProxy)
    motionMaestro.standUp()

    faceProxy = ALProxy("ALFaceDetection", IP, PORT)

    faceVal=faceProxy.learnFace("Folke")
    print "this is the f-result"
    print faceVal
    return 
    for i in xrange(0,10):
        print "still active"
        time.sleep(10)


if __name__ == "__main__":
    main()