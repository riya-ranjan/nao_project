import cv2 as cv
import os.path as path
import argparse
import atexit
import numpy as np
import subprocess

fourCC = cv.VideoWriter_fourcc(*'XVID')


# fourCC = cv.VideoWriter_fourcc(*'X264')
# fourCC = cv.VideoWriter_fourcc(*'MJPG')


def main(device_num, output_filename):
    video_stream = cv.VideoCapture(device_num)
    video_size = (int(video_stream.get(cv.CAP_PROP_FRAME_WIDTH)),
                  int(video_stream.get(cv.CAP_PROP_FRAME_HEIGHT)))
    video_fps = video_stream.get(cv.CAP_PROP_FPS)

    # four_cc = cv.VideoWriter_fourcc(*'XVID')
    video_writer = cv.VideoWriter(output_filename, fourCC, video_fps, video_size)

    atexit.register(exit_hook, device_num=device_num, video_stream=video_stream, video_writer=video_writer)
    display_title = "Camera {} output".format(device_num)

    # start microphone recording
    if device_num == 0:
        output_dir = path.dirname(output_filename)
        print(output_dir)

        # start audio recording
        subprocess.Popen([
            'tmux new-session -d -s "audioSession" arecord -vv -fdat "{}/micRecording.wav"'.format(output_dir)
        ], shell=True)

    while True:
        ret, frame = video_stream.read()

        if not ret:
            break

        # display frame
        cv.imshow(display_title, frame)

        # save output
        cv_img = np.asarray(frame, dtype=np.uint8)
        video_writer.write(cv_img)

        # detect key press
        key = cv.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break


def exit_hook(device_num, video_stream, video_writer):
    print("Exiting...")

    if video_writer is not None:
        video_writer.release()

    if video_stream is not None:
        video_stream.release()

    if device_num == 0:
        subprocess.Popen([
            'tmux kill-session -t "audioSession"'
        ], shell=True)

    # clean up
    cv.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument("-d", "--device", dest="device", help="device number for recording",
                        default="0")

    parser.add_argument("-o", "--output", dest="output", help="the output path to store the recording",
                        default="./output_cam.avi")
    FLAGS = parser.parse_args()

    main(int(FLAGS.device), FLAGS.output)
