import os
from PIL import Image
import argparse
parser=argparse.ArgumentParser(description="Delete invalid dimension images".format(os.linesep))
parser.add_argument("path", type=str)

args = parser.parse_args()
path = args.path

def bad_dimension(imgPath):
	img=Image.open(imgPath)
	w,h=img.size
	if w < 10 or h < 10:
		return True
	else:
		return False

with os.scandir(path) as dir:
	for file in dir:
		if bad_dimension(file.path):
			os.remove(file.path)
