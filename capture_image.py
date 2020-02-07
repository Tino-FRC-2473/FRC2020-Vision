import math
import cv2
import numpy as np
import subprocess
import imghdr
import traceback
import os
from math import sin, cos
from operator import add


# finds rotation and translation of vision targets
class CaptureImage:

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> Add test images
    # initilaze variables
<<<<<<< HEAD
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
<<<<<<< HEAD
<<<<<<< HEAD
            
        frame = self.get_frame()
        self.input.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.input.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]
        print(self.SCREEN_HEIGHT)
=======

=======
            
>>>>>>> Manually set frame dimensions and add test images
        frame = self.get_frame()
        self.input.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.input.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]
<<<<<<< HEAD
>>>>>>> Add test images
=======
        print(self.SCREEN_HEIGHT)
>>>>>>> Manually set frame dimensions and add test images
=======
    def __init__(self, detector):

        self.detector = detector
        self.generator = detector.get_generator()

        frame, _ = self.generator.generate()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]
        
        # constant to scale down display windows
        self.DISPLAY_CONSTANT = 0.8 if self.SCREEN_HEIGHT > 1000 else 1.0

>>>>>>> Integrate capture code with Generator and Detector classes

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        cv2.destroyAllWindows()
        print("exited")

    def display_windows(self, frame, ref_frame):
        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.namedWindow("ref_frame", cv2.WINDOW_NORMAL)

        cv2.resizeWindow("frame", (int(self.DISPLAY_CONSTANT * self.SCREEN_WIDTH), int(self.DISPLAY_CONSTANT * self.SCREEN_HEIGHT)))
        cv2.resizeWindow("ref_frame", (int(self.DISPLAY_CONSTANT * self.SCREEN_WIDTH), int(self.DISPLAY_CONSTANT * self.SCREEN_HEIGHT)))

        cv2.moveWindow("frame", 350, 30)
        cv2.moveWindow("ref_frame", 1000, 30)

        cv2.imshow("frame", frame)
        cv2.imshow("ref_frame", ref_frame)

    def update_frame(self):
        frame, _ = self.generator.generate()

        ref_frame, _ = self.generator.generate()
        cv2.circle(ref_frame, (int(self.SCREEN_WIDTH/2), int(self.SCREEN_HEIGHT/2 - 200)), 2, (255, 255, 255), 2)
        cv2.circle(ref_frame, (int(self.SCREEN_WIDTH/2), int(self.SCREEN_HEIGHT/2 + 200)), 2, (255, 255, 255), 2)

        self.display_windows(frame, ref_frame)

<<<<<<< HEAD
    def update_frame(self):
        frame = self.get_frame()
        cv2.imshow("frame: " + str(self.input_path), frame)

        ref_frame = self.get_frame()
<<<<<<< HEAD
<<<<<<< HEAD
        cv2.circle(frame, (320, 240), 2, (255,255,255), 2)
        cv2.circle(frame, (320, 400), 2, (255,255,255), 2)
        cv2.imshow("ref: " + str(self.input_path), frame)

    def capture(self):
        filename = "test_photos/" + str(self.angle) + "_degrees" + str(self.distance) + "inches.png"
=======
        cv2.circle(frame, (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT - 20), 2, (255,255,255), 2)
        cv2.circle(frame, (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2), 2, (255,255,255), 2)
=======
        cv2.circle(frame, (320, 240), 2, (255,255,255), 2)
        cv2.circle(frame, (320, 400), 2, (255,255,255), 2)
>>>>>>> Manually set frame dimensions and add test images
        cv2.imshow("ref: " + str(self.input_path), frame)

    def capture(self):
<<<<<<< HEAD
        filename = "test_photos/" + str(self.angle) + "degrees" + str(self.distance) + "inches.png"
>>>>>>> Add test images
=======
        filename = "test_photos/" + str(self.angle) + "_degrees" + str(self.distance) + "inches.png"
>>>>>>> Add underscore in file name
        cv2.imwrite(filename, self.get_frame())

    def prompt(self):
        print("Capture another image! yay")
        self.angle = input("Angle: ")
        self.distance = input("Distance: ")
<<<<<<< HEAD
=======
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

	def capture(self):
		filename = "test_photos/" + self.angle + "degrees" + self.distance + "inches.png"
		cv2.imwrite(filename, self.get_frame())

	def prompt(self):
		print("Capture another image! yay")
		self.angle = input("Angle: ")
		self.distance = input("Distance: ")
>>>>>>> Add code to capture images
=======
>>>>>>> Add test images
=======
    def capture(self, dir_name, angle, distance):
        filename = dir_name + "/" + str(angle) + "degrees_" + str(distance) + "inches.png"
        frame, _ = self.generator.generate()
        cv2.imwrite(filename, frame)
>>>>>>> Integrate capture code with Generator and Detector classes
