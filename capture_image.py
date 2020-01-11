import cv2
import subprocess
import imghdr
import os

# finds angle between robot's heading and the perpendicular to the targets
class ImageCapture:

    # initilaze variables
    def __init__(self, input, angle, distance):

        self.input_path = input
        self.angle = angle
        self.distance = distance

        try:
            # if input is a camera port
            self.input = cv2.VideoCapture(int(input))
            self.set_camera_settings(input)
        except:
            # if input is a path
            self.input = cv2.VideoCapture(input)

        frame = self.get_frame()
        
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.input.release()
        cv2.destroyAllWindows()
        print("\nexited")

    # sets exposure of the camera (will only work on Linux systems)
    def set_camera_settings(self, camera_port):

        camera_path = "/dev/video" + camera_port

        try:
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_auto=1"])
            subprocess.call(["v4l2-ctl", "-d", camera_path, "-c", "exposure_absolute=1"])
        except:
            print("exposure adjustment not completed")

    # returns a frame corresponding to the input type
    def get_frame(self):

        frame = None

        # if input is a camera port, use VideoCapture()
        if self.input_path.isdigit():
            _, frame = self.input.read()
        # if input is an image, use cv2.imread()
        elif imghdr.what(self.input_path) is not None:
            frame = cv2.imread(self.input_path)
        # if input is a video, use VideoCapture()
        else:
            _, frame = self.input.read()

        return frame

    def update_frame(self):
        frame = self.get_frame()
        cv2.imshow("frame: " + str(self.input_path), frame)

        ref_frame = self.get_frame()
        cv2.circle(frame, (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT - 20), 2, (255,255,255), 2)
        cv2.circle(frame, (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2), 2, (255,255,255), 2)
        cv2.imshow("ref: " + str(self.input_path), frame)

    def capture(self):
        filename = "test_photos/" + str(self.angle) + "degrees" + str(self.distance) + "inches.png"
        cv2.imwrite(filename, self.get_frame())

    def prompt(self):
        print("Capture another image! yay")
        self.angle = input("Angle: ")
        self.distance = input("Distance: ")
