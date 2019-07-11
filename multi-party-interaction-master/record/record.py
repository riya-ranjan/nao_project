import cv2 as cv
import os.path as path
import argparse
import atexit

# fourCC = cv.VideoWriter_fourcc(*'XVID')
fourCC = cv.VideoWriter_fourcc(*'mp4v')
videoWriterList = list()
videoStreamList = list()


def main(output_dir):
    video_stream = cv.VideoCapture(0)
    video_size = (int(video_stream.get(cv.CAP_PROP_FRAME_WIDTH)),
                  int(video_stream.get(cv.CAP_PROP_FRAME_HEIGHT)))
    video_fps = video_stream.get(cv.CAP_PROP_FPS)
    video_writer = cv.VideoWriter(path.join(output_dir, "output_cam0.mp4"), fourCC, video_fps, video_size)
    videoStreamList.append(video_stream)
    videoWriterList.append(video_writer)

    video_stream1 = cv.VideoCapture(1)
    video_size = (int(video_stream1.get(cv.CAP_PROP_FRAME_WIDTH)),
                  int(video_stream1.get(cv.CAP_PROP_FRAME_HEIGHT)))
    video_fps = video_stream1.get(cv.CAP_PROP_FPS)
    video_writer1 = cv.VideoWriter(path.join(output_dir, "output_cam1.mp4"), fourCC, video_fps, video_size)
    videoStreamList.append(video_stream1)
    videoWriterList.append(video_writer1)

    video_stream2 = cv.VideoCapture(2)
    video_size = (int(video_stream2.get(cv.CAP_PROP_FRAME_WIDTH)),
                  int(video_stream2.get(cv.CAP_PROP_FRAME_HEIGHT)))
    video_fps = video_stream2.get(cv.CAP_PROP_FPS)
    video_writer2 = cv.VideoWriter(path.join(output_dir, "output_cam2.mp4"), fourCC, video_fps, video_size)
    videoStreamList.append(video_stream2)
    videoWriterList.append(video_writer2)

    while True:
        ret0, frame0 = video_stream.read()
        ret1, frame1 = video_stream1.read()
        ret2, frame2 = video_stream2.read()

        if not ret0 or not ret1 or not ret2:
            break

        # display frame
        cv.imshow("Camera 1 output", frame0)
        cv.imshow("Camera 2 output", frame1)
        cv.imshow("Camera 3 output", frame2)

        # save output
        video_writer.write(frame0)
        video_writer1.write(frame1)
        video_writer2.write(frame2)

        # detect key press
        key = cv.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # release
    video_writer.release()
    video_writer1.release()
    video_writer2.release()

    video_stream.release()
    video_stream1.release()
    video_stream2.release()

    # clean up
    cv.destroyAllWindows()


@atexit.register
def exit_hook():
    print("Exiting...")
    for i in range(len(videoWriterList)):
        videoStreamList[i].release()
        videoWriterList[i].release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument("-o", "--output", dest="output", help="the output path to store the recording",
                        default=".")
    FLAGS = parser.parse_args()

    main(FLAGS.output)
