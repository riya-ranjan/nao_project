#!/usr/bin/env bash
CURR_TIME=$(date +"%m.%d.%Y_%Hh%Mm%Ss")
BASE_DIR="/home/zijian/Videos"
OUTPUT_DIR="${BASE_DIR}/${CURR_TIME}"
SCRIPT_DIR="/home/zijian/Workspace/multi-party-interaction"

DEPTH_TOPIC="/camera/depth/image_raw"
POINT_CLOUD_TOPIC="/camera/ir/image"

VIDEO_EXTENSION="avi"

mkdir -p ${OUTPUT_DIR} && \
rm "${SCRIPT_DIR}/outputDirLink" ;
ln -s "${OUTPUT_DIR}" "${SCRIPT_DIR}/outputDirLink" && \
tmux new-session -d -s "camera1Session" \
python ~/Workspace/multi-party-interaction/record/record_single.py \
-o "${OUTPUT_DIR}/output_cam1.${VIDEO_EXTENSION}" \
-d "0";
tmux new-session -d -s "camera2Session" \
python ~/Workspace/multi-party-interaction/record/record_single.py \
-o "${OUTPUT_DIR}/output_cam2.${VIDEO_EXTENSION}" \
-d "1";
tmux new-session -d -s "camera3Session" \
python ~/Workspace/multi-party-interaction/record/record_single.py \
-o "${OUTPUT_DIR}/output_cam3.${VIDEO_EXTENSION}" \
-d "2";