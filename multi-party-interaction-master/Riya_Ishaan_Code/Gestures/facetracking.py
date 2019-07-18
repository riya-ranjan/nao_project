from naoqi import ALProxy
import sys
import config

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT

USAGE = "USAGE:\n" \
        "python vision_setfacetracking.py [NAO_IP] [0 or 1] \n" \
        "\nExamples: \n" \
        "Enable tracking: set_tracking.py 192.168.1.102 1\n" \
        "Disable tracking: set_tracking.py 192.168.1.102 0"


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

    tracking_enabled = True

    try:
        if len(sys.argv) > 1:
            nao_ip = sys.argv[1]

        if len(sys.argv) > 2:
            tracking_enabled = bool(int(sys.argv[2]))

        set_nao_face_detection_tracking(IP, PORT, tracking_enabled)

    except Exception as e:
        print "Exception Caught: %s\n" % e
        print USAGE


if __name__ == "__main__":
    main()