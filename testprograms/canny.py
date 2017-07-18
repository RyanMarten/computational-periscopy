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
img = cv2.imread(args['image'], cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
if args["shrink"]:
	img = cv2.resize(img, (0,0), fx=.25, fy=.25)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



#The canney algorithm only takes 8-bit images as input, need to convert if the image is in 16bit
if(gray.dtype == "uint16"):
	gray = (gray/256).astype('uint8')


edges = cv2.Canny(gray, 10, 20)
#adjust low and high hysteresis threshold - to test out what CHT will do (canny computerphile vid)


plt.imshow(cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))
plt.show()

'''
cv2.imshow("canny", np.hstack([gray, edges]))
cv2.waitKey(0)
'''