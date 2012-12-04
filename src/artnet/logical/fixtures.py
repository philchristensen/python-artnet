def load(address, fixturedef):
	f = Fixture(address)
	return f

class FixtureGroup(object):
	fixtures = []

class Fixture(object):
	address = 1
	controls = dict()
	
	def getState(self):
		return [x for c in self.controls.values() for x in c.getState()]
	
	def addControl(label, control):
		self.controls[label] = control

class RGBControl(object):
	red_offset = 0
	green_offset = 1
	blue_offset = 2
	red_level = 0
	green_level = 0
	blue_level = 0
	
	def setColor(self, hex):
		pass
	
	def configureRGBOffsets(self, r, g, b):
		self.red_offset = r
		self.green_offset = g
		self.blue_offset = b
	
	def getState(self):
		return [
			(self.red_offset, self.red_level),
			(self.green_offset, self.green_level),
			(self.blue_offset, self.blue_level)
		]

class XYControl(object):
	has_fine_control = False
	x_offset = 0
	xfine_offset = None
	y_offset = 1
	xfine_offset = None
	x_level = 0
	xfine_level = 0
	y_level = 0
	xfine_level = 0
	
	def setPosition(self, x, y):
		pass
	
	def configureXYOffsets(self, x, y, xfine=None, yfine=None):
		self.has_fine_control = (xfine is None and yfine is None)
		if(self.has_fine_control):
			self.xfine_offset = xfine
			self.yfine_offset = yfine
		self.x_offset = x
		self.y_offset = y
	
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
	strobe_offset = 4
	strobe_value = 0
	
	def configureStrobeOffset(self, strobe):
		self.strobe_offset = strobe
	
	def setStrobe(self, value):
		self.strobe_value = value
	
	def getState(self):
		return [
			(self.strobe_offset, self.strobe_value)
		]

class ProgramControl(object):
	program_offset = 5
	program_speed_offset = 4
	program_macros = dict()
	program_value = 5
	program_speed_value = 4
	
	def setMacro(self, label, value, speed):
		self.program_macros[label] = (value, speed)
	
	def configureProgramOffset(self, program):
		self.program_offset = program
	
	def setProgram(self, program):
		pass
	
	def getState(self):
		return [
			(self.program_offset, self.program_value)
			(self.program_speed_offset, self.program_speed_value)
		]

class IntensityControl(object):
	intensity_offset = 6
	intensityfine_offset = None
	intensity_value = 0
	intensityfine_value = 0
	
	def getState(self):
		fine = []
		if(intensityfine_offset is not None):
			fine = [
				(self.intensityfine_offset, self.intensityfine_value)
			]
		return [
			(self.intensity_offset, self.intensity_value)
		]

