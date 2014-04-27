import logging

from artnet import daemon

log = logging.getLogger(__name__)

def main(config):
	log.info("Running script %s" % __name__)
	q = daemon.Poller(config.get('base', 'address'))
	q.run()
