import sys

from cement.core import backend, foundation, controller, handler

logo_ascii = """           _   _                         _            _
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
		from artnet.scripts import blackout
		blackout.main(self.config.get('base', 'address'))
	
	@controller.expose(help="Send a halfup test command to a particular interface.")
	def halfup(self):
		from artnet.scripts import halfup
		halfup.main(self.config.get('base', 'address'))
	
	@controller.expose(help="this command does relatively nothing useful.")
	def shell(self):
		self.log.error("Shell not yet implemented.")

class ArtnetApp(foundation.CementApp):
	class Meta:
		label = 'artnet'
		config_defaults = defaults
		arguments_override_config = True
		base_controller = ArtnetBaseController

def main():
	app = ArtnetApp()
	
	try:
		app.setup()
		app.run()
	finally:
		app.close()