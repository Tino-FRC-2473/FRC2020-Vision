import imghdr
import cv2
import numpy as np

class imageGenerator:

	# initilaze variables
	def __init__(self, input):
		self.input_path = input
		frame = self.generate()

	def generate(self):
		frame = None

		if imghdr.what(self.input_path) is not None:
			frame = cv2.imread(self.input_path)

		return (cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),None)
