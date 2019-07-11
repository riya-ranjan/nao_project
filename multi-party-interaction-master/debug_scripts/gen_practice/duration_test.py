import sys
import time
import os
from naoqi import ALProxy
from motion_test import head_motion_test

interval = 30


def test_duration(ip_address, port=9559):
    body_temp = ALProxy("ALBodyTemperature", ip_address, port)
    text_to_speech = ALProxy("ALTextToSpeech", ip_address, port)
    audio_device = ALProxy("ALAudioDevice", ip_address, port)

    # Turn off notifications
    body_temp.setEnableNotifications(True)
    # Turn off the voice
    # audio_device.setOutputVolume(0)

    start_time = time.time()
    prev_time = start_time
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > 60 * 60:
            print("an hour has passed! Finished!")
            break

        print("\nTime elapsed: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

        diagnosis = body_temp.getTemperatureDiagnosis()
        print(diagnosis)

        # text_to_speech.say("Hi! Hello!")
        head_motion_test(ip_address, port)

        time.sleep(interval)

    # turn on the voice
    # audio_device.setOutputVolume(50)


if __name__ == "__main__":
    import main as main_py
    test_duration(main_py.IP, main_py.PORT)
