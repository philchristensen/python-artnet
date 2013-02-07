import sys
import logging
import code

from artnet import dmx

log = logging.getLogger(__name__)

def main(config):
	controller = dmx.Controller(config.get('base', 'address'), bpm=60)
	controller.start()
	
	def _script_runner(scriptname):
		if(scriptname == 'shell'):
			log.error("Can't create nested shells.")
			return
		from artnet import scripts
		scripts.run(scriptname, config, controller)
	
	local = dict(
		ctl = controller,
		run = _script_runner
	)
	
	try:
		import readline
	except ImportError, e:
		pass
	else:
		# We don't have to wrap the following import in a 'try', because
		# we already know 'readline' was imported successfully.
		import rlcompleter
		readline.set_completer(rlcompleter.Completer(local).complete)
		if(sys.platform == 'darwin'):
			readline.parse_and_bind ("bind ^I rl_complete")
		else:
			readline.parse_and_bind("tab:complete")
	
	code.interact(local=local)

