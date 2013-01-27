from artnet import dmx

def main(config):
	q = dmx.Controller(config.get('base', 'address'), nodaemon=False)
	q.add(iter([[0] * 512]))
	q.start()

