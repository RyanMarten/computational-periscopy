import argparse
import subprocess
import os
import sys
import time
from generate_spheres import generateSpheres
from filenaming import getOutputName, getOutputPath

def executeCommand(cmd):
	#execute a terminal command as a subprocess
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    #intercept stdout of a subprocess
    for stdout_line in iter(popen.stdout.readline, ""):
    	yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
    	raise subprocess.CalledProcessError(return_code, cmd)

def executeAndPrintCommand(cmd):
	#print subprocess stdout as it happens
	for line in executeCommand(cmd):
		sys.stdout.write(">" + line)
		sys.stdout.flush()
    

def processHDRset(hdrset):
	#configure output filenames and directories
	path = getOutputPath(hdrset)
	fnbase = getOutputName(hdrset)
	fndng = "{}/hdr/{}.dng".format(path, fnbase)
	fntif = "{}/hdr/{}.tif".format(path, fnbase)
	fnsphere = "{}/sphere/{}_sphere.tif".format(path, fnbase)

	print "\nUsing HDRMerge to combine images into a floating point .DNG"
	cmd = ['hdrmerge', '-o', fndng, '-v']
	for image in hdrset:
		cmd.append(image)
	executeAndPrintCommand(cmd)

	print "\nUsing RawTherapee to convert floating point .DNG to 16 bit .TIFF"
	cmd = ['rawtherapee', '-t', '-Y','-c', fndng]
	executeAndPrintCommand(cmd)

	#sleep to wait for tif to finish writing 
	print "\nWriting converted .DNG to {}".format(fntif)
	
	print "\nRemoving .DNG"
	cmd = ["rm", "-r",  fndng]
	executeAndPrintCommand(cmd)

	#TODO - QR code registration and cropping

	#create equirectangular map of sphere
	print "\nGenerating spheres from {}".format(fntif)
	generateSpheres(fntif, fnsphere)


if __name__ == "__main__":
	#Construct and configure argument parser
	parser = argparse.ArgumentParser(description="Processes a directory of raw images and combines ones taken with the same" 
									 "flash angle and different exposures into HDR .DNG and .TIFF images. From the" 
									 "HDR image the mirror and diffuse spheres are isolated, extracted, unwrapped"
									 "and saved into .TIFF files.")
	parser.add_argument("--imagesdir", "-i", help="Directory containing the .ARW input images")
	parser.add_argument("--metadata", "-m", help=".txt containing the angles and HDR pairings")
	args = parser.parse_args()

	startime =  time.time()

	if (os.path.isfile(args.metadata)):
		print "\nReading metadata file"	
		f = open(args.metadata, "r")
		contents = f.readlines()
		f.close()
	else: 
		print "Metadata file {} does not exist".format(args.metadata)
		quit()

	#Seperate ARW files in the directory into "sets" of images based off metadata txt file
	hdrsets = []
	hdrset = []
	setID = "0"

	#Fill the hdrsets with images' filenames (skip first line of metadata)
	print "\nGrouping sets of images together"
	for i in range(1, len(contents)):
		ID, phi, theta, fname = contents[i].split()
		#check to see if the file exists
		if os.path.isfile(args.imagesdir + '/' + fname):
			#group together images with the same ID
			if (setID != ID):
				hdrsets.append(hdrset)
				hdrset = []
				setID = ID
			hdrset.append(args.imagesdir + '/' + fname)
		else:
			print "Image file {}/{} does not exist".format(args.imagesdir, fname)
			quit()
	hdrsets.append(hdrset)			

	#Configure directories for output images
	print "\nCreating output directories"
	cmd = ["mkdir", "-p", "-v", args.imagesdir + "/hdr"]
	executeAndPrintCommand(cmd)
	cmd = ["mkdir", "-p", "-v", args.imagesdir + "/sphere"]
	executeAndPrintCommand(cmd)

	#process each set of images
	for i in range(0, len(hdrsets)):
		print "\n\n Processing image set {}/{}".format(i+1, len(hdrsets))
		processHDRset(hdrsets[i])

	endtime = time.time()
	print "\nFinished processing images"
	print "\nTime elapsed: {}".format(endtime-startime)