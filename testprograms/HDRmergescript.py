import argparse
import subprocess
import os
import sys

parser = argparse.ArgumentParser("combines multiple RAW images into a single HDR .tif image")
parser.add_argument("DIR", help="Directory containing the RAW input images")

#take a folder as an argument
#seperate folder into sets of images that need to be combine


args = parser.parse_args()

hdrsets = []

hdrset = []

#change to add multiple HDR sets based off of sequence or some other characteristic

for path, subdirs, files in os.walk(args.DIR):
	for filename in files:
		if filename.endswith(".ARW"):
			hdrset.append(os.path.join(args.DIR, filename))

hdrsets.append(hdrset)

#helps print out subprocesses stdout as they happen
def executeCommand(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for stdout_line in iter(popen.stdout.readline, ""):
    	yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
    	raise subprocess.CalledProcessError(return_code, cmd)
    

def convertSetsToHDR(hdrsets):
	for hdrset in hdrsets:

		#change "hdr.dng" to a smart naming scheme like HDRMerge uses


		print "Using HDRMerge to combine images into a floating point .DNG \n - - - - - - - - - - -"
		cmd = ['hdrmerge', '-o', 'hdr.dng', '-v']
		for image in hdrset:
			cmd.append(image)
		for line in executeCommand(cmd):
			sys.stdout.write(line)
			sys.stdout.flush()

		print "\nUsing RawTherapee to convert floating point .DNG to 16 bit .TIFF \n - - - - - - - - - - -"
		cmd = ['rawtherapee', '-t', '-Y','-c', 'hdr.dng']
		for line in executeCommand(cmd):
			sys.stdout.write(line)
			sys.stdout.flush()


convertSetsToHDR(hdrsets)