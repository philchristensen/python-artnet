def hex_to_rgb(value):
	value = value.lstrip('#')
	lv = len(value)
	return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def rgb_to_hex(rgb):
	return '#%02x%02x%02x' % rgb

class FixtureGroup(object):
	fixtures = []

class Fixture(object):
	def __init__(self, address):
		self.address = address
		self.controls = dict()
	
	def configure(self, fixturedef):
		for klass in available_controls:
			if klass is ProgramControl:
				for channel in fixturedef.get('program_channels', []):
					ctrl = klass()
					label = ctrl.configure(channel, fixturedef)
					self.addControl(label, ctrl)
			else:
				ctrl = klass()
				label = ctrl.configure(fixturedef)
				self.addControl(label, ctrl)
	
	def getState(self):
		return [x for clist in self.controls.values() for c in clist for x in c.getState()]
	
	def addControl(self, label, control):
		self.controls.setdefault(label, []).append(control)
	
	def setColor(self, hexcode):
		for ctrl in self.controls.get('rgb', []):
			ctrl.setColor(hexcode)
	
	def setIntensity(self, value):
		for ctrl in self.controls.get('intensity', []):
			ctrl.setIntensity(value)

class RGBControl(object):
	def __init__(self):
		self.red_offset = None
		self.green_offset = None
		self.blue_offset = None
		self.red_level = 0
		self.green_level = 0
		self.blue_level = 0
	
	def configure(self, fixturedef):
		self.red_offset = fixturedef['rgb_offsets']['red']
		self.green_offset = fixturedef['rgb_offsets']['green']
		self.blue_offset = fixturedef['rgb_offsets']['blue']
		return 'rgb'
	
	def setColor(self, hexcode):
		r, g, b = hex_to_rgb(hexcode)
		self.red_level = r
		self.green_level = g
		self.blue_level = b
	
	def getState(self):
		return [
			(self.red_offset, self.red_level),
			(self.green_offset, self.green_level),
			(self.blue_offset, self.blue_level)
		]

class XYControl(object):
	def __init__(self):
		self.has_fine_control = False
		self.x_offset = None
		self.xfine_offset = None
		self.y_offset = None
		self.xfine_offset = None
		self.x_level = 0
		self.xfine_level = 0
		self.y_level = 0
		self.xfine_level = 0
	
	def setPosition(self, x, y):
		pass
	
	def configure(self, fixturedef):
		# self.has_fine_control = (xfine is None and yfine is None)
		# self.x_offset = x
		# self.y_offset = y
		# if(self.has_fine_control):
		# 	self.xfine_offset = xfine
		# 	self.yfine_offset = yfine
		return 'xy'
	
	def getState(self):
		xy = [
			(self.x_offset, self.x_level),
			(self.y_offset, self.y_level)
		]
		if(self.has_fine_control):
			xy.append((self.xfine_offset, self.xfine_level))
			xy.append((self.yfine_offset, self.yfine_level))
		return xy

class StrobeControl(object):
	def __init__(self):
		self.strobe_offset = None
		self.strobe_value = 0
	
	def configure(self, fixturedef):
		self.strobe_offset = fixturedef['strobe_offset']
		return 'strobe'
	
	def setStrobe(self, value):
		self.strobe_value = value
	
	def getState(self):
		return [
			(self.strobe_offset, self.strobe_value)
		]

class ProgramControl(object):
	def __init__(self):
		self.program_offset = None
		self.program_speed_offset = None
		self.program_type = None
		self.program_macros = dict()
		self.program_value = 0
		self.program_speed_value = 0
	
	def setMacro(self, label, value, speed):
		self.program_macros[label] = (value, speed)
	
	def configure(self, channel, fixturedef):
		self.program_offset = channel['offset']
		self.program_type = channel['type']
		self.program_speed_offset = channel.get('speed_offset', fixturedef.get('strobe_offset', None))
		for label, conf in channel.get('macros', {}).items():
			if(isinstance(conf, int)):
				self.setMacro(label, conf, None)
			else:
				self.setMacro(label, conf['value'], conf['speed'])
		return 'program'
	
	def setProgram(self, label, speed=None):
		pass
	
	def getState(self):
		return [
			(self.program_offset, self.program_value),
			(self.program_speed_offset, self.program_speed_value)
		]

class IntensityControl(object):
	def __init__(self):
		self.intensity_offset = None
		self.intensityfine_offset = None
		self.intensity_value = 0
		self.intensityfine_value = 0
	
	def configure(self, fixturedef):
		self.intensity_offset = fixturedef['intensity_offset']
		self.intensityfine_offset = fixturedef.get('intensityfine_offset', None)
		return 'intensity'
	
	def setIntensity(self, value):
		self.intensity_value = value
	
	def getState(self):
		fine = []
		if(self.intensityfine_offset is not None):
			fine = [
				(self.intensityfine_offset, self.intensityfine_value)
			]
		return fine + [
			(self.intensity_offset, self.intensity_value)
		]

available_controls = [
	RGBControl,
	XYControl,
	StrobeControl,
	ProgramControl,
	IntensityControl
]