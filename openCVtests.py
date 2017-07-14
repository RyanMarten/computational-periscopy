import numpy as np
import cv2
from matplotlib import pyplot as plt

#reading an image
img = cv2.imread('../rawimages/_DSC1641.ARW.tiff', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
print img.dtype #should be uint16 - 16 bits per color channel for HDR later

#displaying an image
''' 
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

#writing to an image
'''cv2.imwrite('testimages/opencvwritetest.tiff', img)'''

#displaying an image using matplotlib
img2 = cv2.imread('testimages/redpanda.jpg')

'''OpenCV using BGR order and matplotlib uses RGB, so it needs to be converted'''
b, g, r = cv2.split(img2)
img3 = cv2.merge([r,g,b])
#can also do img3 = img2[:,:,::-1]
plt.imshow(np.hstack([img3, img2]))
#removes tick marks
plt.xticks([]), plt.yticks([]) 
plt.show()