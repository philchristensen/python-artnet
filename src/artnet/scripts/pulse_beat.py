import time

from artnet import dmx, fixtures, rig
from artnet.dmx import fades

# set up test fixtures
r = rig.get_default_rig()
g = r.groups['all']

def all_red():
	"""
	Create an all-red frame.
	"""
	g.setColor('#ff0000')
	g.setIntensity(255)
	return g.getFrame()

def all_blue():
	"""
	Create an all-blue frame.
	"""
	g.setColor('#0000ff')
	g.setIntensity(255)
	return g.getFrame()

def main(config, controller=None):
	q = controller or dmx.Controller(config.get('base', 'address'), bpm=60, nodaemon=True, runout=True)
	
	q.add(fades.pulse_beat(q.get_clock(), all_red(), all_blue(), secs=5.0))
	
	if not controller:
		q.start()

