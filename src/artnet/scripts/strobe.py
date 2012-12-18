import sys

from artnet import dmx

def main(address, channel):
	channel = int(channel)
	white = [0] * 512
	white[channel] = 255
	white[channel+1] = 255
	white[channel+2] = 255
	white[channel+6] = 255
	
	q = dmx.Controller(address, nodaemon=True)
	q.enqueue([white, [0] * 512] * 200)
	q.start()

def entry_point():
	main(*sys.argv)

if(__name__ == '__main__'):
	main(*sys.argv[1:])
