import cv2
import numpy as np 
import matplotlib.pyplot as plt


'''first test with 8 bit per channel images, then try doing the same in 16 bit per channel'''

img1 = cv2.imread("../rawimages/HDRset_2/_DSC1714.ARW.tiff", cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
img2 = cv2.imread("../rawimages/HDRset_2/_DSC1715.ARW.tiff", cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

print img1.dtype
print img2.dtype


img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

#convert to floating point (16 bit not properly implemented in pyplot)
img1 = img1 / 65535.0
img2 = img2 / 65535.0

fig = plt.figure(figsize=(16,8), tight_layout = True)
fig.canvas.set_window_title("HDR Merge")
a=fig.add_subplot(1,2,1)
plt.imshow(img1)
a.set_title('Underexposed')
a=fig.add_subplot(1,2,2)
plt.imshow(img2)
a.set_title('Overexposed')
plt.show()




