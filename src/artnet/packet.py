import socket
import struct
import time
import logging
import uuid

from artnet import OPCODES, NODE_REPORT_CODES, STYLE_CODES, STANDARD_PORT

import bitstring

log = logging.getLogger(__name__)

class ArtNetPacket(object):
	opcode = None
	schema = ()
	
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
		
		p = klass(address=address)
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
				setattr(self, name, 0)
	
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
			accessor =  getattr(self, 'format_%s' % name, '\0')
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
		from artnet import dmx
		self.frame = frame or dmx.Frame()
	
	@classmethod
	def parse_framedata(cls, b, fmt):
		from artnet import dmx
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
	
	port = STANDARD_PORT
	
	short_name = 'python-artnet'
	long_name = 'https://github.com/philchristensen/python-artnet.git'
	style = STYLE_CODES['StController']
	esta_manufacturer = 'PA'
	version = 1
	universe = 0
	status1 = 2
	status2 = bitstring.Bits('0b0111').int
	
	num_ports = 0
	port_types = '\0\0\0\0'
	good_input = '\0\0\0\0'
	good_output = '\0\0\0\0'
	
	bind_ip = '\0\0\0\0'
	mac_address = uuid.getnode()
	
	schema = (
		('header', 'bytes:8'),
		('opcode', 'int:16'),
		('ip_address', 'bytes:4'),
		('port', 'int:16'),
		('version', 'uintbe:16'),
		('net_switch', 'int:8'),
		('sub_switch', 'int:8'),
		('oem', 'uintbe:16'),
		('ubea_version', 'int:8'),
		('status1', 'int:8'),
		('esta_manufacturer', 'bytes:2'),
		('short_name', 'bytes:18'),
		('long_name', 'bytes:64'),
		('node_report', 'bytes:64'),
		('num_ports', 'uintbe:16'),
		('port_types', 'bytes:4'),
		('good_input', 'bytes:4'),
		('good_output', 'bytes:4'),
		('switch_in', 'int:8'),
		('switch_out', 'int:8'),
		('switch_video', 'int:8'),
		('switch_macro', 'int:8'),
		('switch_remote', 'int:8'),
		('spare1', 'int:8'),
		('spare2', 'int:8'),
		('spare3', 'int:8'),
		('style', 'int:8'),
		('mac_address', 'uintle:48'),
		('bind_ip', 'bytes:4'),
		('bind_index', 'int:8'),
		('status2', 'int:8'),
		('filler', 'bytes')
	)
	
	def __init__(self, **kwargs):
		super(PollReplyPacket, self).__init__(**kwargs)
		PollReplyPacket.counter += 1
	
	def format_ip_address(self):
		address = socket.gethostbyname(socket.gethostname())
		return bitstring.pack('uint:8, uint:8, uint:8, uint:8', *[int(x) for x in address.split('.')]).bytes
	
	@classmethod
	def parse_ip_address(cls, b, fmt):
		b = bitstring.BitStream(bytes=b.read(fmt))
		address = b.readlist(','.join(['uint:8'] * 4))
		return '.'.join([str(x) for x in address])
		
	def format_short_name(self):
		return self.short_name[0:18].ljust(18)
	
	@classmethod
	def parse_short_name(cls, b, fmt):
		short_name = b.read(fmt)
		return short_name.strip()
	
	def format_long_name(self):
		return self.long_name[0:64].ljust(64)
	
	@classmethod
	def parse_long_name(cls, b, fmt):
		long_name = b.read(fmt)
		return long_name.strip()
	
	def format_node_report(self):
		node_report = "#0001 [%s] Power On Tests successful" % PollReplyPacket.counter
		return node_report[0:64].ljust(64)
	
	@classmethod
	def parse_node_report(cls, b, fmt):
		node_report = b.read(fmt)
		return node_report.strip()	

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
		# ('addr', 'int:8')
	)
