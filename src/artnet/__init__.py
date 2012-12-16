import sys, socket, logging

from artnet import packet

log = logging.getLogger(__name__)

def send_dmx(address, channels):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.bind(('', packet.ARTNET_PORT))
	
	p = packet.DmxPacket()
	for index in range(len(channels)):
		p[index] = channels[index]
	
	log.info(p)
	
	sock.sendto(p.encode(), (address, packet.ARTNET_PORT))
	sock.close()
