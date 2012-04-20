import unittest

from artnet import packet

class TestPacket(unittest.TestCase):
	def tearDown(self):
		packet.reset_sequence()
	
	def test_header(self):
		p = packet.ArtNetPacket()
		self.assertEqual(p.encode(), 'Art-Net\x00P\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
		p = packet.ArtNetPacket()
		self.assertEqual(p.encode(), 'Art-Net\x00P\x00\x00\x0e\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00')
	
	def test_channel_1(self):
		p = packet.ArtNetPacket()
		p[1] = 255
		self.assertEqual(p.encode(), 'Art-Net\x00P\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
