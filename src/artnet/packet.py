import struct, itertools

sequencer = None
def reset_sequence():
	global sequencer
	sequencer = itertools.cycle(xrange(255))
reset_sequence()

HEADER = 'Art-Net\0'
PROTOCOL_VERSION = 14
ARTNET_OUTPUT = 0x5000

class ArtNetPacket(object):
	def __init__(self, physical=0, universe=0):
		self.sequence = sequencer.next()
		self.physical = physical
		self.universe = universe
		self.channels = [0] * 512
	
	def __setitem__(self, index, value):
		if not(isinstance(value, int)):
			raise TypeError("Invalid ArtNet value: %r" % value)
		if(index < 0 or index > 255):
			raise ValueError("Invalid ArtNet channel: %r " % index)
		self.channels[index] = value
	
	def __getitem__(self, index):
		return self.channels[index]
	
	def encode(self):
		header = struct.pack('!8shhiih', 
			HEADER, ARTNET_OUTPUT, PROTOCOL_VERSION,
			self.sequence, self.physical, self.universe)
		predicate = lambda x: x is not None
		def _split(i):
			if(i < 128):
				return i, 0
			else:
				return 127, i - 127
		return header + ''.join([struct.pack('bb', *_split(c)) for c in self.channels])