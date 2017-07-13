import numpy as np 
import cv2
import argparse
import matplotlib.pyplot as plt

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = "Path to the image")
ap.add_argument("-s", "--shrink", action="store_true")
args = vars(ap.parse_args())

#Load the image and clone it for output
img = cv2.imread(args['image'])
if args["shrink"]:
	img = cv2.resize(img, (0,0), fx=.25, fy=.25)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 100)
#adjust low and high hysteresis threshold - to test out what CHT will do (canny computerphile vid)


plt.figure(1)

'''
plt.subplot(121)
plt.imshow(cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB))
'''


#plt.subplot(122)
plt.imshow(cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))
plt.show()

'''
cv2.imshow("canny", np.hstack([gray, edges]))
cv2.waitKey(0)
'''