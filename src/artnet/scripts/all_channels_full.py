from artnet import dmx

def main(config):
	q = dmx.Controller(config.get('base', 'address'), nodaemon=False)
	q.add(iter([[255] * 512]))
	q.start()

