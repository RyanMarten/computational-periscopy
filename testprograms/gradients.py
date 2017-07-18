import numpy as np 
import cv2
import argparse

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to image")
ap.add_argument("-s", "--shrink", action="store_true")

args = vars(ap.parse_args())	

#load the image and convert to gray scal
img = cv2.imread(args["image"])
if args["shrink"]:
	img = cv2.resize(img, (0,0), fx=.25, fy=.25)
blur = cv2.GaussianBlur(img, (5,5), 0)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)


laplacian = cv2.Laplacian(gray, cv2.CV_64F)
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)

cv2.imshow("gradients", np.hstack([laplacian, sobelx, sobely, sobel]))
cv2.waitKey(0)