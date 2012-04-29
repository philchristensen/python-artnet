class Fixture(object):
	def __init__(self, address, count):
		self.address = address
		self.count = count
		self.channels = []
		self.rgb = ()
		
		for i in range(count):
			self.channels[i] = Channel()
	
	def __setitem__(self, channel, value):
		if not(isinstance(value, int)):
			raise TypeError("Invalid DMX value: %r" % value)
		if(value < 0 or value > 255):
			raise ValueError("Invalid DMX value: %r " % value)
		if(channel < 0 or channel > self.count):
			raise ValueError("Invalid DMX channel: %r " % channel)
		self.channels[channel].value = value
	
	def __getitem__(self, index):
		return self.channels[index]
	
	def setRGBChannel(r=0, g=1, b=2):
		self.rgb = (r, g, b)
	
	def setColor(r, g, b):
		if not(rgb):
			raise RuntimeError("No RGB channels defined for this fixture.")
		self[self.rgb[0]] = r
		self[self.rgb[1]] = g
		self[self.rgb[2]] = b

class Channel(object):
	def __init__(self, level=0):
		self.level = level