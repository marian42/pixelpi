import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from menu.menuitems import create_menu_items
from screenfactory import create_screen
import time
import math
from helpers import *
import config
import input

class Menu(object):
	def __init__(self, screen, items):
		self.screen = screen
		input.on_press.append(self.on_key_down)

		self.index = config.default_item_index
		self.items = items
		self.module = None

		self.reset(redraw = False)
		self.resume_animation()
		
		if len(input.available_input_methods) == 0:
			self.launch()

	def reset(self, redraw = True):
		self.dir = 0
		self.offset = 0
		self.zoom = 1
		self.brightness = 1
		if redraw:
			self.draw()

	def draw_on_screen(self, x, y, zoom, graphic):		
		if zoom == 0:
			return
		if self.brightness == 1 and zoom == 1:
			for source_x in range(8):
				for source_y in range(8):
					target = Point(source_x + x - 4, source_y + y - 4)
					if target.x >= 0 and target.x < 16 and target.y >= 0 and target.y < 16:
						self.screen.pixel[target.x][target.y] = rgb_to_int(graphic[source_x][source_y])
			return

		for target_x in range(16):
			for target_y in range(16):
				source = Point(int((target_x - x) / zoom + 4), int((target_y - y) / zoom + 4))
				if source.x >= 0 and source.y >= 0 and source.x < 8 and source.y < 8:
					c = graphic[source.x][source.y]
					self.screen.pixel[target_x][target_y] = Color(int(c.r * self.brightness), int(c.g * self.brightness), int(c.b * self.brightness))

	def draw_scrollbar(self):
		size = int(math.floor(16 / len(self.items)))
		start = int(math.floor((16 - size) * self.index / (len(self.items) - 1)))

		for x in range(size):
			self.screen.pixel[(start + x - int(size * self.offset) + 16) % 16][15] = Color(int(80 * self.brightness), int(80 * self.brightness), int(80 * self.brightness))


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
		input.tick()
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
		self.items[self.index].on_key_press(key, self)
		
		if self.module != None:
			if key == input.Key.HOME or key == input.Key.BACK:
				self.stop()
			return

		if key == input.Key.RIGHT:
			self.move(1)
		if key == input.Key.LEFT:
			self.move(-1)
		if key == input.Key.ENTER or key == input.Key.A:
			self.launch()
			return True

	def stop(self):
		self.module.stop()
		self.screen.fade_out(0.3)
		self.module = None
		self.resume_animation()
		input.on_press = [self.on_key_down]
		input.on_release = []

	def launch(self):
		if self.items[self.index].is_launchable() == False:
			return
		self.start_animation()
		self.module = self.items[self.index].get_module(self.screen)
		self.module.start()

	def start_animation(self):
		start = time.clock()
		end = start + 1

		while time.clock () <= end:
			self.zoom = 1 + 16 * ((time.clock() - start) / (end - start)) ** 2
			self.brightness = min(1, 1 - ((time.clock() - start) / (end - start)))
			self.draw()

		time.sleep(0.1)
		self.reset(redraw = False)

	def resume_animation(self):
		start = time.clock()
		end = start + 0.5

		while time.clock () <= end:
			self.zoom = ((time.clock() - start) / (end - start))
			self.brightness = min(1, 1 * ((time.clock() - start) / (end - start)))
			
			self.draw()

		self.reset()

if __name__ == '__main__':
	menu = Menu(create_screen(), create_menu_items())
	while True:
		menu.tick()
		time.sleep(0.01)