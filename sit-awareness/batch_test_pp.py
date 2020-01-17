import os
import csv
import cv2
from cv_power_port import VisionTargetDetector

with open('vision_output.csv', mode='w', newline='') as output_file:
	output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	sorted_photos = sorted(os.listdir('test_photos_pp'))
	output_writer.writerow(["filename", "distance", "angle", "rx", "ry", "rz", "tx", "ty", "tz"])
	#for every filename
	for filename in sorted_photos:
		vtd = VisionTargetDetector('test_photos_pp/' + filename)
		print(filename)
		with vtd as v:
			r,t = v.run_cv(display=False)
			output_writer.writerow([filename, int(filename[filename.index('_')+1:-10]), int(filename[:filename.index('d')]),
								   r[0], r[1], r[2], t[0], t[1], t[2]])
