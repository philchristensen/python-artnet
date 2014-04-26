import logging

import time

from artnet import dmx, fixtures, rig

# set up test fixtures
r = rig.get_default_rig()
g = r.groups['all']

log = logging.getLogger(__name__)

def main(config, controller=None):
	log.info("Running script %s" % __name__)
	q = controller or dmx.Controller(config.get('base', 'address'), bpm=240, nodaemon=False)

	g.setIntensity(255)
	g.setColor('#ffffff')
	
	g[0].setColor('#ff0000')
	g[1].setColor('#00ff00')
	g[2].setColor('#0000ff')
	g[3].setColor('#ff00ff')
	
	from artnet.dmx import patterns
	q.add(patterns.rotate(q.get_clock(), g))
	
	if not controller:
		q.start()

