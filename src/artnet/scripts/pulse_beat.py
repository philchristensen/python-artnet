import time

from artnet import dmx, fixtures
from artnet.dmx import fades

# set up test fixtures
g = fixtures.FixtureGroup([
	fixtures.Fixture.create(420, 'chauvet/slimpar-64.yaml'),
	fixtures.Fixture.create(427, 'chauvet/slimpar-64.yaml'),
	fixtures.Fixture.create(434, 'chauvet/slimpar-64.yaml'),
	fixtures.Fixture.create(441, 'chauvet/slimpar-64.yaml'),
])

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

def main(config):
	q = dmx.Controller(config.get('base', 'address'), bpm=60, nodaemon=True, runout=True)
	
	q.add(fades.pulse_beat(q.get_clock(), all_red(), all_blue(), secs=5.0))
	
	q.start()

