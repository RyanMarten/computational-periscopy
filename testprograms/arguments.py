import argparse

parser = argparse.ArgumentParser("calculate the square of a number")
parser.add_argument("square", help="display a square of a given number", type=int)

'''
parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
args = parser.parse_args()
answer = args.square**2
if args.verbosity:
	print "the square of {} equals {}".format(args.square, answer)
else:
	print answer
'''

'''
parser.add_argument("-v", "--verbosity", type=int, choices=[0,1,2], help="increases output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
	print "the square of {} equals {}".format(args.square, answer)
elif args.verbosity == 1: 
	print "{}^2 = {}".format(args.square, answer)
else:
	print answer
'''

parser.add_argument("-v", "--verbosity", action="count", help="increase output verbosity", default=0)
args = parser.parse_args()
answer = args.square**2
if args.verbosity >= 2:
	print "the square of {} equals {}".format(args.square, answer)
elif args.verbosity >= 1:
	print "{}^2 = {}".format(args.square, answer)
else:
	print answer

'''
parser.add_argument("images", nargs="+", help='input RAW files to be combined')

command = ['hdrmerge', '-o', 'hdr.dng', '-v', '-Y']
for image in args.images:
	command.append(image)
print subprocess.check_output(command)

command = ['rawtherapee', '-t', '-c', 'hdr.dng']
print subprocess.check_output(command)

'''