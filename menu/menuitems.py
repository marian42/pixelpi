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

menu_items = [
	CycleItem(),
	TetrisItem(),
	SnakeItem(),
	PacmanItem(),
	ClockItem()
]