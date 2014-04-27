import socket, struct, itertools, time, logging

from artnet import dmx
from artnet import OPCODES, NODE_REPORT_CODES, STYLE_CODES

import bitstring

log = logging.getLogger(__name__)

class ArtNetPacket(object):
	opcode = None
	schema = []
	
	opcode_map = dict()
	header = 'Art-Net\0'
	protocol_version = 14
	
	@classmethod
	def register(cls, packet_class):
		cls.opcode_map[packet_class.opcode] = packet_class
		return packet_class
	
	@classmethod
	def decode(cls, address, data):
		[opcode] = struct.unpack('!H', data[8:10])
		if(opcode not in cls.opcode_map):
			raise NotImplementedError('%x' % opcode)
		
		klass = cls.opcode_map[opcode]
		b = bitstring.BitStream(bytes=data)
		fields = dict()
		for name, fmt in klass.schema:
			accessor = getattr(klass, 'parse_%s' % name, None)
			if(callable(accessor)):
				fields[name] = accessor(b, fmt)
			else:
				fields[name] = b.read(fmt)
		
		p = klass(address=fields.get('address'))
		for k,v in fields.items():
			setattr(p, k, v)
		
		return p

	def __init__(self, address=None, sequence=0, physical=0, universe=0):
		self.address = address
		self.sequence = sequence
		self.physical = physical
		self.universe = universe
		
		for name, fmt in self.schema:
			if not(hasattr(self, name)):
				setattr(self, name, None)
	
	def __str__(self):
		return '<%(klass)s from %(address)s:%(universe)s/%(physical)s>' % dict(
			klass    = self.__class__.__name__,
			address  = self.address,
			universe = self.universe,
			physical = self.physical,
		)
	
	def encode(self):
		fields = []
		for name, fmt in self.schema:
			accessor =  getattr(self, 'format_%s' % name, 0)
			if(callable(accessor)):
				value = accessor()
			else:
				value = getattr(self, name)
			fields.append([name, fmt, value])
		
		fmt = ', '.join(['='.join([f,n]) for n,f,v in fields])
		data = dict([(n,v) for n,f,v in fields])
		return bitstring.pack(fmt, **data).tobytes()
	
@ArtNetPacket.register
class DmxPacket(ArtNetPacket):
	opcode = OPCODES['OpDmx']
	schema = (
		('header', 'bytes:8'),
		('opcode', 'int:16'),
		('protocol_version', 'uintbe:16'),
		('sequence', 'int:8'),
		('physical', 'int:8'),
		('universe', 'uintbe:16'),
		('length', 'uintbe:16'),
		('framedata', 'bytes:512')
	)
	
	def __init__(self, frame=None, **kwargs):
		super(DmxPacket, self).__init__(**kwargs)
		self.frame = frame or dmx.Frame()
	
	@classmethod
	def parse_framedata(cls, b, fmt):
		return dmx.Frame([ord(x) for x in b.read('bytes:512')])
	
	def format_length(self):
		return len(self.frame)
	
	def format_framedata(self):
		return ''.join([chr(i or 0) for i in self.frame])
	
	def __str__(self):
		return '<DMX(%(sequence)s): %(channels)s>' % dict(
			sequence = self.sequence,
			channels = ', '.join([
				'%s: %s' % (
					address + 1,
					self.frame[address]
				) for address in range(len(self.frame)) if self.frame[address]
			])
		)
		
@ArtNetPacket.register
class PollPacket(ArtNetPacket):
	opcode = OPCODES['OpPoll']
	schema = (
		('header', 'bytes:8'),
		('opcode', 'int:16'),
		('protocol_version', 'uintbe:16'),
		('talktome', 'int:8'),
		('priority', 'int:8')
	)
	
	def __init__(self, talktome=0x02, priority=0, **kwargs):
		super(PollPacket, self).__init__(**kwargs)
		self.talktome = talktome
		self.priority = priority

@ArtNetPacket.register
class PollReplyPacket(ArtNetPacket):
	opcode = OPCODES['OpPollReply']
	counter = 0
	
	short_name = 'python-artnet'
	long_name = 'https://github.com/philchristensen/python-artnet.git'
	esta_manufacturer = 'PA'
	version = 1
	universe = 0
	status1 = 2
	status2 = bitstring.Bits(bin='00000000')
	num_ports = 4
	good_input = bitstring.Bits(bin='00000000')
	good_output = bitstring.Bits(bin='00000000')
	style = STYLE_CODES['StNode']
	
	schema = (
		('header', 'bytes:8'),
		('opcode', 'int:16'),
		('protocol_version', 'uintbe:16'),
		('ip_address', 'int:8,int:8,int:8,int:8'),
		('port', 'int:16'),
		('version_info', 'uintbe:16'),
		('net_switch', 'int:8'),
		('sub_switch', 'int:8'),
		('oem', 'uintbe:16'),
		('ubea_version', 'int:8'),
		('status1', 'int:8'),
		('esta_manufacturer', 'uintle:16'),
		('short_name', 'bin:18'),
		('long_name', 'bin:64'),
		('node_report', 'bin:64'),
		('num_ports', 'uintbe:16'),
		('port_types', 'int:8,int:8,int:8,int:8'),
		('good_input', 'int:8,int:8,int:8,int:8'),
		('good_output', 'int:8,int:8,int:8,int:8'),
		('switch_in', 'int:8'),
		('switch_out', 'int:8'),
		('switch_video', 'int:8'),
		('switch_macro', 'int:8'),
		('switch_remote', 'int:8'),
		('spare1', 'int:8'),
		('spare2', 'int:8'),
		('spare3', 'int:8'),
		('style', 'int:8'),
		('mac_hi', 'int:8'),
		('mac', 'int:8,int:8,int:8,int:8'),
		('mac_lo', 'int:8'),
		('bind_ip', 'int:8,int:8,int:8,int:8'),
		('bind_index', 'int:8'),
		('status2', 'int:8'),
		('filler', 'bytes')
	)
	
	def __init__(self, **kwargs):
		super(PollReplyPacket, self).__init__(**kwargs)
		PollReplyPacket.counter += 1
	
	def format_ip_address(self):
		address = socket.gethostbyname(socket.gethostname())
		return ''.join([chr(int(x)) for x in address.split('.')])
	
	@classmethod
	def parse_ip_address(cls, b, fmt):
		address = b.readlist(fmt)
		return '.'.join([ord(x) for x in address])
		
	def format_node_report(self):
		return "#0001 [%s] Power On Tests successful" % PollReplyPacket.counter
	
	def format_port_types(self):
		return '\0\0\0\0'
	
	def format_good_input(self):
		return '\0\0\0\0'
	
	def format_good_output(self):
		return '\0\0\0\0'
	
	def format_mac(self):
		return '\0\0\0\0'
	
	def format_bind_ip(self):
		return '\0\0\0\0'
	

@ArtNetPacket.register
class TodRequestPacket(ArtNetPacket):
	opcode = OPCODES['OpTodRequest']
	schema = (
		('header', 'bytes:8'),
		('opcode', 'int:16'),
		('protocol_version', 'uintbe:16'),
		('filler1', 'int:8'),
		('filler2', 'int:8'),
		('spare1', 'int:8'),
		('spare2', 'int:8'),
		('spare3', 'int:8'),
		('spare4', 'int:8'),
		('spare5', 'int:8'),
		('spare6', 'int:8'),
		('spare7', 'int:8'),
		('net', 'int:8'),
		('command', 'int:8'),
		('addcount', 'int:8'),
		('address', 'int:8')
	)
