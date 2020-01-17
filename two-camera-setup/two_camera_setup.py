import cv2
import subprocess


class TwoCameraSetup:
    def __init__(self, input_first, input_second):
        self.input_path_first = input_first
        self.input_path_second = input_second

        self.input_first = cv2.VideoCapture(int(input_first))
        self.input_second = cv2.VideoCapture(int(input_second))

        self.set_camera_settings(input_first)
        self.set_camera_settings(input_second)

        frame_first = self.get_frame_first()
        frame_second = self.get_frame_second()

        self.SCREEN_HEIGHT_FIRST, self.SCREEN_WIDTH_FIRST = frame_first.shape[:2]
        self.SCREEN_HEIGHT_SECOND, self.SCREEN_WIDTH_SECOND = frame_second.shape[:2]

    def __enter__(self):
        return self

    def set_camera_settings(self, camera_port):
        camera_path = "/dev/video" + camera_port

        try:
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_auto=1"])
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_absolute=1"])
        except:
            print("exposure adjustment not completed")

    def get_frame_first(self):
        _, frame = self.input_first.read()
        return frame

    def get_frame_second(self):
        _, frame = self.input_second.read()
        return frame

    def run_cv(self):
        frame_first = self.get_frame_first()
        frame_second = self.get_frame_second()

        cv2.imshow("First camera" + str(self.input_path_first), frame_first)
        cv2.imshow("Second camera" + str(self.input_path_second), frame_second)
