import qi
import time
import sys
import argparse
import config
from naoqi import ALProxy

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT

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
        self.face_detection.setTrackingEnabled(True)
        self.face_detection.subscribe("HumanGreeter")
        self.got_face = False
        self.motion.setStiffnesses("Head", 1.0)


    def wave_hand(self):
        self.motion.setStiffnesses("RArm", 1.0) #stiffness must be >1 for robot to move
        shoulder = "RShoulderPitch"
        shoulderAngle = -0.75
        fractionMaxSpeedShoulder = 0.5
        self.motion.setAngles(shoulder, shoulderAngle, fractionMaxSpeedShoulder)

        self.motion.openHand("RHand")

        elbowYaw = "RElbowYaw"
        elbowYawAngle =  0.0
        fractionMaxSpeedElbow = 0.5
        self.motion.setAngles(elbowYaw, elbowYawAngle, fractionMaxSpeedElbow)
    
        time.sleep(1)

        #Option 1: wave with elbow movement
        elbowRoll = "RElbowRoll"
        angleLists = [1, 0.5, 0.03, 0.5, 1, 0.5, 0.03]
        times = [1, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8]
        isAbsolute = True
        self.motion.angleInterpolation(elbowRoll, angleLists, times, isAbsolute)
        
    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """
        if value == []:  # empty value when the face disappears
            self.got_face = False
        elif not self.got_face:  # only speak the first time a face appears
            self.got_face = True
            print "I saw a face!"
            self.wave_hand()
            self.tts.say("Hello, you!")
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
            self.face_detection.unsubscribe("HumanGreeter")
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