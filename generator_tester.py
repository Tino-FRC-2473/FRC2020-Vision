import argparse
import numpy as np
import time
from depth_data_generator import DepthDataGenerator
from depth_live_generator import DepthLiveGenerator
from image_generator import ImageGenerator
from video_live_generator import VideoLiveGenerator
from video_file_generator import VideoFileGenerator


parser = argparse.ArgumentParser()
parser.add_argument("generator", help="which of the generator classes to test")
parser.add_argument("-destination", nargs="?", help="path of the file to save the results to")
parser.add_argument("-depth", nargs="?", help="path of the CSV file to read")
parser.add_argument("-image", nargs="?", help="path of the image file to read")
parser.add_argument("-video", nargs="?", help="path of the video file to read")
args = parser.parse_args()

if args.generator == "DepthDataGenerator":
    depth_data_generator = DepthDataGenerator(args.depth, args.image)
    rgb, depth = depth_data_generator.generate()
    np.savetxt(args.destination, depth, delimiter=",", fmt="%s")

elif args.generator == "DepthLiveGenerator":
    depth_live_generator = DepthLiveGenerator(1)
    print("The tester will collect data after five seconds")
    time.sleep(5)
    rgb, depth = depth_live_generator.generate()
    np.savetxt(args.destination, depth, delimiter=",", fmt="%s")

elif args.generator == "ImageGenerator":
    image_generator = ImageGenerator(args.image)
    rgb, depth = image_generator.generate()
    print(rgb.shape)

elif args.generator == "VideoLiveGenerator":
    video_live_generator = VideoLiveGenerator(1)
    rgb, depth = video_live_generator.generate()
    print(rgb.shape)

elif args.generator == "VideoFileGenerator":
    video_file_generator = VideoFileGenerator(args.video)
    rgb, depth = video_file_generator.generate()
    print(rgb.shape)
