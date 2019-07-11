#!/usr/bin/env bash
CURR_TIME=$(date +"%m.%d.%Y_%Hh%Mm%Ss")
BASE_DIR="/home/zijian/Videos"
OUTPUT_DIR="${BASE_DIR}/${CURR_TIME}"
DEPTH_TOPIC="/camera/depth/image_raw"
POINT_CLOUD_TOPIC="/camera/ir/image"

VIDEO_EXTENSION="avi"

#ffmpeg -i output_cam1.avi -i micRecording.wav -strict -2 output.mp4
ffmpeg -i "outputDir/cam_output.mp4" -filter:v "crop=1280:720:1280:0" \
-c:a copy "outputDir/annotationVideo.mp4"