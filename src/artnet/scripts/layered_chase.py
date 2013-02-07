import time

from artnet import dmx, fixtures, rig

# set up test fixtures
r = rig.get_default_rig()
g = r.groups['all']

def all_red(secs=5.0):
	"""
	A simple all-red light generator.
	"""
	t = time.time()
	while(True):
		g.setColor('#0000ff')
		g.setIntensity(255)
		yield g.getFrame()
		if(secs and time.time() - t >= secs):
			return

def single_white_beat_chase(clock, secs=5.0):
	"""
	A simple white chase pattern.
	"""
	t = time.time()
	c = clock()
	while(c['running']):
		# Reset to white, but blacked out
		g.setColor('#ffffff')
		g.setIntensity(0)
		
		# Grab one fixture, set its intensity
		f = g.fixtures[c['beat'] - 1]
		f.setIntensity(255)
		
		# Grab just that fixture's DMX values
		frame = f.getFrame()
		yield frame
		if(secs and time.time() - t >= secs):
			return
		c = clock()

def bouncing_ball(clock, secs=5.0):
	"""
	A bouncing red chase pattern.
	"""
	t = time.time()
	c = clock()
	position = 0
	direction = 1
	while(c['running']):
		if not(c['frameindex'] % 4):
			position += direction
		if(position == len(g.fixtures)):
			position -= 2
			direction = -1
		elif(position == 0):
			direction = 1
		
		# Reset to white, but blacked out
		g.setColor('#ff0000')
		g.setIntensity(0)
		
		# Grab one fixture, set its intensity
		f = g.fixtures[position]
		f.setIntensity(255)
		
		# Grab just that fixture's DMX values
		frame = f.getFrame()
		yield frame
		if(secs and time.time() - t >= secs):
			return
		c = clock()

def main(config, controller=None):
	q = controller or dmx.Controller(config.get('base', 'address'), bpm=240, nodaemon=True, runout=True)
	# "base color" red
	q.add(all_red())
	# white chase layer
	q.add(single_white_beat_chase(q.get_clock()))
	q.add(bouncing_ball(q.get_clock()))
	if not controller:
		q.start()

