import numpy as np
import cv2
import subprocess
import pyrealsense2 as rs


class DepthLiveGenerator:
    def __init__(self, input_port):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        prof = self.pipeline.start(self.config)
        s = prof.get_device().query_sensors()[1]
        s.set_option(rs.option.exposure, 80)
        self.input_path = input_port


        self.input = cv2.VideoCapture(int(input_port))
        self.set_camera_settings(str(input_port))
        self.input.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.input.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.scale = prof.get_device().first_depth_sensor().get_depth_scale()
        print(self.scale)
        # self.scale = float(1/1186)

        frame, _, _ = self.get_frame()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]

        self.H_FIELD_OF_VIEW = 69.4
        self.V_FIELD_OF_VIEW = 42.5

    def __enter__(self):
        return self

    def set_camera_settings(self, camera_port):
        camera_path = "/dev/video" + camera_port

        try:
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_auto=1"])
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_absolute=1"])
        except FileNotFoundError:
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

    def get_horizontal_fov(self):
        return self.H_FIELD_OF_VIEW

    def get_vertical_fov(self):
        return self.V_FIELD_OF_VIEW

    def generate(self):
        image, depth, _ = self.get_frame()
        return image, self.scale*depth
