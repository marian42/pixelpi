import time
import math
from helpers import *
from modules import Module

class Pie(Module):
	def __init__(self, screen):
		super(Pie, self).__init__(screen)

	def draw(self):
		self.screen.clear()
		
		start = time.clock() * 2.77 + math.sin(time.clock())
		end = time.clock() * 7.35 + 0.5 * math.pi
		distance = end - start
		start = start % (2 * math.pi)
		end = end % (2 * math.pi)

		invert = distance % (4 * math.pi) > 2 * math.pi
		if invert:
			buf = end
			end = start
			start = buf

		hue = (time.clock() * 0.01) % 1
		color = hsv_to_color(hue, 1, 1)

		for x in range(16):
			for y in range(16):
				r = ((x - 8)**2 + (y - 8)**2)**0.5
				if r == 0:
					r = 0.001
				angle = math.acos((x - 8) / r)
				if y - 8 < 0:
					angle = 2 * math.pi - angle
				if (angle > start and angle < end) or (end < start and (angle > start or angle < end)):
					self.screen.pixel[x][y] = color

		self.screen.update()
	
	def tick(self):
		self.draw()
