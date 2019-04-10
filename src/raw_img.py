# Library Import
import cv2
import numpy as np
import argparse
import os
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--w", metavar="WIDTH", default=300, help="Input shape's Width is required", type=int)
parser.add_argument("--h", metavar="HEIGHT", default=300, help="Input shape's Height is required", type=int)
parser.add_argument("--c", metavar="CHANNEL", default=3, help="Input shape's Channel is required", type=int)
parser.add_argument("--img_dir", metavar="Image Directory Path", help="Give image directory name, make sure that all file are having .jpg extention", required=True, type=str)

args = parser.parse_args()

# To convert the all the .jpg images to raw images 
class RawConvert:
	def __init__(self):
		self.img_dir = args.img_dir
		if(os.path.isdir(self.img_dir + '/raw_files') == False):
			os.mkdir(os.path.join(self.img_dir, 'raw_files'))
		self.channel = args.c
		self.input_shape = (args.w, args.h)

	def convert_to_raw(self):
		list_files = glob.glob(os.path.join(os.getcwd(), self.img_dir) + "/*.jpg")
		done = 0
		i = 0
		for f in list_files:
			print(f)
			if self.channel == 1:
				img = cv2.imread(str(f), 0)
			else:
				img = cv2.imread(f)
			i += 1
			img = cv2.resize(img, self.input_shape)
			img_arr = np.array(img)
			img_arr.tofile(os.path.join(os.getcwd(), self.img_dir, 'raw_files/')+str(i)+'.raw')
			# for image reference in raw_files folder can uncommnet below code
			#cv2.imwrite(os.path.join(os.getcwd(), self.img_dir, 'raw_files/')+str(i)+'.jpg', img)
			done = 1
		if done == 1:
			print ("Output raw generated in "+os.path.join(os.getcwd(), self.img_dir, 'raw_files'))


if __name__ == '__main__':
	convert_img = RawConvert()
	convert_img.convert_to_raw()
