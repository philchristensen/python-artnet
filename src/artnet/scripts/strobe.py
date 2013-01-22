import sys

from artnet import dmx

def main(address, channel):
	channel = int(channel)
	white = [0] * 512
	white[channel] = 255
	white[channel+1] = 255
	white[channel+2] = 255
	white[channel+6] = 255
	
	q = dmx.Controller(address, nodaemon=False)
	q.add(iter([white, [0] * 512]))
	q.start()
