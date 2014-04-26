import sys
import logging
import code

from artnet import dmx, rig

log = logging.getLogger(__name__)

def main(config, controller=None):
	log.info("Running script %s" % __name__)
	controller = dmx.Controller(config.get('base', 'address'), bpm=60)
	controller.start()
	
	def _runner(scriptname):
		if(scriptname == 'shell'):
			log.error("Can't create nested shells.")
			return
		with controller.autocycle:
			from artnet import scripts
			scripts.run(scriptname, config, controller)
	
	def _watch(r):
		def __watch(fixture, clock):
			c = clock()
			while(c['running']):
				yield fixture.getFrame()
				c = clock()
		controller.add(__watch(r.groups['all'], controller.get_clock()))
	
	default_rig = rig.get_default_rig()
	local = dict(
		run = _runner,
		ctl = controller,
		rig = default_rig,
		watch = _watch,
		blackout = lambda: _runner('all_channels_blackout'),
	)
	
	# try:
	# 	import readline
	# except ImportError, e:
	# 	pass
	# else:
	# 	# We don't have to wrap the following import in a 'try', because
	# 	# we already know 'readline' was imported successfully.
	# 	import rlcompleter
	# 	readline.set_completer(rlcompleter.Completer(local).complete)
	# 	if(sys.platform == 'darwin'):
	# 		readline.parse_and_bind ("bind ^I rl_complete")
	# 	else:
	# 		readline.parse_and_bind("tab:complete")
	
	code.interact(local=local)

