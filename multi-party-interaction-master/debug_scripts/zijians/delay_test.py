from naoqi import ALProxy
import time
import random

from reset import reset_robot_settings

totalIter = 100
greetMsgs = ("Hi", "Hello", "How are you",
             "How have you been", "Nice", "Okay",
             "No problem", "Cool", "Good", "Yes")


def delay_test_slow(ip_address, port=9559):
    audio_device = ALProxy("ALAudioDevice", ip_address, port)

    audio_device.setOutputVolume(20)
    total_elapsed_time = 0

    _ = raw_input("Press any key to start the test: ")
    for i in range(totalIter):
        start_time = time.time()

        text_to_speech = ALProxy("ALTextToSpeech", ip_address, port)

        rand_idx = random.randint(0, len(greetMsgs) - 1)
        text_to_speech.say(greetMsgs[rand_idx])

        elapsed_time = time.time() - start_time
        total_elapsed_time += elapsed_time

    audio_device.setOutputVolume(50)
    print("average elapsed time: {}".format(total_elapsed_time / totalIter))


def delay_test(ip_address, port=9559):
    audio_device = ALProxy("ALAudioDevice", ip_address, port)
    text_to_speech = ALProxy("ALTextToSpeech", ip_address, port)

    audio_device.setOutputVolume(20)
    total_elapsed_time = 0

    _ = raw_input("Press any key to start the test: ")
    for i in range(totalIter):
        start_time = time.time()

        rand_idx = random.randint(0, len(greetMsgs) - 1)
        text_to_speech.say(greetMsgs[rand_idx])

        elapsed_time = time.time() - start_time
        total_elapsed_time += elapsed_time

    audio_device.setOutputVolume(50)
    print("average elapsed time: {}".format(total_elapsed_time / totalIter))


if __name__ == "__main__":
    from config import IP, PORT

    reset_robot_settings(IP, PORT)

    # print("Start the delay test normal version")
    # delay_test(IP, PORT)

    print("Start the delay test slow version")
    delay_test_slow(IP, PORT)
