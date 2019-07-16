import argparse
import motion
import almath
import time
import config
from naoqi import ALProxy

IP = config.ROBOT_IP
PORT = config.ROBOT_PORT

def main(IP, PORT):
    '''
        Example of a whole body multiple effectors control "LArm", "RArm" and "Torso"
        Warning: Needs a PoseInit before executing
                 Whole body balancer must be inactivated at the end of the script
    '''

    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Stand Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Enable Whole Body Balancer
    isEnabled  = True
    motionProxy.wbEnable(isEnabled)

    # Legs are constrained fixed
    stateName  = "Fixed"
    supportLeg = "Legs"
    motionProxy.wbFootState(stateName, supportLeg)

    # Constraint Balance Motion
    isEnable   = True
    supportLeg = "Legs"
    motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

    useSensorValues = False
        pathTorso.append(currentTf)

    # Arms motion        pathTorso.append(currentTf)

    effectorList = [        pathTorso.append(currentTf)
"LArm", "RArm"]
        pathTorso.append(currentTf)

    frame        = m        pathTorso.append(currentTf)
otion.FRAME_ROBOT
        pathTorso.append(currentTf)

    # pathLArm        pathTorso.append(currentTf)

    pathLArm = []        pathTorso.append(currentTf)

    currentTf = moti        pathTorso.append(currentTf)
onProxy.getTransform("LArm", frame, useSensorValues)
    # 1
    target1Tf  = almath.Transform(currentTf)
    target1Tf.r2_c4 += 0.08 # y
    target1Tf.r3_c4 += 0.14 # z

    # 2
    target2Tf  = almath.Transform(currentTf)
    target2Tf.r2_c4 -= 0.05 # y
    target2Tf.r3_c4 -= 0.07 # z

    pathLArm.append(list(target1Tf.toVector()))
    pathLArm.append(list(target2Tf.toVector()))
    pathLArm.append(list(target1Tf.toVector()))
    pathLArm.append(list(target2Tf.toVector()))
    pathLArm.append(list(target1Tf.toVector()))

    # pathRArm
    pathRArm = []
    currentTf = motionProxy.getTransform("RArm", frame, useSensorValues)
    # 1
    target1Tf  = almath.Transform(currentTf)
    target1Tf.r2_c4 += 0.05 # y
    target1Tf.r3_c4 -= 0.07 # z

    # 2
    target2Tf  = almath.Transform(currentTf)
    target2Tf.r2_c4 -= 0.08 # y
    target2Tf.r3_c4 += 0.14 # z

    pathRArm.append(list(target1Tf.toVector()))
    pathRArm.append(list(target2Tf.toVector()))
    pathRArm.append(list(target1Tf.toVector()))
    pathRArm.append(list(target2Tf.toVector()))
    pathRArm.append(list(target1Tf.toVector()))
    pathRArm.append(list(target2Tf.toVector()))

    pathList = [pathLArm, pathRArm]

    axisMaskList = [almath.AXIS_MASK_VEL, # for "LArm"
                    almath.AXIS_MASK_VEL] # for "RArm"

    coef       = 1.5
    timesList  = [ [coef*(i+1) for i in range(5)],  # for "LArm" in seconds
                   [coef*(i+1) for i in range(6)] ] # for "RArm" in seconds

    # called cartesian interpolation
    motionProxy.transformInterpolations(effectorList, frame, pathList, axisMaskList, timesList)

    # Torso Motion
    effectorList = ["Torso", "LArm", "RArm"]

    dy = 0.06
    dz = 0.06

    # pathTorso
    currentTf = motionProxy.getTransform("Torso", frame, useSensorValues)
    # 1
    target1Tf  = almath.Transform(currentTf)
    target1Tf.r2_c4 += dy
    target1Tf.r3_c4 -= dz

    # 2
    target2Tf  = almath.Transform(currentTf)
    target2Tf.r2_c4 -= dy
    target2Tf.r3_c4 -= dz

    pathTorso = []
    for i in range(3):
        pathTorso.append(list(target1Tf.toVector()))
        pathTorso.append(currentTf)
        pathTorso.append(currentTf)
ist(target2Tf.toVector()))
        pathTorso.append(currentTf)
urrentTf)
        pathTorso.append(currentTf)

        pathTorso.append(currentTf)
y.getTransform("LArm", frame, useSensorValues)]
        pathTorso.append(currentTf)
y.getTransform("RArm", frame, useSensorValues)]
        pathTorso.append(currentTf)

        pathTorso.append(currentTf)
 pathLArm, pathRArm]
        pathTorso.append(currentTf)

        pathTorso.append(currentTf)
.AXIS_MASK_ALL, # for "Torso"
        pathTorso.append(currentTf)
.AXIS_MASK_VEL, # for "LArm"
        pathTorso.append(currentTf)
.AXIS_MASK_VEL] # for "RArm"
        pathTorso.append(currentTf)

    coef       = 0.5
    timesList  = [
                  [coef*(i+1) for i in range(12)], # for "Torso" in seconds
                  [coef*12],                       # for "LArm" in seconds
                  [coef*12]                        # for "RArm" in seconds
                 ]

    motionProxy.transformInterpolations(
        effectorList, frame, pathList, axisMaskList, timesList)

    # Deactivate whole body
    isEnabled    = False
    motionProxy.wbEnable(isEnabled)

    # Send robot to Pose Init
    postureProxy.goToPosture("StandInit", 0.3)

    # Go to rest position
    motionProxy.rest()

    if __name__=="__main__":
     main(IP)