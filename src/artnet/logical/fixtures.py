class FixtureGroup(object):
	fixtures = []

class Fixture(object):
	address = 1
	controls = []
	
	def getState(self):
		channels = [None] * 512
		for control in self.controls:
			for offset, value in control.getLevels():
				if(value is None):
					continue
				channels[address + offset] = value
		return (address, channels)
	
	def addControl(control):
		pass

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
	
	def getLevels(self):
		rgb = [None] * 512
		rgb[self.red_offset] = self.red_level
		rgb[self.green_offset] = self.green_level
		rgb[self.blue_offset] = self.blue_level
		return rgb

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
	
	def getLevels(self):
		xy = [None] * 512
		xy[self.x_offset] = self.x_level
		xy[self.y_offset] = self.y_level
		if(self.has_fine_control):
			xy[self.xfine_offset] = self.xfine_level
			xy[self.yfine_offset] = self.yfine_level
		return xy

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

#example config
{
	"name": "ADJ MegaBar RGB50",
	"rgb_offsets" : {
		"red": 0,
		"blue": 1,
		"green": 2,
	},
	"program_channel": {
		"offset": 3,
		"type": "color",
		"macro": {
			"white": 255,
		}
	},
	"strobe_offset": 4,
	"program_channel": {
		"offset": 5,
		"type": "program",
		"macro": {
			"slow-fade": 127,
		}
	},
	"intesity_offset": 6
}

#example code
fixture.setColor('#fff')
fixture.setPosition(0.5, 0.2)
fixture.setIntensity(0.9)
fixture.strobeSpeed(10) #ms?
fixture[0].setColor('#f00') # subfixtures
fixture.setMacro('short-fade')
fixture.programSpeed(10) #ms?