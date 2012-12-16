import socket, struct, itertools, time

from artnet import listener

HEADER = 'Art-Net\0'
PROTOCOL_VERSION = 14

ARTNET_PORT = 6454

def lohi(i):
	low = i & 0x00FF
	high = (i & 0xFF00) >> 8
	return low, high

class ArtNetPacket(object):
	opcode = None
	
	def __init__(self, source=None, physical=0, universe=0):
		self.sequence = 0
		self.physical = physical
		self.universe = universe
		self.source = source
	
	def __repr__(self):
		return '<%(klass)s from %(source)s:%(universe)s/%(physical)s>' % dict(
			klass    = self.__class__.__name__,
			source   = self.source,
			universe = self.universe,
			physical = self.physical,
		)
	
	def encode(self):
		raise NotImplementedError('encode')
	
	@classmethod
	def parse(cls, address, data):
		[opcode] = struct.unpack('!H', data[8:10])
		for k, packet_class in globals().items():
			if not(k.endswith('Packet')):
				continue
			if(packet_class == cls):
				continue
			if not(issubclass(packet_class, cls)):
				continue
			if(packet_class.opcode == opcode):
				return packet_class.decode(address, data)
		raise NotImplementedError('%r' % opcode)

class DmxPacket(ArtNetPacket):
	opcode = 0x0050
	
	def __init__(self, sequence=0, **kwargs):
		super(DmxPacket, self).__init__(**kwargs)
		self.sequence = sequence
		self.channels = [0] * 512
	
	def __setitem__(self, channel, value):
		if not(isinstance(value, int)):
			raise TypeError("Invalid DMX value: %r" % [value])
		if(value < 0 or value > 255):
			raise ValueError("Invalid DMX value: %r " % [value])
		if(channel < 0 or channel > 511):
			raise ValueError("Invalid DMX channel: %r " % [channel])
		self.channels[channel] = value
	
	def __getitem__(self, index):
		return self.channels[index]
	
	def __str__(self):
		return '<DMX(%(sequence)s): %(channels)s>' % dict(
			sequence = self.sequence,
			channels = ', '.join([
				'%s: %s' % (
					address + 1,
					self.channels[address]
				) for address in range(len(self.channels)) if self.channels[address]
			])
		)
	
	def encode(self):
		proto_lo, proto_hi = lohi(PROTOCOL_VERSION)
		len_lo, len_hi = lohi(512)
		header = struct.pack('!8sHBBBBHBB', 
			HEADER, self.opcode, proto_hi, proto_lo,
			self.sequence, self.physical, self.universe, len_hi, len_lo)
		return header + ''.join([0 if c is None else struct.pack('!B', c) for c in self.channels])
	
	@classmethod
	def decode(cls, address, data):
		return cls(source=address)

class PollPacket(ArtNetPacket):
	opcode = 0x0020
	
	def __init__(self, ttm=0x02, priority=0, **kwargs):
		super(PollPacket, self).__init__(**kwargs)
		self.ttm = ttm
		self.priority = priority
	
	def encode(self):
		proto_lo, proto_hi = lohi(PROTOCOL_VERSION)
		return struct.pack('!8sHBBBB', HEADER, self.opcode, proto_hi, proto_lo, self.ttm, self.priority)
	
	@classmethod
	def decode(cls, address, data):
		parts = struct.unpack(''.join([
			'!',
			'8s',  # header
			'H',   # opcode
			'BB',  # proto hi,lo
			'B',   # talk to me
			'B',   # level
		]), data)
		return cls(ttm=parts[4], priority=parts[5], source=address)

