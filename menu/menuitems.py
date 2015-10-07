import pygame.image
from helpers import *

class MenuItem(object):
	PREVIEW_SIZE = 8

	def __init__(self):
		self.preview = None

	def get_preview(self):
		return self.preview

	def get_module(self, screen, gamepad):
		raise NotImplementedError()

	@staticmethod
	def load_preview(filename):
		bmp = pygame.image.load(filename)
		arr = pygame.PixelArray(bmp)
		frame = [[int_to_color(arr[x, y]) for y in range(MenuItem.PREVIEW_SIZE)] for x in range(MenuItem.PREVIEW_SIZE)]

		return frame

	def on_key_press(self, key, menu):
		pass

	def is_launchable(self):
		return True

class CycleItem(MenuItem):
	def __init__(self):
		self.preview = MenuItem.load_preview('menu/preview/cycle.bmp')

	def get_module(self, screen, gamepad):
		from modules.cycle import Cycle
		return Cycle(screen, 'animations')

class TetrisItem(MenuItem):
	def __init__(self):
		self.preview = MenuItem.load_preview('menu/preview/tetris.bmp')

	def get_module(self, screen, gamepad):
		from modules.tetris import Tetris
		return Tetris(screen, gamepad)

class SnakeItem(MenuItem):
	def __init__(self):
		self.preview = MenuItem.load_preview('menu/preview/snake.bmp')

	def get_module(self, screen, gamepad):
		from modules.snake import Snake
		return Snake(screen, gamepad)

class PacmanItem(MenuItem):
	def __init__(self):
		self.preview = MenuItem.load_preview('menu/preview/pacman.bmp')

	def get_module(self, screen, gamepad):
		from modules.pacman import Pacman
		return Pacman(screen, gamepad)

class ClockItem(MenuItem):
	def __init__(self):
		self.preview = MenuItem.load_preview('menu/preview/clock.bmp')

	def get_module(self, screen, gamepad):
		from modules.clock import Clock
		return Clock(screen)

class PieItem(MenuItem):
	def __init__(self):
		self.preview = MenuItem.load_preview('menu/preview/pie.bmp')

	def get_module(self, screen, gamepad):
		from modules.pie import Pie
		return Pie(screen)

class BrightnessItem(MenuItem):
	def __init__(self):
		self.preview_template = MenuItem.load_preview('menu/preview/brightness.bmp')
		self.value = 5
		self.draw()

	def draw(self):
		self.preview = [self.preview_template[x][:] for x in range(8)]
		for x in range(8):
			if self.value > x:
				self.preview[x][7] = Color(255, 255, 255)

	def is_launchable(self):
		return False

	def update(self, menu):
		menu.screen.strip.setBrightness(int(4 + 3.1 * (self.value+1)**2))
		self.draw()
		menu.draw()

	def on_key_press(self, key, menu):
		if key == menu.gamepad.UP:
			self.value = min(max(0, self.value + 1), 8)
			self.update(menu)
		if key == menu.gamepad.DOWN:
			self.value = min(max(0, self.value - 1), 8)
			self.update(menu)

class MusicItem(MenuItem):
	def __init__(self):
		self.preview = MenuItem.load_preview('menu/preview/music.bmp')

	def get_module(self, screen, gamepad):
		from modules.music import Music
		return Music(screen)

menu_items = [
	CycleItem(),
	TetrisItem(),
	SnakeItem(),
	PacmanItem(),
	ClockItem(),
	PieItem(),
	BrightnessItem(),
	MusicItem()
]