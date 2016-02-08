import time
import math
from helpers import *
from module import Module
from noise import snoise2

class PaletteStop:
	def __init__(self, pos, color):
		self.pos = pos
		self.color = color

palette = [
	PaletteStop(0.0, [0, 0, 0]),
	PaletteStop(0.1, [0, 0, 0]),
	PaletteStop(0.15, [198, 101, 0]),
	PaletteStop(0.4, [255, 191, 0]),
	PaletteStop(0.55, [255, 255, 255]),
	PaletteStop(1.0, [255, 255, 255])
]

def map(value, old_lower, old_upper, new_lower, new_upper):
	return max(new_lower, min(new_upper, new_lower + (new_upper - new_lower) * (value - old_lower) / (old_upper - old_lower)))

class Fire(Module):
	def __init__(self, screen):
		super(Fire, self).__init__(screen)

		self.presets = 100
		self.gradient = [self.get_color(1.0 * i / self.presets) for i in range(self.presets + 1)]

	def get_fire_value(self, x, y, t):
		stretch = 2
		exp = 1.5

		value = map(snoise2(x * 3, stretch**(-1.0 / exp) * (1.0 - ((1.0 - y) * stretch)**exp) * 0.8 - t * 0.7, 4), -0.72, 0.7, 0, 1)
		value = value ** 1.5

		value *= 1.0 - y**1.5

		return value

	def get_color(self, value):
		stop1 = 0;

		while (palette[stop1 + 1].pos < value):
			stop1 += 1

		blend = 1.0 - (value - palette[stop1].pos) / (palette[stop1 + 1].pos - palette[stop1].pos)

		r = blend * palette[stop1].color[0] + (1.0 - blend) * palette[stop1 + 1].color[0]
		g = blend * palette[stop1].color[1] + (1.0 - blend) * palette[stop1 + 1].color[1]
		b = blend * palette[stop1].color[2] + (1.0 - blend) * palette[stop1 + 1].color[2]

		return Color(int(r), int(g), int(b))

	def get_color_quick(self, value):
		return self.gradient[int(value * self.presets)]
	
	def draw(self):
		t = time.clock()
		for x in range(16):
			for y in range(16):
				self.screen.pixel[x][y] = self.get_color_quick(self.get_fire_value(x / 16.0, 1.0 - y / 16.0, t))

		self.screen.update()
	
	def tick(self):
		self.draw()