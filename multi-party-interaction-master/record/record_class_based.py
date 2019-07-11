import cv2 as cv

fourCC = cv.VideoWriter_fourcc(*'DIVX')


class Recorder:
    def __init__(self):
        self.videoStreamList = list()
        self.videoWriterList = list()
        self.frameBuffer = list()

    def add(self, input_path, output_path, frame_size=None):
        if frame_size is None:
            frame_size = (1280, 720)

        video_stream = cv.VideoCapture(input_path)
        # four_cc = int(video_stream.get(cv.CAP_PROP_FOURCC))
        four_cc = cv.VideoWriter_fourcc(*'XVID')
        video_fps = video_stream.get(cv.CAP_PROP_FPS)
        video_size = (int(video_stream.get(cv.CAP_PROP_FRAME_WIDTH)),
                      int(video_stream.get(cv.CAP_PROP_FRAME_HEIGHT)))

        video_writer = cv.VideoWriter(output_path, four_cc, video_fps, video_size, True)
        self.videoStreamList.append(video_stream)
        self.videoWriterList.append(video_writer)
        self.frameBuffer.append(None)

    def read(self, display=True):
        if len(self.videoWriterList) == 0 or len(self.videoStreamList) == 0:
            return False, None

        return_value = True
        for idx, video_stream in enumerate(self.videoStreamList):
            ret, frame = video_stream.read()

            if not ret:
                return False, None

            return_value = return_value and ret
            self.frameBuffer[idx] = frame

            if display:
                cv.imshow("Camera {} output".format(idx + 1), frame)

        return return_value

    def write(self):
        for idx, video_writer in enumerate(self.videoWriterList):
            video_writer.write(self.frameBuffer[idx])

    def release(self):
        for idx in range(len(self.videoWriterList)):
            self.videoStreamList[idx].release()
            self.videoWriterList[idx].release()


def main(recorder):
    while True:
        if not recorder.read(display=True):
            break

        # save recording
        recorder.write()

        # detect key press
        key = cv.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # release
    recorder.release()

    # clean up
    cv.destroyAllWindows()


if __name__ == '__main__':
    import os.path as path

    basePath = '/home/zijian/Videos'

    recorderObj = Recorder()

    for i in range(3):
        recorderObj.add(i, path.join(basePath, "output_cam{}.avi".format(i)))

    main(recorderObj)
