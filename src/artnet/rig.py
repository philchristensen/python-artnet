from artnet import fixtures

import os.path
import yaml
import logging
import pkg_resources as pkg

from artnet import dmx

log = logging.getLogger(__name__)

_default_rig = None
def get_default_rig():
	global _default_rig
	if(_default_rig is None):
		_default_rig = load(os.path.expanduser("~/.artnet-rig.yaml"))
	return _default_rig

def load(config_path):
	rig = Rig()
	with open(config_path, 'r') as f:
		rig_data = yaml.safe_load(f)
	
	rig.name = rig_data['name']
	for name, f in rig_data['fixtures'].items():
		rig.fixtures[name] = fixtures.Fixture.create(f['address'], f['config'])
	
	for name, groups in rig_data['groups'].items():
		rig.groups[name] = fixtures.FixtureGroup([
			rig.fixtures[g] for g in groups
		])
	return rig

class Rig(object):
	def __init__(self, name=None):
		self.name = repr(self)
		self.groups = {}
		self.fixtures = {}
