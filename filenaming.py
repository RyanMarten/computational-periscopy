import os

def getBaseName(fp):
	return os.path.basename(fp)

def getDirName(fp):
	return os.path.dirname(fp)

def getBaseNameNoExt(fp):
	name = getBaseName(fp)
	return name[0:name.index(".")]

def getNumberSuffix(fp):
	name = getBaseNameNoExt(fp)
	pos = len(name) - 1
	while (pos >= 0 and name[pos] >= '0' and name[pos] <= '9'):
		pos -= 1
	return name[pos+1:]

def getOutputName(hdrset):
	hdrset.sort()
	name = getBaseNameNoExt(hdrset[0]) 
	for i in range(1,len(hdrset)-1):
		name += "-" + getNumberSuffix(hdrset[i])
	return name

def getOutputPath(hdrset):
	return getDirName(hdrset[0])

if __name__ == "__main__":
	hdrset = ['../rawimages/HDRset_1/_DSC1718.ARW', 
			  '../rawimages/HDRset_1/_DSC1720.ARW', 
			  '../rawimages/HDRset_1/_DSC1719.ARW', 
			  '../rawimages/HDRset_1/_DSC1721.ARW',
			  '../rawimages/HDRset_1/_DSC1724.ARW', 
			  '../rawimages/HDRset_1/_DSC1722.ARW', 
			  '../rawimages/HDRset_1/_DSC1723.ARW']
	for img in hdrset:
		print getDirName(img)
		print getBaseName(img)
		print getBaseNameNoExt(img)
		print getNumberSuffix(img)
	print getOutputName(hdrset)
