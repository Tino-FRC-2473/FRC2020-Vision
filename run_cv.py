#!/usr/bin/env python3
import argparse
import cv2
from pose_detector import PoseDetector
# from depth_data_generator import DepthDataGenerator
# from depth_live_generator import DepthLiveGenerator
from image_generator import ImageGenerator
from video_file_generator import VideoFileGenerator
from video_live_generator import VideoLiveGenerator
from target_detector import TargetDetector

# "python test.py 0" to run from camera in port 0
# "python test.py video.mp4" to run from the video recording video.mp4

parser = argparse.ArgumentParser()
parser.add_argument("generator", help="read from the given input type", choices=["depth_data", "depth_live", "image", "video_live", "video_file"])
parser.add_argument("--destination", "--dest", nargs="?", help="path of the file to save the results to")
parser.add_argument("--depth", "-d", nargs="?", help="path of the CSV file to read")
parser.add_argument("--image", "-i", nargs="?", help="path of the image file to read")
parser.add_argument("--video", "-v", nargs="?", help="path of the video file to read")
parser.add_argument("--port", "-p", nargs="?", help="camera port to read from")
parser.add_argument("target", help="target to detect pose for", choices=["loading_bay", "power_port"])
args = parser.parse_args()

generator = None
wait_time = 0  # wait time of 0 will wait indefinitely for next key press

if args.generator == "depth_data":
    generator = DepthDataGenerator(args.depth, args.image)
elif args.generator == "depth_live":
    generator = DepthLiveGenerator(args.port)
    wait_time = 3
elif args.generator == "image":
    generator = ImageGenerator(args.image)
elif args.generator == "video_live":
    generator = VideoLiveGenerator(args.port)
    wait_time = 3
elif args.generator == "video_file":
    generator = VideoFileGenerator(args.video)

target_detector = TargetDetector(generator)
pd = PoseDetector(target_detector, args.target)

with pd as p:
    while True:
        p.get_values()
        key = cv2.waitKey(wait_time)
        if key == ord('q'):
            break
