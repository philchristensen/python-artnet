import unittest, copy

from artnet import packet

POLL_PACKET = ''.join([
	"Art-Net\x00",  # ID[8] (Int8)
	"\x00\x20",     # OpCode (Int16)
	"\x00", "\x0e", # ProtVerHi, ProtVerLo (Int8)
	"\x02",         # TalkToMe (Int8)
	"\x00",         # Priority (Int8)
])

TOD_REQUEST = ''.join([
	"Art-Net\x00",           # ID[8] (Int8)
	"\x00\x80",              # OpCode (Int16)
	"\x00", "\x0e",          # ProtVerHi, ProtVerLo (Int8)
	"\x00",  "\x00",         # Filler1, Filler2 (Int8)
	"".join(["\x00"] * 7),   # Spare1-7 (Int8)
	"\x00", # Net (Int8)
	"\x00", # Command (Int8)
	"\x01", # AddCount (Int8)
	"\x01", ''.join(["\x00"] * 31), # Address[31] (Int8)
])

BLACKOUT_PACKET = ''.join([
	"Art-Net\x00",  # ID[8] (Int8)
	"\x00P",        # OpCode (Int16)
	"\x00", "\x0e", # ProtVerHi, ProtVerLo (Int8)
	"\x00",         # Sequence (Int8)
	"\x00",         # Physical (Int8)
	"\x00", "\x00", # SubUni, Net (Int8)
	"\x00", "\x02", # LenHi, LenLo (Int8)
	"".join(["\x00"] * 512)
])

U30_BLACKOUT_PACKET = ''.join([
	"Art-Net\x00",  # ID[8] (Int8)
	"\x00P",        # OpCode (Int16)
	"\x00", "\x0e", # ProtVerHi, ProtVerLo (Int8)
	"\x00",         # Sequence (Int8)
	"\x00",         # Physical (Int8)
	"\x00", "\x1e", # SubUni, Net (Int8)
	"\x00", "\x02", # LenHi, LenLo (Int8)
	"".join(["\x00"] * 512)
])

WHITEOUT_PACKET = ''.join([
	"Art-Net\x00",  # ID[8] (Int8)
	"\x00P",        # OpCode (Int16)
	"\x00", "\x0e", # ProtVerHi, ProtVerLo (Int8)
	"\x00",         # Sequence (Int8)
	"\x00",         # Physical (Int8)
	"\x00", "\x00", # SubUni, Net (Int8)
	"\x00", "\x02", # LenHi, LenLo (Int8)
	"".join(["\xff"] * 512)
])

class TestPacket(unittest.TestCase):
	def tearDown(self):
		packet.reset_sequence()
	
	def test_sequence(self):
		p = packet.DmxPacket()
		x = p.encode()
		self.assertEqual(len(x), len(BLACKOUT_PACKET))
		self.assertEqual(x, BLACKOUT_PACKET)
		
		b = copy.copy(BLACKOUT_PACKET)
		b = b[:12] + '\x01' + b[13:]
		
		p = packet.DmxPacket()
		x = p.encode()
		self.assertEqual(len(x), len(b))
		self.assertEqual(x, b)
		
		b = copy.copy(BLACKOUT_PACKET)
		b = b[:12] + '\x02' + b[13:]
		
		p = packet.DmxPacket()
		x = p.encode()
		self.assertEqual(len(x), len(b))
		self.assertEqual(x, b)
	
	def test_poll(self):
		p = packet.PollPacket()
		x = p.encode()
		self.assertEqual(len(x), len(POLL_PACKET))
		self.assertEqual(x, POLL_PACKET)
	
	def test_tod_request(self):
		p = packet.TodRequestPacket()
		x = p.encode()
		self.assertEqual(len(x), len(TOD_REQUEST))
		self.assertEqual(x, TOD_REQUEST)
	
	def test_blackout(self):
		p = packet.DmxPacket()
		x = p.encode()
		self.assertEqual(len(x), len(BLACKOUT_PACKET))
		self.assertEqual(x, BLACKOUT_PACKET)
	
	def test_whiteout(self):
		p = packet.DmxPacket()
		for i in range(512):
			p[i] = 255
		x = p.encode()
		self.assertEqual(len(x), len(WHITEOUT_PACKET))
		self.assertEqual(x, WHITEOUT_PACKET)
	
	def test_universe_30(self):
		p = packet.DmxPacket(universe=30)
		x = p.encode()
		self.assertEqual(len(x), len(U30_BLACKOUT_PACKET))
		self.assertEqual(x, U30_BLACKOUT_PACKET)
	
