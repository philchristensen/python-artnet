import sys

import artnet

def main():
	if(len(sys.argv) < 2):
		print "\nUsage:\n\tartnet_halfup [address]\n"
		sys.exit(1)
	
	artnet.send_dmx(sys.argv[1], [127] * 512)

