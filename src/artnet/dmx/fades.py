import time, logging

from artnet import dmx

log = logging.getLogger(__name__)

def create_multifade(frames, secs=5.0, fps=40):
	result = []
	total_frames = len(frames)
	for index in range(total_frames):
		if(index < len(frames) - 1):
			fade = generate_fade(frames[index], frames[index+1], secs/(total_frames-1), fps)
			result.extend(list(fade))
	return iter(result)

def generate_fade(start, end, secs=5.0, fps=40):
	for index in range(int(secs * fps)):
		f = dmx.Frame()
		for channel in range(len(start)):
			a = start[channel] or 0
			b = end[channel] or 0
			f[channel] = int(a + (((b - a) / (secs * fps)) * index))
		yield f

def pulse_beat(clock, start, end, secs=5.0):
	t = time.time()
	c = clock()
	while(c['running']):
		if(c['beat'] % 2):
			yield start
		else:
			yield end
		if(time.time() - t >= secs):
			return
		c = clock()

