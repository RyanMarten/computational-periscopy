import numpy as np 
import cv2

#example input (This one happens to be 420 by 420)
img = cv2.imread("testimages/cropped.jpg")

cv2.imshow("Image", img)


#I arbitrarily picked the output image to be the same height and twice the width
#I should play around with different dimensions
srcheight = img.shape[0]
srcwidth = img.shape[1]

dstheight = srcheight
dstwidth = srcwidth*2



print "\t dstwidth: %f\n\t dstheight: %f" %(dstwidth, dstheight)
print "\t srcwidth: %f\n\t srcheight: %f" %(srcwidth, srcheight)


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


unwrapped = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)

cv2.imshow("Unwrapped", unwrapped)
cv2.waitKey(0)



'''
Without using meshgrids and vectorized computation


#create a empty maps the size of the desired equirectangular output 
map_x = np.zeros((dstheight, dstwidth), np.float32)
map_y = np.zeros((dstheight, dstwidth), np.float32)

for j in range (0, dstheight - 1):
	for i in range(0, dstwidth -1):

		#scales i,j from integer pixel positions (dst) to float values [-1, 1]
		scaledi = (float(i)*2/dstwidth - 1) * np.pi/2
		scaledj = (float(j)*2/dstheight - 1) * np.pi/2

		#x = np.sin(np.pi/2 - scaledj) * np.cos(scaledi)
		y = np.sin(np.pi/2 - scaledj) * np.sin(scaledi)
		z = np.cos(np.pi/2 - scaledj)

		#scales z and y from float values [-1, 1] to float value pixel positions (src)
		scaledy = (y + 1)*srcwidth/2
		scaledz = (z + 1)*srcheight/2

		map_x.itemset((j,i), scaledy)
		map_y.itemset((j,i), scaledz)

unwrapped = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)

cv2.imshow("Unwrapped", unwrapped)
cv2.waitKey(0)

'''


'''
This just pulls the image to twice its width

for j in range (0, dstheight - 1):
	for i in range(0, dstwidth -1):

		x = i / 2
		y = j

		map_x.itemset((j,i), x)
		map_y.itemset((j,i), y)


unwrapped = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)

cv2.imshow("Unwrapped", unwrapped)
cv2.waitKey(0)
'''