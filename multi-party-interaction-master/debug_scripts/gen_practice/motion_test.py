from naoqi import ALProxy
import time
import math


def posture_test(ip_address, port=9559):
    robot_posture = ALProxy("ALRobotPosture", ip_address, port)
    motion = ALProxy("ALMotion", ip_address, port)

    print("Postures: ", robot_posture.getPostureList())
    print("Current posture: ", robot_posture.getPosture())

    # print("Body Stiffnesses: ", motion.getStiffnesses('Body'))
    # print("JointActuators Stiffnesses: ", motion.getStiffnesses('JointActuators'))
    # print("Joints Stiffnesses: ", motion.getStiffnesses('Joints'))
    # print("Actuators Stiffnesses: ", motion.getStiffnesses('Actuators'))

    # motion.setStiffnesses('Body', 1.0);
    # motion.setStiffnesses('JointActuators', 1.0);
    # motion.setStiffnesses('Joints', 1.0);

    motion.wakeUp()

    # robot_posture.goToPosture('StandInit', 0.2)
    # time.sleep(1)
    # robot_posture.goToPosture('StandZero', 0.2)
    # time.sleep(1)
    # robot_posture.goToPosture('Stand', 0.2)
    # time.sleep(1)
    robot_posture.goToPosture('StandInit', 0.2)
    time.sleep(1)

    # Example showing how Initialize move process.
    motion.moveInit()

    print("prepare to move...")
    motion.move(0.1, 0.0, 0.0)
    time.sleep(2)
    motion.stopMove()

    print("prepare to move backward...")
    motion.move(-0.1, 0.0, 0.0)
    time.sleep(2)

    # stop motion
    motion.stopMove()

    # Go to rest position
    motion.rest()

def head_motion_test(ip_address, port=9559):
    motion = ALProxy("ALMotion", ip_address, port)

    # wake up robot
    # motion.wakeUp()
    motion.setStiffnesses('HeadYaw', 1.0);

    # get head informations
    print("HeadYaw (w/o sensor): ", motion.getAngles("HeadYaw", False))
    print("HeadYaw (w/ sensor): ", motion.getAngles("HeadYaw", True))
    # print("HeadPitch (w/o sensor): ", motion.getAngles("HeadPitch", False))
    # print("HeadPitch (w/ sensor): ", motion.getAngles("HeadPitch", True))

    for i in range(4):
        if i % 2 == 1:
            motion.setAngles("HeadYaw", -15.0 * math.pi / 180.0, 0.2)
        else:
            motion.setAngles("HeadYaw", 15.0 * math.pi / 180.0, 0.2)
        time.sleep(1)

    motion.setAngles("HeadYaw", 0, 0.2)
    time.sleep(1)
    motion.setStiffnesses('HeadYaw', 0.0);

def behavior_test(ip_address, port=9559):
    behavior_manager = ALProxy("ALBehaviorManager", ip_address, port)

    print("Installed behaviors: ", behavior_manager.getInstalledBehaviors())

if __name__ == "__main__":
    import main as main_py

    head_motion_test(main_py.IP, main_py.PORT)