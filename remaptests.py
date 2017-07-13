import numpy as np 
import cv2

'''
remap decides where to map a pixel (i,j) by checking map_x(i,j) and map_y(i,j). 
At the end, your pixel (i,j) is mapped to (map_x(i,j),map_y(i,j))
'''

'''
Pixel maps are not maps from source to destination.
Instead, for each pixel in the destination, we describe which source pixel it comes from. 
Now the source pixel we provide here is a float variable. 
Thus it can lie not directly on a pixel, but rather on a point in-between a few pixels. 
The OpenCV interpolation functions then calculate the destination pixel value using this position information and the surrounding pixel values with the chosen interpolation function.
'''

img = cv2.imread("testimages/uzi.jpg")


imgHeight = img.shape[0]
imgWidth = img.shape[1]

map_x = np.zeros((imgHeight, imgWidth), np.float32)
map_y = np.zeros((imgHeight, imgWidth), np.float32)

for y in range(0, int(imgHeight - 1)):
	for x in range(0, int(imgWidth -1)):
		map_x.itemset((y, x), imgWidth - x)
		map_y.itemset((y, x), y)

flipx = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)

''''for y in range(0, int(imgHeight - 1)):
	for x in range(0, int(imgWidth -1)):
 		map_x.itemset((y, x), x)
		map_y.itemset((y, x), imgHeight - y)

flipy = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)

for y in range(0, int(imgHeight - 1)):
	for x in range(0, int(imgWidth -1)):
 		map_x.itemset((y, x), imgWidth - x)
		map_y.itemset((y, x), imgHeight - y)

flipboth = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)'''

cv2.imshow("Original", img)
cv2.imshow("FlipX", flipx)
# cv2.imshow("FlipY", flipy)
# cv2.imshow("FlipBoth", flipboth)
cv2.waitKey(0)