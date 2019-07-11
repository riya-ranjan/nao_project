# Multi-Party Human Robot Interaction

## Description:
This repository is for developing multi-party algorithms for use in SAR. It will cover the sensing and WoZ control of the Nao Robot.

## Getting Started
- See the [instructions](./INSTRUCTION.md)

## Project Components:

### Software
- [Ubuntu 16.04 LTS](http://releases.ubuntu.com/16.04/)
- [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu)
    - [ros_astra_camera](https://github.com/orbbec/ros_astra_camera)
    - [ros_astra_launch](https://github.com/orbbec/ros_astra_launch)
    - [cv_bridge](http://wiki.ros.org/cv_bridge/Tutorials)
- [Choregraphe and NAOqi](https://community.ald.softbankrobotics.com/en/resources/software/language/en-gb/robot/nao-2)

### Nao Robot
- Documentations and Guide see [this tutorial](https://www.zijianhu.com/post/nao-tutorial/installation/)
- Development Tools:
    - [NAO script-box format](http://doc.aldebaran.com/2-1/software/choregraphe/objects/python_script.html#python-script)
    - [NAOqi API](http://doc.aldebaran.com/2-1/naoqi/index.html#naoqi-api)
    - [NAO Actuator & Sensor list](http://doc.aldebaran.com/2-1/family/nao_dcm/actuator_sensor_names.html)
        - [NAO Joint Ctrl Terms](http://doc.aldebaran.com/2-1/family/robots/bodyparts.html#nao-chains)
        - [NAO Joint Ctrl Sample Code](http://doc.aldebaran.com/2-1/naoqi/motion/control-joint.html)

### Simulation
- [nao_moveit_config](https://github.com/ros-naoqi/nao_moveit_config)


### Orbec Astra 3D Sensor
- [Astra Documentation](https://orbbec3d.com/develop/)
- [Astra Ros Package](http://wiki.ros.org/astra_camera)

### Microphone Array
- TBD

## Control Paradigm
The setup will consist of a Nao Robot, a microphone array, and a 3D sensor. The signals from which will be viewed by a WoZ controller, who will select from a set of predermined actions and phrases which will then be executed by the robot.

### Motion Control 
The system uses keyframes in order to parse commands to the Nao-Robot. The keyframes are divided into `main_motion.json` and `sub_motion.json`. The main motions contain high level detail of commands which are directly called by `main_control.py`. The `sub_motion.json` lists specific motor movements. 
Steps:
- Enter `main_motion.json` to create major commands
    - Add a new command while including parameter  `submotions` (array)
        - Each submotion *must* have `pct_time` (0-100%)
        - Optional parameters which define movement include:
            - `animation_name`: preloaded behavior (refer to `taglist.txt` for more detail)
            - `tags`: preloaded tag behavior (refer to `taglist.txt` for more detail)
            - `submotion_name`: manual behavior defined in `sub_motion.json`
- *Optional*: Enter `sub_motion.json` to define angle-specific motion
    - Add a new command name (array default) with each keyframe including:
        - `name`: Name of keyframe (pure documentation)
        - `pct_time`: pct of time (0-100%)
        - `motion`: an array of all angles moved. Each has:
            - `n`: Name of [joint] (http://doc.aldebaran.com/1-14/family/robots/joints_robot.html)
            - `angle`: Angle of joint movement (degrees)

### Speech Control
The system reads and parses a variety of files which contain multiple speech commands coordinated with `main_motion.json`. 
- Enter `speech` file
    - Pick `.txt` file best fitting category of command
        - Want to see if you Classification already exists? Check `SUPPORTED_COMMANDS` array in `master_control.py`.
    - Add line in following format: `<speech> | <Classification>`
        - Ensure that `<Classification>` coordinates with a motion in `main_motion.json`. Refer to **Motion Control** for more detail
    - New classification? Add it to the `SUPPORTED_COMMANDS` array in `master_control.py`.
- Speech command can now be tested by running `call_command(<Classification>)` in `master_control.py`

### WoZ Interface
- See [instructions](./INSTRUCTION.md)

## Data Processing
### Text to Speech 
- [Google Cloud Text-to-Speech API](https://cloud.google.com/text-to-speech/docs/basics)
- Set-Up Sets:
    - Refer to [Google API SDK setup](https://cloud.google.com/text-to-speech/docs/quickstart-protocol) to connect terminal to Google Cloud Services and set environment variable GOOGLE_APPLICATION_CREDENTIALS.
        - If using *Bashful* you can just run `export GOOGLE_APPLICATION_CREDENTIALS=/home/interaction/Downloads/notional-portal-230904-63d2487d00d9.json`
        - Ensure *gcloud* command works. If it doesn't try to debug in the google sdk folder and follow [these steps](https://stackoverflow.com/questions/31037279/gcloud-command-not-found-while-installing-google-cloud-sdk)
    - Open file in `/workspace/multi-party-interaction/sample.sh`
    - Edit `text` field in order to change what the robot will say.
        - refer to Text-to-Speech API for further speech specification
    - Run `./run.sh`. The program will populate *output.txt* 
    - In *output.txt*, edit the contents of the file out of json format so the file only contains the base64 numbers `example:  //NExAASWoXsAUEQAAAABRjGAExv/`
    - Run `base64 output.txt --decode > <ouput-file-name>.mp3`

