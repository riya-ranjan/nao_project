#!/usr/bin/env bash
CURR_TIME=$(date +"%m.%d.%Y_%Hh%Mm%Ss")
BASE_DIR="/media/sdbdrive"
OUTPUT_DIR="${BASE_DIR}/${CURR_TIME}"

DEPTH_TOPIC="/camera/depth/image_raw"
POINT_CLOUD_TOPIC="/camera/ir/image"

VIDEO_EXTENSION="avi"


mkdir -p ${OUTPUT_DIR} && \
rm "${BASE_DIR}/outputDir" ;
rm "./outputDir" ;
ln -s "${OUTPUT_DIR}" "./outputDir" && \
ln -s "${OUTPUT_DIR}" "${BASE_DIR}/outputDir" && \
tmux new-session -d -s "depthSession" rosrun multi_party_record astra_listener.py \
--topic ${DEPTH_TOPIC} \
--output "${OUTPUT_DIR}/output_depth.${VIDEO_EXTENSION}" \
--is_record True ;
tmux new-session -d -s "pointCloudSession" rosrun multi_party_record astra_listener.py \
--topic ${POINT_CLOUD_TOPIC} \
--output "${OUTPUT_DIR}/point_cloud.${VIDEO_EXTENSION}" \
--is_record True ;
tmux new-session -d -s "rosbagDepthSession" rosbag record \
-o "${OUTPUT_DIR}/depth_info.bag" ${DEPTH_TOPIC} ;
#tmux new-session -d -s "rosbagPointCloudSession" rosbag record \
#-o "${OUTPUT_DIR}/point_cloud.bag" ${POINT_CLOUD_TOPIC} ;

# this is a blocking call which should be put at the end of this script
obs --profile "MultiParty" --startrecording