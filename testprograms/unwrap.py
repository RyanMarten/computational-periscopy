import numpy as np 
import cv2
import argparse

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
ap.add_argument("-s", "--shrink", action=
	"store_true")
args = vars(ap.parse_args())

#load the image, optional resize, and clone it for output 
img = cv2.imread(args['image'], cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
if args["shrink"]:
	img = cv2.resize(img, (0,0), fx=.25, fy=.25)
	print "Resized image to %d x %d" %(img.shape[0], img.shape[1])
output = img.copy()

#guassian blur for better circle detection -- reduces noise to avoid false circle detection
blur = cv2.GaussianBlur(img, (5,5), 0)

#convert to grayscale - increase contrast
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

#The CHT algorithm only takes 8-bit images as input, need to convert if the image is in 16bit
if(gray.dtype == "uint16"):
	gray = (gray/256).astype('uint8')


#detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 300, param1=40, param2=50, minRadius=10, maxRadius=0)
#use canny.py to test param1 values

def unwrap(img, dstheight, dstwidth, interpolationMode):
	srcheight = img.shape[0]
	srcwidth = img.shape[1]

	i, j = np.meshgrid(range(dstwidth), range(dstheight))
	i = i.astype(np.float32)
	j = j.astype(np.float32)
	#scales i,j from integer pixel positions (dst) to float values [-1, 1]
	scaledi = (i*2/dstwidth - 1) * np.pi/2
	scaledj = (j*2/dstheight - 1) * np.pi/2

	#x = np.sin(np.pi/2 - scaledj) * np.cos(scaledi)
	y = np.sin(np.pi/2 - scaledj) * np.sin(scaledi)
	z = np.cos(np.pi/2 - scaledj)

	#scales z and y from float values [-1, 1] to float value pixel positions (src)
	map_x = (y + 1)*srcwidth/2
	map_y = (z + 1)*srcheight/2

	unwrapped = cv2.remap(img, map_x, map_y, interpolationMode)
	return unwrapped


#make sure some circles are found
if circles is not None:
	#convert the (x,y) coordinates and radius of the circles to integers
	circles = np.round(circles[0,:]).astype('int')

	#store cirlce params
	x = circles[0][0]
	y = circles[0][1]
	r = circles[0][2]

	print "Circle found at (%d, %d) with raidus %d" %(x, y, r)

	#create an all black mask the size of the image
	mask = np.zeros(img.shape, dtype=img.dtype)

	if(img.dtype == "uint16"):
		#add a white mask where the circle was detected
		cv2.circle(mask, (x, y), r, (65535, 65535, 65535), -1)
	else:
		#add a white mask where the circle was detected
		cv2.circle(mask, (x, y), r, (255, 255, 255), -1)

	#apply mask 
	masked = cv2.bitwise_and(img, mask)

	#crop image to be centered around the sphere
	crop = masked[y - r: y + r, x - r: x + r, :]

	#unwrapp the image to equirectagular (with a width twice as large)
	unwrapped = unwrap(crop, crop.shape[0], 2*crop.shape[1], cv2.INTER_LINEAR)
	
	cv2.imshow("Original", img)
	cv2.imshow("Cropped", crop)
	cv2.imshow("Unwrapped", unwrapped)
	cv2.waitKey(0)

else:
	print "No circles found"