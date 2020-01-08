import math
import cv2
import numpy as np
import subprocess
import imghdr
import random

# finds angle between robot's heading and the perpendicular to the targets
class VisionTargetDetector:

	# initilaze variables
	def __init__(self, input):

		self.input_path = input
		

		try:
			# if input is a camera port
			self.input = cv2.VideoCapture(int(input))
			self.set_camera_settings(input)
		except:
			# if input is a path
			self.input = cv2.VideoCapture(input)

		frame = self.get_frame()

		# intialize screen width and screen height
		self.SCREEN_HEIGHT, self.SCREEN_WIDTH = frame.shape[:2]

		# intialize angle of field of view in radians
		self.FIELD_OF_VIEW_RAD = 70.42 * math.pi / 180.0

		# calculates focal length based on a right triangle representing the "image" side of a pinhole camera
		# ABC where A is FIELD_OF_VIEW_RAD/2, a is SCREEN_WIDTH/2, and b is the focal length
		self.FOCAL_LENGTH_PIXELS = (self.SCREEN_WIDTH / 2.0) / math.tan(self.FIELD_OF_VIEW_RAD / 2.0)

		rgb_data = np.loadtxt('green_data.csv', dtype=np.uint8, delimiter=',')
		bgr_data = np.copy(rgb_data)
		bgr_data[:, 0] = rgb_data[:, 2]
		bgr_data[:, 2] = rgb_data[:, 0]

		bgr_data = np.reshape(bgr_data, (79, 1, 3))

		self.TRUE_GREEN_VALS = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2HSV)

		self.LOW_GREEN = np.array([68, 100, 10])
		self.HIGH_GREEN = np.array([84, 255, 255])

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

	def get_euler_from_rodrigues(self, rmat):
		sin = math.sqrt(rmat[2][0] * rmat[2][0] + rmat[2][1] * rmat[2][1])
		if sin >= 1e-6:
			z1 = math.atan2(rmat[2][0], rmat[2][1])  # around z1-axis
			x = math.atan2(sin, rmat[2][2])  # around x-axis
			z2 = math.atan2(rmat[0][2], -rmat[1][2])  # around z2-axis
		else:  # gimbal lock
			z1 = 0  # around z1-axis
			x = math.atan2(sin, rmat[2][2])  # around x-axis
			z2 = 0  # around z2-axis

		euler = np.array([[z1], [x], [z2]])

		euler_deg = -180 * euler / math.pi
		# euler_deg[0][0] = (360 - euler_deg[0][0])%360
		euler_deg[1][0] = euler_deg[1][0]

		return euler_deg[0][0], euler_deg[1][0], euler_deg[2][0]

	def get_new_hsv(self, res):
		if (len(res) == 0):
			return self.LOW_GREEN, self.HIGH_GREEN
		for i in range(100):
			row = random.randrange(0, len(res))
			self.TRUE_GREEN_VALS = np.append(self.TRUE_GREEN_VALS, np.reshape(np.array(res[row]), (1, 1, 3)), 0)

		h = self.TRUE_GREEN_VALS[:, :, 0]
		s = self.TRUE_GREEN_VALS[:, :, 1]
		v = self.TRUE_GREEN_VALS[:, :, 2]

		low_h, low_s, low_v = (h.mean() - 3.25 * h.std()), (s.mean() - 3.5 * s.std()), (v.mean() - 3.25 * v.std())
		high_h, high_s, high_v = (h.mean() + 3.25 * h.std()), (s.mean() + 3.5 * s.std()), (v.mean() + 3.25 * v.std())

		return np.array([int(low_h), int(low_s), int(low_v)]), np.array([int(high_h), int(high_s), int(high_v)])

	def get_angle_dist(self, target):

		obj_points = [[ 0.0,                      0, 0],
					  [ 19.625,                   0, 0],
					  [ 19.625 - 4/math.sqrt(3),  0, 0],
					  [ 9.8125 - 2/math.sqrt(3), 15, 0],
					  [-9.8125 + 2/math.sqrt(3), 15, 0],
					  [-19.625 + 4/math.sqrt(3),  0, 0],
					  [-19.625,                   0, 0],
					  [-9.8125,                  17, 0],
					  [ 9.8125,                  17, 0]]

		mx = sum(p[0][0] for p in target) / 8
		my = sum(p[0][1] for p in target) / 8

		img_points = []
		img_points.append([0,0])

		for p in target:
			img_points.append([p[0][0] - mx, p[0][1] - my])

		frame = self.get_frame()

		obj_points = np.float64(obj_points)
		img_points = np.float64(img_points)

		print("object", obj_points)
		print("image", img_points)
		#Camera matrix
		camera_matrix = np.float64([[self.FOCAL_LENGTH_PIXELS, 0,                        self.SCREEN_WIDTH/2],
								    [0,                        self.FOCAL_LENGTH_PIXELS, self.SCREEN_HEIGHT/2],
								    [0,                        0,                        1]])

		#Returning solvePnP which returns the rotation vector and translation vector
		bool, rvec, tvec = cv2.solvePnP(obj_points, img_points, camera_matrix, None)
		return rvec, tvec, np.float64(obj_points)

	def run_cv(self):

		frame = self.get_frame()

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# isolate the desired shades of green
		mask = cv2.inRange(hsv, self.LOW_GREEN, self.HIGH_GREEN)
		contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		greens = hsv[np.where((mask == 255))]

		self.LOW_GREEN, self.HIGH_GREEN = self.get_new_hsv(greens)

		if len(contours) < 1:
			return [360, 360, 360], -1

		target = max(contours, key=lambda c: cv2.contourArea(c))
		if cv2.contourArea(target) < 100:
			return [360, 360, 360], -1

		epsilon = 0.005*cv2.arcLength(target,True)
		approx = cv2.approxPolyDP(target,epsilon,True)

		cv2.drawContours(frame, approx, -1, (0,0,255), 6)

		# r, t, o = self.get_angle_dist(approx)
		# rmat, _ = cv2.Rodrigues(r)
		#
		# yaw, pitch, roll = self.get_euler_from_rodrigues(rmat)
		#
		# font = cv2.FONT_HERSHEY_SIMPLEX
		# cv2.putText(frame, "Yaw: " + str(round(yaw,2)), (20, self.SCREEN_HEIGHT - 90), font, 1, (255,255,255), 2, cv2.LINE_AA)
		# cv2.putText(frame, "Pitch: " + str(round(pitch,2)), (20, self.SCREEN_HEIGHT - 60), font, 1, (255,255,255), 2, cv2.LINE_AA)
		# cv2.putText(frame, "Roll: " + str(round(roll,2)), (20, self.SCREEN_HEIGHT - 30), font, 1, (255,255,255), 2, cv2.LINE_AA)

		# show windows
		cv2.imshow("contours: " + str(self.input_path), mask)
		cv2.imshow("frame: " + str(self.input_path), frame)
		print("hello")
		# return [yaw, pitch, roll], t

# this class defines a point
class Point:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def get_coordinate(self):
		return [self.x, self.y]
