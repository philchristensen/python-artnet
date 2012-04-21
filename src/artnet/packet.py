import struct, itertools, time

HEADER = 'Art-Net\0'
PROTOCOL_VERSION = 14

ARTNET_POLL = 0x0020
ARTNET_POLL_REPLY = 0x0021
ARTNET_TOD_REQUEST = 0x0080
ARTNET_OUTPUT = 0x0050

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
	def __init__(self, opcode=ARTNET_OUTPUT, physical=0, universe=0):
		self.sequence = sequencer.next()
		self.physical = physical
		self.universe = universe
		self.channels = [0] * 512
		self.opcode = opcode
	
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
		len_lo, len_hi = lohi(512)
		
		if(self.opcode == ARTNET_OUTPUT):
			header = struct.pack('!8sHBBBBHBB', 
				HEADER, self.opcode, proto_hi, proto_lo,
				self.sequence, self.physical, self.universe, 0, 0)
			return header + ''.join([struct.pack('!B', c) for c in self.channels])
		elif(self.opcode == ARTNET_POLL):
			return struct.pack('!8sHBBBB', HEADER, self.opcode, proto_hi, proto_lo, 0x02, 0)
		elif(self.opcode == ARTNET_TOD_REQUEST):
			return ''.join([
				struct.pack('!8sHBB', HEADER, self.opcode, proto_hi, proto_lo),
				''.join([struct.pack('!B', 0) for x in range(7)]),
				''.join([struct.pack('!B', x) for x in [0, 0, 0, 0, 1, 1]]),
				''.join([struct.pack('!B', 0) for x in range(31)])
			])

if(__name__ == '__main__'):
	import socket
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('192.168.0.98', 6454))
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	p = ArtNetPacket(opcode=ARTNET_POLL)
	l = sock.sendto(p.encode(), ('192.168.0.255', 6454))
	
	print 'sent %s bytes' % l	
	time.sleep(2)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('192.168.0.98', 6454))
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	p = ArtNetPacket(opcode=ARTNET_TOD_REQUEST)
	l = sock.sendto(p.encode(), ('192.168.0.255', 6454))
	
	print 'sent %s bytes' % l	
	time.sleep(2)

	# blackout
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('192.168.0.98', 6454))
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	p = ArtNetPacket()
	l = sock.sendto(p.encode(), ('192.168.0.255', 6454))
	
	print 'sent %s bytes' % l