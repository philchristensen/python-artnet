import sys

from cement.core import backend, foundation, controller, handler

logo_ascii = """
           _   _                         _            _
 _ __ _  _| |_| |_  ___ _ _ ___ __ _ _ _| |_ _ _  ___| |_ 
| '_ \ || |  _| ' \/ _ \ ' \___/ _` | '_|  _| ' \/ -_)  _|
| .__/\_, |\__|_||_\___/_||_|  \__,_|_|  \__|_||_\___|\__|
|_|   |__/
"""

defaults = backend.defaults('base')
defaults['base']['address'] = '<broadcast>'

class ArtnetBaseController(controller.CementBaseController):
	class Meta:
		label = 'base'
		description = "%s\nBasic artnet protocol support." % logo_ascii
		
		arguments = [
			(['-a', '--address'], dict(action='store', help='Address of an artnet interface.')),
		]

	@controller.expose(hide=True)
	def default(self):
		self.app.args.print_help()
	
	@controller.expose(help="Send a blackout command to a particular interface.")
	def blackout(self):
		from artnet.scripts import all_channels_blackout as blackout
		blackout.main(self.config.get('base', 'address'))
	
	@controller.expose(help="This command is not yet implemented.")
	def shell(self):
		self.log.error("Shell not yet implemented.")

class ArtnetScriptController(controller.CementBaseController):
	class Meta:
		label = 'script'
		description = "Artnet scripting support."
		arguments = [
			(['-a', '--address'], dict(action='store', help='Address of an artnet interface.')),
			(['scriptname'], dict(action='store', help='Name of script to run.')),
		]

	@controller.expose(help="Run a named lighting script.")
	def default(self):
		name = self.app.pargs.scriptname
		mod = __import__('artnet.scripts', globals(), locals(), [name], -1)
		getattr(mod, name).main(self.config.get('base', 'address'))

class ArtnetApp(foundation.CementApp):
	class Meta:
		label = 'artnet'
		config_defaults = defaults
		arguments_override_config = True
		base_controller = ArtnetBaseController

def main():
	app = ArtnetApp()
	handler.register(ArtnetScriptController)
	
	try:
		app.setup()
		app.run()
	finally:
		app.close()