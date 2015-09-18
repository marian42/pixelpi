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

class TetrisItem(MenuItem):
	def __init__(self):
		self.preview = MenuItem.load_preview('menu/preview/tetris.bmp')

class SnakeItem(MenuItem):
	def __init__(self):
		self.preview = MenuItem.load_preview('menu/preview/snake.bmp')

class ClockItem(MenuItem):
	def __init__(self):
		self.preview = MenuItem.load_preview('menu/preview/clock.bmp')

menu_items = [
	CycleItem(),
	TetrisItem(),
	SnakeItem(),
	ClockItem()
]