import numpy as np
import cv2
import subprocess
import pyrealsense2 as rs


class DepthLiveGenerator:
    def __init__(self, input):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        prof = self.pipeline.start(self.config)
        s = prof.get_device().query_sensors()[1]
        s.set_option(rs.option.exposure, 50)
        self.input_path = input

        self.input = cv2.VideoCapture(int(input))
        self.set_camera_settings(str(input))

        frame, _, _ = self.get_frame()

        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]

    def __enter__(self):
        return self

    def set_camera_settings(self, camera_port):
        camera_path = "/dev/video" + camera_port

        try:
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_auto=1"])
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_absolute=1"])
        except:
            print("exposure adjustment not completed")

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            return
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        return color_image, depth_image, depth_frame

    def generate(self):
        arr = np.empty((self.SCREEN_HEIGHT, self.SCREEN_WIDTH))
        _, _, frame = self.get_frame()
        for y in range(self.SCREEN_HEIGHT):
            for x in range(self.SCREEN_WIDTH):
                arr[y, x] = frame.get_distance(x, y)
        return np.asanyarray(arr)
