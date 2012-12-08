import sys, socket

import artnet
from artnet.logical import fixtures

def main():
	if(len(sys.argv) < 2):
		sys.argv.append('<broadcast>')
	
	f = fixtures.Fixture(17)
	f.configure({
		"name": "ADJ MegaBar RGB50",
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
				}
			},
			{
				"offset": 5,
				"type": "program",
				"macro": {
					"slow-fade": {
						"value": 127,
						"speed": 127,
					},
				}
			}
		],
		"strobe_offset": 4,
		"intensity_offset": 6
	})
	f.setColor('#ff0000')
	f.setIntensity(255)
	
	# #example code
	# f.setColor('#fff')
	# f.setPosition(0.5, 0.2)
	# f.setIntensity(0.9)
	# f.strobeSpeed(10) #ms?
	# f[0].setColor('#f00') # subfixtures
	# f.setMacro('short-fade')
	
	channels = [0] * 512
	for offset, value in f.getState():
		if(offset is None):
			continue
		channels[(f.address - 1) + offset] = value
	
	artnet.send_dmx(sys.argv[1], channels)

if(__name__ == '__main__'):
	main()