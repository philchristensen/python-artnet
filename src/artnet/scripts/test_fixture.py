#!/opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import sys, time

from artnet import dmx, packet
from artnet.logical import fixtures

def main():
	if(len(sys.argv) < 2):
		sys.argv.append('192.168.0.88') #<broadcast>')
	
	f = fixtures.Fixture(427)
	f.configure({
		"name": "Chauvet SlimPAR 64",
		"rgb_offsets" : {
			"red": 0,
			"blue": 1,
			"green": 2,
		},
		"program_channels": [
			{
				"offset": 3,
				"type": "color",
				"macros": {
					"white": 255,
					"teal": 16,
					"violet": 32,
					"lime-green": 64,
					"purple": 80,
					"blue": 112,
					"aqua": 127,
					"magenta": 180
				}
			},
			{
				"offset": 5,
				"type": "program",
				"macros": {
					"pulse-up": {
						"value": 32,
						"speed": 255,
					},
					"pulse-down": {
						"value": 64,
						"speed": 255,
					},
					"pulse": {
						"value": 96,
						"speed": 255,
					},
					"autofade": {
						"value": 128,
						"speed": 255,
					},
					"autosnap-3": {
						"value": 160,
						"speed": 255,
					},
					"autosnap-7": {
						"value": 192,
						"speed": 255,
					},
					"soundsens": {
						"value": 224,
						"speed": 0,
					}
				}
			}
		],
		"strobe_offset": 4,
		"intensity_offset": 6
	})
	f.setColor('#ff0000')
	f.setIntensity(255)
	#f.triggerMacro('color', 'purple')
	#f.triggerMacro('program', 'soundsens')
	#f.setStrobe(255)
	
	frame1 = dmx.get_channels(f)
	f.setColor('#0000ff')
	frame2 = dmx.get_channels(f)
	f.setColor('#00ff00')
	frame3 = dmx.get_channels(f)
	
	q = dmx.PacketQueue(sys.argv[1])
	q.enqueue(dmx.create_fade(frame1, frame2))
	q.enqueue(dmx.create_multifade([frame1, frame2, frame3] * 3, secs=5.0))
	q.enqueue(dmx.create_multifade([frame1, frame2, frame3], secs=15.0))
	q.enqueue(dmx.create_multifade([frame1, frame2, frame3] * 6, secs=5.0))
	t = time.time()
	q.run()
	print time.time() - t
	


if(__name__ == '__main__'):
	import logging
	logging.basicConfig(level=logging.INFO)
	main()