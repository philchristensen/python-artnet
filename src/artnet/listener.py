import threading, socket, time

class ArtPollListener(threading.Thread):
	def __init__(self, sock):
		threading.Thread.__init__(self)
		self.running = False
		self.sock = sock
	
	def stop(self):
		self.running = False
	
	def run(self):
		from artnet import packet
		
		ip_address = socket.gethostbyname(socket.gethostname())
		last_poll = time.time()
		
		def _poll():
			p = packet.PollPacket(source=(ip_address, 6454))
			l = self.sock.sendto(p.encode(), ('192.168.1.255', packet.ARTNET_PORT))
			print 'poll packet: %s' % p
		
		self.sock.settimeout(0.0)
		self.running = True
		
		_poll()
		while(self.running):
			if(time.time() - last_poll >= 4):
				last_poll = time.time()
				_poll()
			
			try:
				data, addr = self.sock.recvfrom(1024)
			except socket.error, e:
				time.sleep(0.1)
				continue
			
			p = packet.ArtNetPacket.parse(addr, data)
			
			if(isinstance(p, packet.PollPacket)):
				r = packet.PollReplyPacket([], source=(ip_address, 6454))
				l = self.sock.sendto(r.encode(), ('192.168.1.255', packet.ARTNET_PORT))
