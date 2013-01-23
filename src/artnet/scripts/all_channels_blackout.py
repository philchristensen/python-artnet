from artnet import dmx

def main(address):
	q = dmx.Controller(address, nodaemon=False)
	q.add(iter([[0] * 512]))
	q.start()

