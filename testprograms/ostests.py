import argparse
import subprocess
import os

parser = argparse.ArgumentParser("combines multiple RAW images into a single HDR .tif image")
parser.add_argument("DIR", help="Directory containing the RAW input images")


args = parser.parse_args()

print args.DIR

listdir = os.listdir(args.DIR)
for f in listdir:
	if os.path.isfile(os.path.join(args.DIR,f)):
		print f

print "\n\n --------Filtered-------- \n\n"

for path, subdirs, files in os.walk(args.DIR):
	for filename in files:
		if filename.endswith(".ARW"):
			print filename