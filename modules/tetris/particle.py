from helpers import *

class Particle:
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.vy = 0
		self.color = color

	def step(self, dt):
		self.y += dt * self.vy
		self.vy += dt * 250

class Tetromino:
	def __init__(self, blocks, color):
		self.color = color
	
		self.width = 0
		self.height = 0
		for block in blocks:
			self.width = max(self.width, block.x + 1)
			self.height = max(self.height, block.y + 1)
		
		self.map = [[False for y in range(self.height)] for x in range(self.width)]
		for block in blocks:
			self.map[block.x][block.y] = True
			
	def rotate(self, amount = 1):
		if amount < 1:
			return self
		if amount > 1:
			return self.rotate(amount - 1).rotate()
			
		blocks = []
		for x in range(self.width):
			for y in range(self.height):
				if self.map[x][y]:
					blocks.append(Point(self.height - y - 1, x))
		return Tetromino(blocks, self.color)