import time, logging

from artnet import dmx, fixtures, rig
from artnet.dmx import fades

log = logging.getLogger(__name__)

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
	log.info("Running script %s" % __name__)
	# global g
	# g = get_default_fixture_group(config)
	q = controller or dmx.Controller(config.get('base', 'address'), bpm=60, nodaemon=True, runout=True)

	q.add(fades.create_multifade([
		all_red(),
		all_blue(),
	] * 3, secs=5.0))
	
	if not controller:
		q.start()

