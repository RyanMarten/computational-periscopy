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
img = cv2.imread(args['image'])
if args["shrink"]:
	img = cv2.resize(img, (0,0), fx=.25, fy=.25)
output = img.copy()

print "Image size is %d x %d" %(img.shape[0], img.shape[1])

#guassian blur for better detection -- reduces noise to avoid false circle detection
blur = cv2.GaussianBlur(img, (5,5), 0)

#convert to grayscale - increase contrast
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

#detect circles in the image
circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 300, param1=200, param2=50, minRadius=10, maxRadius=0)

#create an all black mask the size of the image
mask = np.zeros(img.shape, dtype=np.uint8)


#make sure some circles are found
if circles is not None:
	#convert the (x,y) coordinates and radius of the circles to integers
	circles = np.round(circles[0,:]).astype('int')

	#store cirlce params
	x = circles[0][0]
	y = circles[0][1]
	r = circles[0][2]

	print "Circle found at (%d, %d) with raidus %d" %(x, y, r)

	#add a white mask where the circle was detected
	cv2.circle(mask, (x, y), r, (255, 255, 255), -1)

	#apply mask 
	masked = cv2.bitwise_and(img, mask)

	#show the output image
	cv2.imshow("Masked", np.hstack([img, masked]))
	
	#crop/center
	crop = masked[y - r: y + r, x - r: x + r, :]
	cv2.imshow("Cropped", crop)
	

	#rest of image
	invMask = 255 - mask
	restOfImage = cv2.bitwise_and(img, invMask)

	cv2.imshow("Rest of Image", restOfImage)
	cv2.waitKey(0)


else:
	print "No circles found"