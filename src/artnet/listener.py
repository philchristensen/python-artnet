import sys
import threading
import socket
import time
import logging
import json

import artnet
from artnet import packet, dmx

log = logging.getLogger(__name__)

def main(config):
	log.info("Running script %s" % __name__)
	q = dmx.Controller(config.get('base', 'address'))
	q.run()
