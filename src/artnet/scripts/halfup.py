import sys

from artnet import dmx

def main():
	if(len(sys.argv) < 2):
		sys.argv.append('<broadcast>')
	
	q = dmx.Controller(sys.argv[1], nodaemon=True)
	q.enqueue([[0] * 512])
	q.start()

