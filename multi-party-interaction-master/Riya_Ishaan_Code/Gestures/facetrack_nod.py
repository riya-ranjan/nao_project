import qi
import time
import cv2
import sys
import argparse
import config
from naoqi import ALProxy

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT
motion = ALProxy("ALMotion", IP, PORT)

class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.on_human_tracked)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        self.motion = session.service("ALMotion")
        self.face_detection = session.service("ALFaceDetection")
        self.face_tracker = session.service("ALFaceTracker")
        self.face_tracker.startTracker()
        self.face_detection.subscribe("HumanGreeter")
        self.posture_setup = session.service("ALRobotPosture")
        self.got_face = False
        self.motion.setStiffnesses("Head", 1.0)
        self.motion.setStiffnesses("Body",1.0)
        self.posture_setup.goToPosture("StandInit", 0.5)

    def nod(self):
        self.motion.setStiffnesses("Head", 1.0) #stiffness must be >1 for robot to move
        head = "HeadPitch"
        headAngleLists = [0.25, 0.35, 0.15, -0.15, -.35, -0.25, 0, 0.15, 0.35, 0.15, 0]
        times = [1, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0, 5.3]
        isAbsolute = True
        motion.angleInterpolation(head, headAngleLists, times, isAbsolute)

    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """
        if value == []:  # empty value when the face disappears
            self.got_face = False
        elif not self.got_face:  # only speak the first time a face appears
            self.got_face = True
            print "I saw a face!"
            self.nod()
            
            # First Field = TimeStamp.
            timeStamp = value[0]
            print "TimeStamp is: " + str(timeStamp)

            # Second Field = array of face_Info's.
            faceInfoArray = value[1]
            for j in range( len(faceInfoArray)-1 ):
                faceInfo = faceInfoArray[j]

                # First Field = Shape info.
                faceShapeInfo = faceInfo[0]

                # Second Field = Extra info (empty for now).
                faceExtraInfo = faceInfo[1]

                print "Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
                print "Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
                print "Face Extra Infos :" + str(faceExtraInfo)

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting HumanGreeter"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping HumanGreeter"
            self.face_tracker.stopTracker()
            self.face_detection.unsubscribe("HumanGreeter")
            app.stop()
            while(self.face_tracker.isActive()):
                self.face_tracker.stopTracker()
            self.posture_setup.goToPosture("Crouch", 0.2)
            #self.motion.setStiffnesses("Body", 0.0)
            
            #stop
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + IP + ":" + str(PORT)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + IP + "\" on port " + str(PORT) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = HumanGreeter(app)
    human_greeter.run()