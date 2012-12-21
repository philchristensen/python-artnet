import time, sys, socket, logging, threading

from artnet import packet

log = logging.getLogger(__name__)

def create_multifade(frames, secs=5.0, fps=40):
	result = []
	total_frames = len(frames)
	for index in range(total_frames):
		if(index < len(frames) - 1):
			result.extend(create_fade(frames[index], frames[index+1], secs/(total_frames-1), fps))
	return result

def create_fade(start, end, secs=5.0, fps=40):
	result = []
	for position in range(int(secs * fps)):
		f = Frame()
		for channel in range(len(start)):
			a = start[channel] or 0
			b = end[channel] or 0
			f[channel] = int(a + (((b - a) / (secs * fps)) * position))
		result.append(f)
	return result

def get_channels(fixtures):
	fixtures = fixtures if isinstance(fixtures, list) else [fixtures]
	channels = [0] * 512
	for f in fixtures:
		for offset, value in f.getState():
			if(offset is None):
				continue
			channels[(f.address - 1) + offset] = value
	return channels

class Frame(list):
	def __init__(self, channels=None):
		super(Frame, self).__init__((channels[i] if channels else None for i in xrange(512)))
	
	def __setitem__(self, index, value):
		if not(isinstance(index, int)):
			raise TypeError("Invalid channel index: %r" % index)
		if not(0 <= index < 512):
			raise ValueError("Invalid channel index: %r" % index)
		if not(isinstance(value, int)):
			raise TypeError("Invalid value index: %r" % index)
		if not(0 <= value < 256):
			raise ValueError("Invalid value index: %r" % index)
		super(Frame, self).__setitem__(index, value)
	
	def merge(self, frame):
		for i in range(512):
			self[i] = self[i] if frame[i] is None else frame[i]

class Controller(threading.Thread):
	def __init__(self, address, fps=40.0, nodaemon=False):
		super(Controller, self).__init__()
		self.address = address
		self.fps = fps
		self.last_frame = Frame()
		self.generators = []
		self.access_lock = threading.Lock()
		self.nodaemon = nodaemon
		self.daemon = not nodaemon
		self.running = True
	
	def stop(self):
		try:
			self.access_lock.acquire()
			if(self.running):
				self.running = False
		finally:
			self.access_lock.release()
	
	def add(self, generator):
		try:
			self.access_lock.acquire()
			self.generators.append(generator)
		finally:
			self.access_lock.release()
	
	def iterate(self):
		f = None
		for g in self.generators:
			try:
				n = g.next()
				f = f.merge(n) if f else n
			except StopIteration:
				self.generators.remove(g)
		self.last_frame = f if f else self.last_frame
	
	def run(self):
		now = time.time()
		while(self.generators if self.nodaemon else self.running):
			drift = now - time.time()
			self.iterate()
			self.send(self.last_frame)
			elapsed = time.time() - now
			excess = (1 / self.fps) - elapsed
			if(excess > 0):
				time.sleep(excess - drift)
			else:
				log.warning("Frame rate loss; generators took %ss too long" % round(abs(excess), 2))
			now = time.time()
	
	def send(self, frame):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		sock.bind(('', packet.ARTNET_PORT))
		
		p = packet.DmxPacket(frame)
		
		#log.info(p)
		
		sock.sendto(p.encode(), (self.address, packet.ARTNET_PORT))
		sock.close()

	