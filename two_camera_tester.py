import argparse
import cv2
from two_camera_setup import TwoCameraSetup


parser = argparse.ArgumentParser()
parser.add_argument("input_first", help="read from the given camera port as the first camera", default="0")
parser.add_argument("input_second", help="read from the given camera port as the second camera", default="1")
args = parser.parse_args()

setup = TwoCameraSetup(args.input_first, args.input_second)

while True:
    setup.run_cv()
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
