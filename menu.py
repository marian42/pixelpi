from menu.menuitems import menu_items
from screenfactory import create_screen
from gamepadfactory import create_gamepad
import pygame
from gamepad.virtualgamepad import *
import time
import math
from helpers import *

class Menu(object):
	def __init__(self, items):
		self.screen = create_screen()
		self.gamepad = create_gamepad()
		self.gamepad.on_press.append(self.on_key_down)

		self.index = 0		
		self.items = items
		self.module = None		

		self.reset(redraw = False)
		self.resume_animation()

	def reset(self, redraw = True):
		self.dir = 0
		self.offset = 0
		self.zoom = 1
		self.brightness = 1
		if redraw:
			self.draw()

	def draw_on_screen(self, x, y, zoom, graphic):
		size = int(8 * zoom)
		for line in range(size):
			for pixel in range(size):
				source = Point(int(pixel / zoom), int(line / zoom))
				target = Point(int(x - size * 0.5 + pixel), int(y - size * 0.5 + line))
				if target.x >= 0 and target.x < 16 and target.y >= 0 and target.y < 16:
					c = graphic[source.x][source.y]
					self.screen.pixel[target.x][target.y] = Color(c.r * self.brightness, c.g * self.brightness, c.b * self.brightness)

	def draw_scrollbar(self):
		size = int(math.floor(16 / len(self.items)))
		start = int(math.floor((16 - size) * self.index / (len(self.items) - 1)))

		for x in range(size):
			self.screen.pixel[(start + x - int(size * self.offset) + 16) % 16][15] = Color(80 * self.brightness, 80 * self.brightness, 80 * self.brightness)


	def draw(self):
		if self.module != None:
			return

		self.screen.clear()
		self.draw_scrollbar()

		self.draw_on_screen(8 + int(self.offset * 12), 8, self.zoom, self.items[self.index].get_preview())

		if self.dir != 0:
			self.draw_on_screen(8 + int(self.offset * 12) - self.dir * 12, 8, self.zoom, self.items[(self.index - self.dir + len(self.items)) % len(self.items)].get_preview())

		self.screen.update()

	def ease(self, x):
		return x

	def tick(self):
		if (self.dir != 0):
			self.offset = self.dir * self.ease((1 - (time.clock() - self.start) / (self.end - self.start)))
			
			if (time.clock() > self.end):
				self.offset = 0
				self.dir = 0

			self.draw()

	def move(self, direction):
		if self.dir != 0:
			return

		self.index = (self.index + direction + len(self.items)) % len(self.items)
		self.dir = direction
		self.start = time.clock()
		self.end = self.start + 0.3

	def on_key_down(self, key):
		if self.module != None:
			if key == 10:
				self.stop()
			return

		if key == self.gamepad.RIGHT:
			self.move(1)
		if key == self.gamepad.LEFT:
			self.move(-1)
		if key == 1:
			self.launch()

	def stop(self):
		self.module.stop()
		pygame.time.wait(200)
		self.module = None
		self.resume_animation()
		self.gamepad.on_press = [self.on_key_down]
		self.gamepad.on_release = []

	def launch(self):
		self.start_animation()
		self.module = self.items[self.index].get_module(self.screen, self.gamepad)
		self.module.start()

	def start_animation(self):
		start = time.clock()
		end = start + 1

		while time.clock () <= end:
			self.zoom = 1 + 16 * ((time.clock() - start) / (end - start)) ** 2
			self.brightness = min(1, 1 - ((time.clock() - start) / (end - start)))
			self.draw()
			pygame.time.wait(20)

		pygame.time.wait(100)
		self.reset(redraw = False)

	def resume_animation(self):
		start = time.clock()
		end = start + 0.5

		while time.clock () <= end:
			self.zoom = ((time.clock() - start) / (end - start))
			self.brightness = min(1, 1 * ((time.clock() - start) / (end - start)))
			
			self.draw()
			pygame.time.wait(20)

		self.reset()

if __name__ == '__main__':
	menu = Menu(menu_items)
	while True:
		menu.tick()
		pygame.time.wait(10)
		for event in pygame.event.get():
			instance.consume_event(event)