from reset import reset_robot_settings
from check_version import show_robot_info
from audio_player import play_file
from hello_world import say_hello
from duration_test import test_duration
from motion_test import posture_test, behavior_test

IP = "192.168.7.114"
PORT = 9559


def main():
    # display robot information
    show_robot_info(IP, PORT)
    print("------------------------------------------------")

    reset_robot_settings(IP, PORT, volume=50)

    # say_hello(IP, PORT)

    play_file("/home/nao/sounds/robot_blip.wav", IP, PORT)

    # posture_test(IP, PORT)
    print("------------------------------------------------")

    # behavior_test(IP, PORT)
    print("------------------------------------------------")

    say_hello(IP, PORT)
    # test_duration(IP, PORT)


if __name__ == "__main__":
    main()
