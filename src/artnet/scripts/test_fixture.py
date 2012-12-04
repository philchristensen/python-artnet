import sys, socket

import artnet

def main():
	if(len(sys.argv) < 2):
		print "\nUsage:\n\ttest_fixture [address]\n"
		sys.exit(1)
	
	f = fixtures.create(499, {
		"name": "ADJ MegaBar RGB50",
		"rgb_offsets" : {
			"red": 0,
			"blue": 1,
			"green": 2,
		},
		"program_channel": {
			"offset": 3,
			"type": "color",
			"macro": {
				"white": 255,
			}
		},
		"strobe_offset": 4,
		"program_channel": {
			"offset": 5,
			"type": "program",
			"macro": {
				"slow-fade": 127,
			}
		},
		"intesity_offset": 6
	})
	f.setColor('#f00')
	
	# #example code
	# f.setColor('#fff')
	# f.setPosition(0.5, 0.2)
	# f.setIntensity(0.9)
	# f.strobeSpeed(10) #ms?
	# f[0].setColor('#f00') # subfixtures
	# f.setMacro('short-fade')
	
	artnet.send_dmx(sys.argv[1], f.getState())

if(__name__ == '__main__'):
	main()