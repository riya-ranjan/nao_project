import time
import config
from naoqi import ALProxy

IP =  config.ROBOT_IP # Replace here with your NaoQi's IP address.
PORT = config.ROBOT_PORT

def set_nao_face_detection_tracking(IP, PORT, tracking_enabled):
    """Make a proxy to nao's ALFaceDetection and enable/disable tracking.

    """
    print "Will set tracking to '%s' on the robot ..." % tracking_enabled
    # Enable or disable tracking.
    faceProxy.setTrackingEnabled(tracking_enabled)
    # Just to make sure correct option is set.
    print "Is tracking now enabled on the robot?", faceProxy.isTrackingEnabled()
# Create a proxy to ALFaceDetection
try:
  faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:
  print "Error when creating face detection proxy:"
  print str(e)
  exit(1)

# Subscribe to the ALFaceDetection proxy
# This means that the module will write in ALMemory with
# the given period below
period = 500
faceProxy.subscribe("Test_Face", period, 0.0 )

# ALMemory variable where the ALFacedetection modules
# outputs its results
memValue = "FaceDetected"

# Create a proxy to ALMemory
try:
  memoryProxy = ALProxy("ALMemory", IP, PORT)
except Exception, e:
  print "Error when creating memory proxy:"
  print str(e)
  exit(1)

set_nao_face_detection_tracking(IP, PORT, True)

# A simple loop that reads the memValue and checks whether faces are detected.
try:
    while True:
        time.sleep(1.0)
        val = memoryProxy.getData(memValue)

        print ""
        print "*****"
        print ""

        # Check whether we got a valid output.
        if(val and isinstance(val, list) and len(val) >= 2):

            # We detected faces !
            # For each face, we can read its shape info and ID.

            # First Field = TimeStamp.
            timeStamp = val[0]

            # Second Field = array of face_Info's.
            faceInfoArray = val[1]

            try:
            # Browse the faceInfoArray to get info on each detected face.
                for j in range( len(faceInfoArray)-1 ):
                    faceInfo = faceInfoArray[j]

                    # First Field = Shape info.
                    faceShapeInfo = faceInfo[0]

                    # Second Field = Extra info (empty for now).
                    faceExtraInfo = faceInfo[1]

                    print "  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
                    print "  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])

            except Exception, e:
                print "faces detected, but it seems getData is invalid. ALValue ="
                print val
                print "Error msg %s" % (str(e))
        else:
            print "No face detected"
except KeyboardInterrupt:
    print "Interrupted by user, stopping HumanGreeter"
    #stop
    sys.exit(0)
    faceProxy.unsubscribe("Test_Face")

print "Test terminated successfully."