class PollReplyPacket(ArtNetPacket):
	opcode = 0x0021
	
	def __init__(self, replydata, **kwargs):
		super(PollReplyPacket, self).__init__(**kwargs)
		self.replydata = replydata
	
	def encode(self):
		ip = [int(x) for x in socket.gethostbyname(socket.gethostname()).split('.')]
		data = (HEADER, self.opcode, ip[0], ip[1], ip[2], ip[3], ARTNET_PORT,
			0, 1, # version
			0, 0, # universe 
			1, 144, # oem
			0, 2, 0, # ubea-version, status1, esta man
			'python-artnet-lib\x00', # short name
			'python-artnet-lib\x00\x00\x00\x01\x00\x01admin\x00\xff\x92\xff\xbf\xf90{\xdd\x7f>\xfa\x8f\xeb3?o\xc3?wo\xe8\x1f\t\xe8;8\x85\xcbc<\xad\xce\xea\xf6\xb1',
			'\x00\xe8y\xff\xfb\xe2\xeb[}\xb5\xd3\x99\xf1\xfd\xb37C\xeb\x83-\x01\xf0v\t\xe3\xdeP\x13\x03\xc2\x94\x89Z\x88\x14\x9dHEf\x07\xc8\x0b\x17\x00\x00\x982\x1c\x08T\x0bkW\x17\xb2\x00B\x05\x82\xd3\x00\x00\x00\x94',
			0, 1, # num ports
			128, 0, 0, 0, # port types
			0, 0, 0, 0, # good input
			128, 0, 0, 0, # good output
			74, 0, 0, 0, # SWIN
			0, 0, 0, 0, # SWOUT
			0, 0, 0, # vid, macro, remote
			0, 0, 0, # 3 - spare
			0, #style
			# MAC hi
			0x00, 0x14, 0x51, 0x62, 0x81, 0xe0,
			0
		)
		return struct.pack(''.join([
			'!',
			'8s',  # 1 header
			'H',   # 2 opcode
			'4B',  # 3 ip address
			'H',   # 4 port
			'BB',  # 5,6 versioninfo hi,lo
			'BB',  # 7,8 net, sub
			'BB',  # 9,10 oem hi,lo
			'B',   # 11 UBEA version
			'B',   # 12 Status 1
			'H',   # 13 ESTA manufacturer code,
			'18s', # 14 Short Name
			'64s', # 15 Long Name
			'64s', # 16 Node Report
			'BB',  # 17,18 num ports hi,lo
			'4B',  # 19 port types array
			'4B',  # 20 good input array
			'4B',  # 21 good output array
			'4B',  # 22 sw input address
			'4B',  # 23 sw output address
			'B',   # 24 sw video
			'B',   # 25 sw macro
			'B',   # 26 sw remote
			'B',   # 27 not used
			'B',   # 28 not used
			'B',   # 29 not used
			'B',   # 30 style
			'B',   # 31 mac address hi
			'B',   # 32 mac address
			'B',   # 33 mac address
			'B',   # 34 mac address
			'B',   # 35 mac address
			'B',   # 36 mac address lo
			'B',   # extra
		]), *data)
	
	@classmethod
	def decode(cls, address, data):
		if(len(data) == 207):
			data += '\x00'
		parts = struct.unpack(''.join([
			'!',
			'8s',  # 1 header
			'H',   # 2 opcode
			'4B',  # 3 ip address
			'H',   # 4 port
			'BB',  # 5,6 versioninfo hi,lo
			'BB',  # 7,8 net, sub
			'BB',  # 9,10 oem hi,lo
			'B',   # 11 UBEA version
			'B',   # 12 Status 1
			'H',   # 13 ESTA manufacturer code,
			'18s', # 14 Short Name
			'64s', # 15 Long Name
			'64s', # 16 Node Report
			'BB',  # 17,18 num ports hi,lo
			'4B',  # 19 port types array
			'4B',  # 20 good input array
			'4B',  # 21 good output array
			'4B',  # 22 sw input address
			'4B',  # 23 sw output address
			'B',   # 24 sw video
			'B',   # 25 sw macro
			'B',   # 26 sw remote
			'B',   # 27 not used
			'B',   # 28 not used
			'B',   # 29 not used
			'B',   # 30 style
			'B',   # 31 mac address hi
			'B',   # 32 mac address
			'B',   # 33 mac address
			'B',   # 34 mac address
			'B',   # 35 mac address
			'B',   # 36 mac address lo
			'B', #extra
			#'4B',  # 37 bind ip
			# 'B',   # 38 bind index
			# 'B',   # 39 status 2
			# '26B', # 40 filler
		]), data)
		return cls(parts, source=address)

class TodRequestPacket(ArtNetPacket):
	opcode = 0x0080
	
	def __init__(self, **kwargs):
		super(TodRequestPacket, self).__init__(**kwargs)
	
	def encode(self):
		proto_lo, proto_hi = lohi(PROTOCOL_VERSION)
		return ''.join([
			struct.pack('!8sHBB', HEADER, self.opcode, proto_hi, proto_lo),
			''.join([struct.pack('!B', 0) for x in range(7)]),
			''.join([struct.pack('!B', x) for x in [0, 0, 0, 0, 1, 1]]),
			''.join([struct.pack('!B', 0) for x in range(31)])
		])


