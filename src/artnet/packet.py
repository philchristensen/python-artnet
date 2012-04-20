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
	
	def __setitem__(self, channel, value):
		if not(isinstance(value, int)):
			raise TypeError("Invalid ArtNet value: %r" % value)
		if(value < 0 or value > 255):
			raise ValueError("Invalid ArtNet value: %r " % value)
		if(channel < 0 or channel > 511):
			raise ValueError("Invalid ArtNet value: %r " % channel)
		self.channels[channel] = value
	
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
				return 127, i - 128
		return header + ''.join([struct.pack('bb', *_split(c)) for c in self.channels])

if(__name__ == '__main__'):
	import socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	p = ArtNetPacket()
	l = sock.sendto(p.encode(), ('192.168.0.88', 6454))
	print 'sent %s bytes' % l