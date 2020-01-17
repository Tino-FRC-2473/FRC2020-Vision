import argparse
import numpy as np
import time
from depth_data_generator import DepthDataGenerator
from depth_live_generator import DepthLiveGenerator
from image_generator import ImageGenerator


parser = argparse.ArgumentParser()
parser.add_argument("generator", help="which of the generator classes to test")
parser.add_argument("input_depth", help="path of the CSV file to read from")
parser.add_argument("input_image", help="path of the image file to read from")
parser.add_argument("destination", help="file to save the results to")
args = parser.parse_args()

if args.generator == "DepthDataGenerator":
    depth_data_generator = DepthDataGenerator(args.input_depth, args.input_image)
    _, arr = depth_data_generator.generate()
    np.savetxt(args.destination, arr, delimiter=",", fmt="%s")
elif args.generator == "DepthLiveGenerator":
    depth_live_generator = DepthLiveGenerator(1)
    print("The tester will collect data after five seconds")
    time.sleep(5)
    _, arr = depth_live_generator.generate()
    np.savetxt(args.destination, arr, delimiter=",", fmt="%s")
elif args.generator == "ImageGenerator":
    image_generator = ImageGenerator(args.input_image)
    image, _ = image_generator.generate()
