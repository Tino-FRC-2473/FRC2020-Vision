import argparse
import cv2
from capture_image import ImageCapture

# "python test.py 0" to run from camera in port 0
# "python test.py video.mp4" to run from the video recording video.mp4

parser = argparse.ArgumentParser()
parser.add_argument("input", help="read from the given camera or file", default="0")
parser.add_argument("angle", help="angle of capture", default="0")
parser.add_argument("distance", help="distance of capture", default="60")
args = parser.parse_args()

print("reading from", args.input)
print("angle:", args.angle)
print("distance:", args.distance)

capture = ImageCapture(args.input, args.angle, args.distance)
wait_time = 0 # wait time of 0 will wait indefinitely for next key press

# if input is from a camera, set wait time to 3 ms
if len(args.input) == 1:
	wait_time = 3

with capture as c:
	while True:
		c.update_frame()
		key = cv2.waitKey(wait_time)
		if key == ord('q'):
			break
		if key == ord('c'):
			c.capture()
			c.prompt()
