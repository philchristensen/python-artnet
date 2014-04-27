import sys
import threading
import socket
import time
import logging
import json

import artnet
from artnet import packet

log = logging.getLogger(__name__)

def main(config):
	address = config.get('base', 'address')
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', 6454))
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	l = ArtnetThread(sock, address)
	l.run()

class ArtnetThread(threading.Thread):
	def __init__(self, sock, broadcast_address):
		threading.Thread.__init__(self)
		self.running = False
		self.sock = sock
		self.broadcast_address = broadcast_address
	
	def stop(self):
		self.running = False
	
	def run(self):
		ip_address = socket.gethostbyname(socket.gethostname())
		last_poll = 0
		
		self.sock.settimeout(0.0)
		self.running = True
		
		while(self.running):
			if(time.time() - last_poll >= 4):
				last_poll = time.time()
				p = packet.PollPacket(address=(ip_address, artnet.STANDARD_PORT))
				self.sock.sendto(p.encode(), (self.broadcast_address, artnet.STANDARD_PORT))
			
			try:
				data, addr = self.sock.recvfrom(1024)
			except socket.error, e:
				time.sleep(0.1)
				continue
			
			p = packet.ArtNetPacket.decode(addr, data)
			
			if(p.opcode != artnet.OPCODES['OpDmx']):
				log.info("recv: %s" % p)
			
			if(isinstance(p, packet.PollPacket)):
				r = packet.PollReplyPacket(address=(ip_address, artnet.STANDARD_PORT))
				self.sock.sendto(r.encode(), (self.broadcast_address, artnet.STANDARD_PORT))
				log.info("send: %s" % r)
