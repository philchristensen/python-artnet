import sys

import artnet

def main():
	if(len(sys.argv) < 2):
		sys.argv.append('<broadcast>')
	
	artnet.send_dmx(sys.argv[1], [127] * 512)

