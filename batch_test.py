import os
import csv
import cv2
import argparse
from cv import PoseDetector
from pathlib import Path

# take in an argument to specify either loading bay or power port
parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory with test photos")
parser.add_argument("target", help="target to detect pose for", choices=["loading_bay", "power_port"])
args = parser.parse_args()

with open('vision_output.csv', mode='w', newline='') as output_file:
	output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	sorted_photos = sorted(os.listdir(args.dir)
	output_writer.writerow(["filename", "distance", "angle", "rx", "ry", "rz", "tx", "ty", "tz"])

	for filename in sorted_photos:
		print(filename)
		with PoseDetector(args.dir + "/" + filename, args.target) as pd:
			r,t = pd.get_values(display=False)
			# example filename: 0degrees_18inches.png
			output_writer.writerow([filename, int(filename[filename.index('_')+1:-10]), int(filename[:filename.index('d')]),
								   r[0], r[1], r[2], t[0], t[1], t[2]])
