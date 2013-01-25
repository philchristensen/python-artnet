import time

from artnet import dmx
from artnet.logical import fixtures

g = fixtures.FixtureGroup([
	fixtures.Fixture.create(420, 'chauvet/slimpar-64.yaml'),
	fixtures.Fixture.create(427, 'chauvet/slimpar-64.yaml'),
	fixtures.Fixture.create(434, 'chauvet/slimpar-64.yaml'),
	fixtures.Fixture.create(441, 'chauvet/slimpar-64.yaml'),
])

def all_red():
	while(True):
		g.setColor('#ff0000')
		g.setIntensity(255)
		yield g.getChannels()

def single_white_beat_chase(clock, secs=5.0):
	t = time.time()
	c = clock()
	while(c['running']):
		g.setColor('#ffffff')
		g.setIntensity(0)
		f = g.fixtures[c['beat'] - 1]
		f.setIntensity(255)
		frame = f.getChannels()
		yield frame
		if(secs and time.time() - t >= secs):
			return
		c = clock()

def main(address):
	q = dmx.Controller(address, bpm=60, nodaemon=True, runout=True)
	q.add(all_red())
	q.add(single_white_beat_chase(q.get_clock()))
	q.start()

