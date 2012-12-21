#!/opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import sys, time

from artnet import dmx, packet
from artnet.logical import fixtures

def main():
	if(len(sys.argv) < 2):
		sys.argv.append('192.168.0.88') #<broadcast>')
	
	f = fixtures.Fixture(427)
	f.configure(fixtures.load('chauvet/slimpar-64.yaml'))
	f.setColor('#ff0000')
	f.setIntensity(255)
	#f.triggerMacro('color', 'purple')
	#f.triggerMacro('program', 'soundsens')
	#f.setStrobe(255)
	
	red = dmx.get_channels(f)
	f.setColor('#0000ff')
	blue = dmx.get_channels(f)
	f.setColor('#000000')
	blackout = dmx.get_channels(f)
	
	q = dmx.Controller(sys.argv[1], nodaemon=True)

	# g = iter(dmx.create_multifade([red, blue] * 3, secs=5.0))
	# q.add(g)
	
	# def _timeout():
	# 	time.sleep(1)
	# 	yield dmx.Frame()
	# q.add(_timeout())
	
	q.add(dmx.generate_fade(red, blue))
	
	q.start()

if(__name__ == '__main__'):
	import logging
	logging.basicConfig(level=logging.INFO)
	main()