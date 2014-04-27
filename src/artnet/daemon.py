import sys
import threading
import socket
import time
import logging
import json

import artnet
from artnet import packet, STANDARD_PORT, OPCODES, STYLE_CODES

log = logging.getLogger(__name__)

def main(config):
	log.info("Running script %s" % __name__)
	d = Poller(config.get('base', 'address'))
	d.run()

class Poller(threading.Thread):
	def __init__(self, address, nodaemon=False, runout=False):
		super(Poller, self).__init__()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		
		self.sock.bind(('', STANDARD_PORT))
		self.sock.settimeout(0.0)
		
		self.broadcast_address = '<broadcast>'
		self.last_poll = 0
		self.address = address

		self.nodaemon = nodaemon
		self.daemon = not nodaemon
		self.running = True

	def run(self):
		now = time.time()
		while(self.running):
			self.handle_artnet()
	
	def read_artnet(self):
		try:
			data, addr = self.sock.recvfrom(1024)
		except socket.error, e:
			time.sleep(0.1)
			return None
		
		return packet.ArtNetPacket.decode(addr, data)
	
	def handle_artnet(self):
		if(time.time() - self.last_poll >= 4):
			self.last_poll = time.time()
			self.send_poll()
		
		p = self.read_artnet()
		if(p is None):
			return
		
		log.debug("recv: %s" % p)
		if(p.opcode == OPCODES['OpPoll']):
			self.send_poll_reply(p)
	
	def send_dmx(self, frame):
		p = packet.DmxPacket(frame)
		self.sock.sendto(p.encode(), (self.address, STANDARD_PORT))
	
	def send_poll(self):
		p = packet.PollPacket(address=self.broadcast_address)
		self.sock.sendto(p.encode(), (p.address, STANDARD_PORT))
	
	def send_poll_reply(self, poll):
		ip_address = socket.gethostbyname(socket.gethostname())
		style = STYLE_CODES['StNode'] if isinstance(self, Poller) else STYLE_CODES['StController']
		
		r = packet.PollReplyPacket(address=self.broadcast_address)
		r.style = style
		
		log.debug("send: %s" % r)
		self.sock.sendto(r.encode(), (r.address, STANDARD_PORT))
		