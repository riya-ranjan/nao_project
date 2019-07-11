#!/usr/bin/env python

# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2 as cv
import numpy as np

import sys
import argparse

bridge = CvBridge()

# fourCC = cv.VideoWriter_fourcc(*'DIVX')
fourCC = cv.VideoWriter_fourcc(*'XVID')

videoSize = (640, 480)
videoFPS = 30.0
videoWriter = None
FLAGS = None

pointCloudTopic = "/camera/ir/image"
depthImageTopic = "/camera/depth/image_raw"
# depthImageTopic = "/camera/depth/image_rect_raw"


def image_record_callback(msg):
    global videoWriter

    try:
        # Convert your ROS Image message to OpenCV2
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
    except CvBridgeError, e:
        print(e)
    else:
        cv_img = np.asarray(cv_img, dtype=np.uint8)
        # Save your OpenCV2 image as a jpeg
        videoWriter.write(cv_img)
        cv.imshow(FLAGS.topic, cv_img)

        # detect key press
        key = cv.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            videoWriter.release()
            rospy.signal_shutdown("Manual Exit")


def image_view_callback(msg):
    try:
        # Convert your ROS Image message to OpenCV2
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
    except CvBridgeError, e:
        print(e)
    else:
        cv_img = np.asarray(cv_img, dtype=np.uint8)
        cv.imshow(FLAGS.topic, cv_img)

        # detect key press
        key = cv.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            rospy.signal_shutdown("Manual Exit")


def main(image_topic, is_record=True):
    rospy.init_node('astra_listener', anonymous=True)
    # Set up your subscriber and define its callback
    if is_record:
        rospy.Subscriber(image_topic, Image, image_record_callback)
    else:
        rospy.Subscriber(image_topic, Image, image_view_callback)
    # Spin until ctrl + c
    rospy.spin()


def shutdown_hook():
    print("Exiting...")
    global videoWriter

    if videoWriter is not None:
        videoWriter.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument("-t", "--topic", dest="topic", help="the topic you want to subscribe",
                        default="/camera/ir/image")

    parser.add_argument("-o", "--output", dest="output", help="the output path to store the recording",
                        default="./output_point_cloud.avi")

    parser.add_argument("-r", "--is_record", dest="is_record", help="the output path to store the recording",
                        default=True)
    FLAGS = parser.parse_args(rospy.myargv()[1:])

    videoWriter = cv.VideoWriter(FLAGS.output, fourCC, videoFPS, videoSize, False)

    # hook shutdown callback
    rospy.on_shutdown(shutdown_hook)

    main(FLAGS.topic, is_record=FLAGS.is_record)
