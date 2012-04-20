import struct, itertools

HEADER = 'Art-Net\0'
PROTOCOL_VERSION = 14
ARTNET_OUTPUT = 0x5000

def lohi(i):
	low = i & 0x00FF
	high = (i & 0xFF00) >> 8
	return low, high

sequencer = None
def reset_sequence():
	global sequencer
	sequencer = itertools.cycle(xrange(255))
reset_sequence()

class ArtNetPacket(object):
	def __init__(self, physical=0, universe=0):
		self.sequence = sequencer.next()
		self.physical = physical
		self.universe = universe
		self.channels = [0] * 512
	
	def __setitem__(self, channel, value):
		if not(isinstance(value, int)):
			raise TypeError("Invalid DMX value: %r" % value)
		if(value < 0 or value > 255):
			raise ValueError("Invalid DMX value: %r " % value)
		if(channel < 0 or channel > 511):
			raise ValueError("Invalid DMX channel: %r " % channel)
		self.channels[channel] = value
	
	def __getitem__(self, index):
		return self.channels[index]
	
	def encode(self):
		proto_lo, proto_hi = lohi(PROTOCOL_VERSION)
		subuni, net = lohi(self.universe)
		len_lo, len_hi = lohi(512)
		header = struct.pack('!8shBBBBBBBB', 
			HEADER, ARTNET_OUTPUT, proto_hi, proto_lo,
			self.sequence, self.physical, subuni, net, len_hi, len_lo)
		return header + ''.join([struct.pack('!B', c) for c in self.channels])

if(__name__ == '__main__'):
	import socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	p = ArtNetPacket()
	l = sock.sendto(p.encode(), ('192.168.0.88', 6454))
	print 'sent %s bytes' % l