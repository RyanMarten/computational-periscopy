import cv2
import numpy as np 
import matplotlib.pyplot as plt
import exifread
import math

print cv2.__version__

def cvtTagToFloat(fnumber):
	fnumber = str(fnumber)
	if '/' in fnumber:
		#coverts a string (non mixed) fraction to a float
		num, den = fnumber.split( '/' )
		return (float(num)/float(den))
	else: 
		return float(fnumber)


img_fn = [
	"../rawimages/HDRset_1/_DSC1717.ARW.tiff",
	"../rawimages/HDRset_1/_DSC1718.ARW.tiff",
	"../rawimages/HDRset_1/_DSC1719.ARW.tiff",
	"../rawimages/HDRset_1/_DSC1720.ARW.tiff",
	"../rawimages/HDRset_1/_DSC1721.ARW.tiff",
	"../rawimages/HDRset_1/_DSC1722.ARW.tiff"]
img_list = []
times = []

#create a list of the images and a list of their exposure times
for fn in img_fn:

	#read images
	img_list.append(cv2.imread(fn, cv2.IMREAD_ANYCOLOR))

	#read metadata tags
	f = open(fn, 'rb')
	tags = exifread.process_file(f, details=False)
	f.close()

	#parse metadata tags and store
	fnumber = cvtTagToFloat(tags["EXIF FNumber"])
	exposureTime = cvtTagToFloat(tags["EXIF ExposureTime"])
	focalLength = tags["EXIF FocalLength"]
	ISOspeed = tags["EXIF ISOSpeedRatings"]

	#calculate exposure value
	ev = math.log(fnumber**2/exposureTime, 2)

	#another way of doing it is for every increase of ev by 1, exposuretime doubles
	#so you could do it relatively to each other

	#calculate a exposure time for a standard fnumber of 4
	adjExposureTime = (4.0**2) / (2**ev)
	times.append(adjExposureTime)


exposure_times = np.array(times, dtype=np.float32)
print len(img_list)
print len(exposure_times)

#Merge exposures to HDR image
merge_debvec = cv2.createMergeDebevec()
hdr_debvec = merge_debvec.process(img_list, times=exposure_times.copy())

#Tonemap HDR image
tonemap = cv2.createTonemapDurand(gamma=2.2)
res_debvec = tonemap.process(hdr_debvec.copy())

#Convert to 8-bit and save
res_debvec_8bit = np.clip(res_debvec*255, 0, 255).astype("uint8")

cv2.imwrite("res_debvec_8bit.jpg", res_debvec_8bit)



#!!!!!WARNING, this might not work with images of 16 bit depth - need to test
print "\n-----------------"
print "Images datatype: %s" %(img_list[0].dtype)
print "-----------------\n"

plt.imshow(cv2.cvtColor(res_debvec_8bit, cv2.COLOR_BGR2RGB))
plt.show()

'''
#for 16bit images
def makePlotable(img):
	#openCV in is BGR and pyplot uses RGB
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	#convert to floating point (16 bit not properly implemented in pyplot)
	img = img / 65535.0
	return img


#plot all the images to be merged
fig = plt.figure(figsize=(13,13),tight_layout = True)
fig.canvas.set_window_title("HDR Merge")
plots = len(img_list)
rows = 1 + plots/3
cols = 3
for i in range(0, plots):
	a=fig.add_subplot(rows, cols, i + 1)
	plt.imshow(makePlotable(img_list[i]))
plt.show()	
'''



