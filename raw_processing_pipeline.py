import argparse
import subprocess
import os
import sys
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
		sys.stdout.write(line)
		sys.stdout.flush()
    

def processHDRset(hdrset):
	#configure output filenames and directories
	path = getOutputPath(hdrset)
	fnbase = getOutputName(hdrset) 
	fndng = path + "/hdr/" + fnbase + ".dng"
	fntif = path + "/hdr/" + fnbase + ".tif"
	fnsphere = path + "/sphere/" + fnbase + "_sphere.tif"

	print "Creating output directories"
	cmd = ["mkdir", "-p", "-v", path + "/hdr"]
	executeAndPrintCommand(cmd)
	cmd = ["mkdir", "-p", "-v", path + "/sphere"]
	executeAndPrintCommand(cmd)

	print "\nUsing HDRMerge to combine images into a floating point .DNG \n - - - - - - - - - - -"
	cmd = ['hdrmerge', '-o', fndng, '-v']
	for image in hdrset:
		cmd.append(image)
	executeAndPrintCommand(cmd)

	print "\nUsing RawTherapee to convert floating point .DNG to 16 bit .TIFF \n - - - - - - - - - - -"
	cmd = ['rawtherapee', '-t', '-Y','-c', fndng]
	executeAndPrintCommand(cmd)
	print "Wrote converted .DNG to {}".format(fntif)

	print "\nRemoving .DNG"
	cmd = ["rm", "-r",  fndng]
	executeAndPrintCommand(cmd)

	#TODO - QR code registration and cropping

	#create equirectangular map of sphere
	print "Generating spheres from {}".format(fntif)
	generateSpheres(fntif, fnsphere)


if __name__ == "__main__":
	#Construct and configure argument parser
	parser = argparse.ArgumentParser(description="Processes a directory of raw images and combines ones taken with the same" 
									 "flash angle and different exposures into HDR .DNG and .TIFF images. From the" 
									 "HDR image the mirror and diffuse spheres are isolated, extracted, unwrapped"
									 "and saved into .TIFF files.", 
									 usage="RAW Image Dataset Procesing Pipeline \n [-h] DIR")
	parser.add_argument("DIR", help="Directory containing the .ARW input images")
	args = parser.parse_args()


	#Seperate ARW files in the directory into "sets" of images with the same angle
	hdrsets = []
	hdrset = []
	for path, subdirs, files in os.walk(args.DIR):
		for filename in files:
			if filename.endswith(".ARW"):
				hdrset.append(os.path.join(args.DIR, filename))
	hdrsets.append(hdrset)

	#process each set of images
	for hdrset in hdrsets:
		processHDRset(hdrset)

