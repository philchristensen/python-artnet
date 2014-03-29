import time

from artnet import dmx, packet

def main(config, controller=None):
	f = dmx.Frame()
	p = packet.DmxPacket(f)
	with open('/Users/phil/Desktop/blackout-py.dmx', 'w') as f:
		f.write(p.encode())


