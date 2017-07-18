import numpy as np 
import cv2
import argparse
import matplotlib.pyplot as plt


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
output = img.copy()

#guassian blur for better detection -- reduces noise to avoid false circle detection
blur = cv2.GaussianBlur(img, (5,5), 0)

#convert to grayscale - increase contrast
gray = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY, 3)

#The CHT algorithm only takes 8-bit images as input, need to convert if the image is in 16bit
if(gray.dtype == "uint16"):
	gray = (gray/256).astype('uint8')

#detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 300, param1=40, param2=50, minRadius=10, maxRadius=0)
#1 is dp - the inverse ration of the acculumator resolution to the image resolution (for 1 they are the same)
#300 is the minDist - minimum distance between centers of detected circles
#param1 is the high threshold for the canney() done before CHT, and low is equal to half of param1
#param2 is the accumulator threshold for the circle centers at the detection stage, smaller it is, more false circles 
#may be detected

#cht uses canny, canny uses sobel

#make sure some circles are found
if circles is not None:
	#convert the (x,y) coordinates and radius of the circles to integers
	circles = np.round(circles[0,:]).astype('int')

	#loop over the (x,y) coordinates and radius of the circles
	for(x, y, r) in circles:
		#draw the circle in the output image, then draw a rectangle
		#corresponding to the center of the circle
		cv2.circle(output, (x, y), r, (0, 255, 0), 20)
		cv2.circle(output, (x, y), 50, (0, 128, 255), -1)

	#show the output image
	plt.figure(figsize=(12,4), tight_layout=True)
	plt.subplot(121)
	plt.imshow(cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB))
	#matplotlib doesn't support 16bit, have to convert to floating point output
	output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
	if(output.dtype == "uint16"):
		output = output / 65535.0
	plt.subplot(122)
	plt.imshow(output)
	plt.show()
