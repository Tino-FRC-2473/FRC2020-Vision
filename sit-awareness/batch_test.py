import os
import csv
import cv2
import argparse
from cv import PoseDetector

parser = argparse.ArgumentParser()
parser.add_argument("target", help="target to detect pose for", default="lb")
args = parser.parse_args()

with open('vision_output.csv', mode='w', newline='') as output_file:
	output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	sorted_photos = sorted(os.listdir('test_photos_' + args.target))
	output_writer.writerow(["filename", "distance", "angle", "rx", "ry", "rz", "tx", "ty", "tz"])
	#for every filename
	for filename in sorted_photos:
		pd = PoseDetector('test_photos_' + args.target + '/' + filename, args.target)
		print(filename)
		with pd as p:
			r,t = p.get_values(display=False)
			output_writer.writerow([filename, int(filename[filename.index('_')+1:-10]), int(filename[:filename.index('d')]),
								   r[0], r[1], r[2], t[0], t[1], t[2]])
