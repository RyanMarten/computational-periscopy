import argparse
import subprocess

parser = argsparse.ArgumentParser("combines multiple RAW images into a single HDR .tif image"
parser.add_argument("images", nargs="+", help='input RAW files to be combined')
parser.add_argument("-o", "--output", help="output file name", action="store_true")
args = parser.parse_args()

print args.images
print args.output


print subprocess.check_output(['ls', '-l'])

