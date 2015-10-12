import helpers

class AbstractScreen(object):
	def __init__(self, width = 16, height = 16):
		self.width = width
		self.height = height

		self.pixel = [[helpers.Color(0,0,0) for y in range(height)] for x in range(width)]
	
	def clear(self, color = helpers.Color(0,0,0)):
		for x in range(self.width):
			for y in range(self.height):
				self.pixel[x][y] = color

	def update(self):
		pass