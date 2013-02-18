import time

from artnet import dmx

def rotate(clock, group):
	t = time.time()
	c = clock()
	while(c['running']):
		if(c['beatindex'] == 0):
			colors = group.getColor()
			colors.append(colors.pop(0))
			for i in range(len(colors)):
				group[i].setColor(colors[i])
			
			intensities = group.getIntensity()
			intensities.append(intensities.pop(0))
			for i in range(len(intensities)):
				group[i].setIntensity(intensities[i])
			
			strobes = group.getStrobe()
			strobes.append(strobes.pop(0))
			for i in range(len(strobes)):
				group[i].setStrobe(strobes[i])
		
		yield group.getFrame()
		c = clock()

