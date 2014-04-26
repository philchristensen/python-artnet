import time, logging

from artnet import dmx, packet

log = logging.getLogger(__name__)

def main(config, controller=None):
	log.info("Running script %s" % __name__)
	f = dmx.Frame()
	p = packet.DmxPacket(f)
	with open('/Users/phil/Desktop/blackout-py.dmx', 'w') as f:
		f.write(p.encode())


