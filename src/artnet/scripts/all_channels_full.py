import logging

from artnet import dmx

log = logging.getLogger(__name__)

def main(config, controller=None):
	log.info("Running script %s" % __name__)
	q = controller or dmx.Controller(config.get('base', 'address'), nodaemon=False)
	q.add(iter([[255] * 512]))
	if not controller:
		q.start()

