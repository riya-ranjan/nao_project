## Getting Started
### Install Dependencies
1. install all required packages/libraries
    - install NAOqi SDK (C++ and Python)
        - see [this tutorial](https://www.zijianhu.com/post/nao-tutorial/installation/) for detail
    - install ROS Kinetic
        - install [ros_astra_camera](https://github.com/orbbec/ros_astra_camera)
            - follow instructions in the link
        - install [ros_astra_launch](https://github.com/orbbec/ros_astra_launch)
            - clone this repo to `<your ROS workspace root>/src`
        - install [cv_bridge](http://wiki.ros.org/cv_bridge/Tutorials)
            - execute `sudo apt install ros-kinetic-cv-bridge` and<br>
            `sudo apt-get install ros-kinetic-vision-opencv`
    - install python packages (see [requirement.txt](./gui_demo/server_side/requirement.txt))
    - install `ffmpeg` and `arecord`
        - execute `sudo apt install ffmpeg arecord`
1. install **multi_party_record package**
    1. copy [multi_party_record](./record/multi_party_record) folder to `<your ROS workspace>/src/`
    1. go back to your ROS workspace root directory
    1. execute `catkin_make` to install the packages
    
### Run the program
1. change **BASE_DIR** and **SCRIPT_DIR** in [record_all_in_one.sh](./record/record_all_in_one.sh)
to your desired output base directory
1. run **roscore** and wait until it says it's ready
1. run **astra camera topics**
    - execute `roslaunch astra_launch astra.launch`
1. run [socket_server.py](./gui_demo/server_side/socket_server.py)
1. open [index.html](./gui_demo/client-side/index.html) in your browser