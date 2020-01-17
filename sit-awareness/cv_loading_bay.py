import math
import cv2
import numpy as np
import subprocess
import imghdr
import traceback
import os
from math import sin, cos

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
		roll = 180*math.atan2(-rmat[2][1], rmat[2][2])/math.pi
		pitch = 180*math.asin(rmat[2][0])/math.pi
		yaw = 180*math.atan2(-rmat[1][0], rmat[0][0])/math.pi
		return yaw, pitch, roll

		# sin = math.sqrt(rmat[2][0] * rmat[2][0] + rmat[2][1] * rmat[2][1])
		# if sin >= 1e-6:
		#     z1 = math.atan2(rmat[2][0], rmat[2][1])  # around z1-axis
		#     x = math.atan2(sin, rmat[2][2])  # around x-axis
		#     z2 = math.atan2(rmat[0][2], -rmat[1][2])  # around z2-axis
		# else:  # gimbal lock
		#     z1 = 0  # around z1-axis
		#     x = math.atan2(sin, rmat[2][2])  # around x-axis
		#     z2 = 0  # around z2-axis
		#
		# euler = np.array([[z1], [x], [z2]])
		#
		# euler_deg = -180 * euler / math.pi
		# # euler_deg[0][0] = (360 - euler_deg[0][0])%360
		# euler_deg[1][0] = euler_deg[1][0]
		#
		# return euler_deg[0][0], euler_deg[1][0], euler_deg[2][0]

	def get_angle_dist(self, rectangles):

		# obj_points = [[ 0.0,  0.0, 0],
		# 			  [ 3.5,  5.5, 0],
		# 			  [-3.5,  5.5, 0],
		# 			  [-3.5, -5.5, 0],
		# 			  [ 3.5, -5.5, 0],
		# 			  [ 1.5,  3.5, 0],
		# 			  [-1.5,  3.5, 0],
		# 			  [-1.5, -3.5, 0],
		# 			  [ 1.5, -3.5, 0]]

		obj_points = [[ 320.0,  0.0, 0],
					  [ 390,  350, 0],
					  [ 250,  350, 0],
					  [ 250,  130, 0],
					  [ 390,  130, 0],
					  [ 350,  310, 0],
					  [ 290,  310, 0],
					  [ 290,  170, 0],
					  [ 350,  170, 0]]

		mx = rectangles[0].get_center().x
		my = rectangles[0].get_center().y

		img_points = []
		img_points.append([0,0])

		for r in rectangles:
			for p in r.get_points():
				img_points.append([p.x - mx, p.y - my])
				# img_points.append([p.x, p.y])

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

	def get_corners(self, contour):

		hull = cv2.convexHull(contour)
		hull_changed = []
		for i in range(len(hull)):
			hull_changed.append([hull[i][0][0], hull[i][0][1]])

		max = 0
		max_arr = []
		for i in range(len(hull_changed)):
			for j in range(i):
				for k in range(j):
					for m in range(k):
						total = 0
						total += math.hypot(hull_changed[i][0]-hull_changed[j][0],hull_changed[i][1]-hull_changed[j][1])
						total += math.hypot(hull_changed[j][0]-hull_changed[k][0],hull_changed[j][1]-hull_changed[k][1])
						total += math.hypot(hull_changed[k][0]-hull_changed[m][0],hull_changed[k][1]-hull_changed[m][1])
						total += math.hypot(hull_changed[m][0]-hull_changed[i][0],hull_changed[m][1]-hull_changed[i][1])
						if(total>max):
							max = total
							max_arr = [hull_changed[i],hull_changed[j],hull_changed[k],hull_changed[m]]

		arrmax_changed = []
		for i in range(len(max_arr)):
			arrmax_changed.append([max_arr[i]])
		return np.int0(arrmax_changed)

	def run_cv(self):

		frame = self.get_frame()

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		low_green = np.array([65,145,65])
		high_green= np.array([87,255,229])

		# isolate the desired shades of green
		mask = cv2.inRange(hsv, low_green, high_green)
		_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

		if len(contours) < 2:
			return [360, 360, 360], -1

		rectangles = []
		for i in range(2):
			c = contours[i]
			if cv2.contourArea(c) < 100:
				return [360, 360, 360], -1

			area = cv2.contourArea(c)
			corners = self.get_corners(c)
			rectangles.append(Rectangle(corners, area))
			cv2.drawContours(frame, corners, -1, (0,0,255), 6)

		r, t, o = self.get_angle_dist(rectangles)
		rmat, _ = cv2.Rodrigues(r)

		yaw, pitch, roll = self.get_euler_from_rodrigues(rmat)

		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame, "Yaw: " + str(round(yaw,2)), (20, self.SCREEN_HEIGHT - 90), font, 1, (255,255,255), 2, cv2.LINE_AA)
		cv2.putText(frame, "Pitch: " + str(round(pitch,2)), (20, self.SCREEN_HEIGHT - 60), font, 1, (255,255,255), 2, cv2.LINE_AA)
		cv2.putText(frame, "Roll: " + str(round(roll,2)), (20, self.SCREEN_HEIGHT - 30), font, 1, (255,255,255), 2, cv2.LINE_AA)

		# show windows
		cv2.imshow("contours: " + str(self.input_path), mask)
		cv2.imshow("frame: " + str(self.input_path), frame)

		return [yaw, pitch, roll], t

class Rectangle:

	def __init__(self, box, area):
		self.box = box
		self.area = area
		self.points = []
		for coordinates in box:
			self.points.append(Point(coordinates[0][0], coordinates[0][1]))

	def get_center(self):
		x = sum(point.x for point in self.points) / 4
		y = sum(point.y for point in self.points) / 4
		return Point(x, y)

	def get_points(self):
		points = self.points
		mx, my = self.get_center().x, self.get_center().y

		#sort points clockwise
		def sort_clockwise(p):
			return (math.atan2(p.y - my, p.x - mx) + 2 * math.pi) % (2*math.pi)
		points.sort(key=sort_clockwise)
		return points

# this class defines a point
class Point:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def get_coordinate(self):
		return [self.x, self.y]
