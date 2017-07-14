import cv2
import numpy as np 
import matplotlib.pyplot as plt


'''first test with 8 bit per channel images, then try doing the same in 16 bit per channel'''

img1 = cv2.imread("../rawimages/HDRset_2/_DSC1714.ARW.tiff", cv2.IMREAD_ANYCOLOR)
img2 = cv2.imread("../rawimages/HDRset_2/_DSC1715.ARW.tiff", cv2.IMREAD_ANYCOLOR)

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

print gray1.dtype
print gray2.dtype


'''
#OpenCV histograms -- faster, only supports floating point or uint8
cv2.calcHist([gray1], [0], None, [256], [0,256])
#Numpy histograms 
hist, bins = np.histogram(gray1.ravel(), 256, [0,256])
'''


#Matplot plotting histograms
fig = plt.figure(figsize=(12,8), tight_layout = True)
fig.canvas.set_window_title("Histograms")
a=fig.add_subplot(2,2,1)
plt.imshow(gray1, cmap="gray")
a.set_title('Underexposed')
a=fig.add_subplot(2,2,2)
plt.imshow(gray2, cmap="gray")
a.set_title('Overexposed')
a=fig.add_subplot(2,2,3)
plt.hist(gray1.ravel(), 256, [0, 256])
a=fig.add_subplot(2,2,4)
plt.hist(gray2.ravel(), 256, [0, 256])
plt.show()





