class FixtureGroup(object):
	fixtures = []

class Fixture(object):
	address = 1

class RGBControl(object):
	red_offset = 0
	green_offset = 1
	blue_offset = 2
	
	def setColor(self, hex):
		pass
	
	def configureRGBOffsets(self, r, g, b):
		self.red_offset = r
		self.green_offset = g
		self.blue_offset = b

class XYControl(object):
	has_fine_control = False
	x_offset = 0
	xfine_offset = None
	y_offset = 1
	xfine_offset = None
	
	def setPosition(self, x, y):
		pass
	
	def configureXYOffsets(self, x, y, xfine=None, yfine=None):
		self.has_fine_control = (xfine is None and yfine is None)
		if(self.has_fine_control):
			self.xfine_offset = xfine
			self.yfine_offset = yfine
		self.x_offset = x
		self.y_offset = y

class StrobeControl(object):
	strobe_offset = 4
	
	def setStrobe(self, speed):
		pass

class ProgramControl(object):
	program_offset = 5
	
	def setProgram(self, program):
		pass

class IntensityControl(object):
	intensity_offset = 6
	intensityfine_offset = None

#example code
fixture.setColor('#fff')
fixture.setPosition(0.5, 0.2)
fixture.setIntensity(0.9)
fixture.strobeSpeed(10) #ms?
fixture[0].setColor('#f00') # subfixtures
fixture.setMacro('short-fade')
fxiture.programSpeed(10) #ms?