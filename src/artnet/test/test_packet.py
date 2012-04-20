import unittest, copy

from artnet import packet

BLACKOUT_PACKET = ''.join([
	"Art-Net\x00",  # ID[8] (Int8)
	"P\x00",        # OpCode (Int16)
	"\x00", "\x0e", # ProtVerHi, ProtVerLo (Int8)
	"\x00",         # Sequence (Int8)
	"\x00",         # Physical (Int8)
	"\x00", "\x00", # SubUni, Net (Int8)
	"\x02", "\x00", # LenHi, LenLo (Int8)
	"".join(["\x00"] * 512)
])

U30_BLACKOUT_PACKET = ''.join([
	"Art-Net\x00",  # ID[8] (Int8)
	"P\x00",        # OpCode (Int16)
	"\x00", "\x0e", # ProtVerHi, ProtVerLo (Int8)
	"\x00",         # Sequence (Int8)
	"\x00",         # Physical (Int8)
	"\x1e", "\x00", # SubUni, Net (Int8)
	"\x02", "\x00", # LenHi, LenLo (Int8)
	"".join(["\x00"] * 512)
])

FIRST_FIXTURE_WHITE_PACKET = ''.join([
	"Art-Net\x00",  # ID[8] (Int8)
	"P\x00",        # OpCode (Int16)
	"\x00", "\x0e", # ProtVerHi, ProtVerLo (Int8)
	"\x00",         # Sequence (Int8)
	"\x00",         # Physical (Int8)
	"\x00", "\x00", # SubUni, Net (Int8)
	"\x02", "\x00", # LenHi, LenLo (Int8)
	"".join(["\xff"] * 3),
	"".join(["\x00"] * 509)
])

class TestPacket(unittest.TestCase):
	def tearDown(self):
		packet.reset_sequence()
	
	def test_sequence(self):
		p = packet.ArtNetPacket()
		x = p.encode()
		self.assertEqual(len(x), len(BLACKOUT_PACKET))
		self.assertEqual(x, BLACKOUT_PACKET)
		
		b = copy.copy(BLACKOUT_PACKET)
		b = b[:12] + '\x01' + b[13:]
		
		p = packet.ArtNetPacket()
		x = p.encode()
		self.assertEqual(len(x), len(b))
		self.assertEqual(x, b)
		
		b = copy.copy(BLACKOUT_PACKET)
		b = b[:12] + '\x02' + b[13:]
		
		p = packet.ArtNetPacket()
		x = p.encode()
		self.assertEqual(len(x), len(b))
		self.assertEqual(x, b)
	
	def test_blackout(self):
		p = packet.ArtNetPacket()
		x = p.encode()
		self.assertEqual(len(x), len(BLACKOUT_PACKET))
		self.assertEqual(x, BLACKOUT_PACKET)
	
	def test_first_fixture(self):
		p = packet.ArtNetPacket()
		p[0] = 255
		p[1] = 255
		p[2] = 255
		x = p.encode()
		self.assertEqual(len(x), len(FIRST_FIXTURE_WHITE_PACKET))
		self.assertEqual(x, FIRST_FIXTURE_WHITE_PACKET)
	
	def test_universe_30(self):
		p = packet.ArtNetPacket(universe=30)
		x = p.encode()
		self.assertEqual(len(x), len(U30_BLACKOUT_PACKET))
		self.assertEqual(x, U30_BLACKOUT_PACKET)
	
