import exifread
'''Uses exifread package (install using "sudo pip install exifread")'''

f = open("../rawimages/HDRset_1/_DSC1718.ARW.tiff",
'rb')
tags = exifread.process_file(f, details=False)

f.close()

#Only output exif tags
for tag in tags.keys():
	if 'EXIF' in tag:
		print "%s: %s" %(tag, tags[tag])

#Output specific values
fnumber = tags["EXIF FNumber"]
exposureTime = tags["EXIF ExposureTime"]
focalLength = tags["EXIF FocalLength"]
ISOspeed = tags["EXIF ISOSpeedRatings"]

print fnumber, exposureTime, focalLength, ISOspeed

'''
Documentation for @ https://pypi.python.org/pypi/ExifRead

Example: processing tags

-Code
for tag in tags.keys():
	#omit some tags that tend to be too long or boring
    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        print "Key: %s, value %s" % (tag, tags[tag])

-Output
Key: Image PhotometricInterpretation, value 2
Key: Image ExifOffset, value 294
Key: Image RowsPerStrip, value 4024
Key: Image DateTime, value 2017:07:14 10:46:23
Key: Image Software, value dcraw v9.26
Key: Image SubfileType, value Full-resolution Image
Key: Image Model, value ILCE-6500
Key: EXIF FNumber, value 2
Key: Image StripOffsets, value 1852
Key: Image ResolutionUnit, value Pixels/Inch
Key: Image Compression, value Uncompressed
Key: Image ImageLength, value 4024
Key: EXIF ExposureTime, value 1/160
Key: Image InterColorProfile, value [0, 0, 1, 220, 0, 0, 0, 0, 2, 16, 0, 0, 109, 110, 116, 114, 82, 71, 66, 32, ... ]
Key: Image ImageWidth, value 6024
Key: Image Artist, value 
Key: Image PlanarConfiguration, value 1
Key: Image ImageDescription, value                                
Key: EXIF FocalLength, value 24
Key: Image StripByteCounts, value 145443456
Key: Image BitsPerSample, value [16, 16, 16]
Key: Image XResolution, value 300
Key: Image Make, value Sony
Key: EXIF ISOSpeedRatings, value 1600
Key: Image YResolution, value 300
Key: Image SamplesPerPixel, value 3

'''