import subprocess
import time
import signal
import os
import atexit

DEPTH_TOPIC = "/camera/depth/image_raw"
POINT_CLOUD_TOPIC = "/camera/ir/image"

SCRIPT_BASE_PATH = "/home/zijian/Workspace/multi-party-interaction/record"

processList = list()


@atexit.register
def exit_hook():
    # for process in processList:
    #     os.killpg(os.getpgid(process), signal.SIGTERM)
    print("Exiting...")


def main():
    subprocess.Popen(['zsh', '{}/record_all_in_one.sh'.format(SCRIPT_BASE_PATH)])
    time.sleep(20)

    subprocess.call(['tmux', 'kill-server'])


if __name__ == '__main__':
    main()
