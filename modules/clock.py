import collections
import random
import time
import datetime
import os
import math
from helpers import *
from module import Module

class Clock(Module):
	def __init__(self, screen):
		super(Clock, self).__init__(screen)
		
	
	def draw_digit(self, digit, pos, color):
		if digit in [0, 2, 3, 4, 5, 6, 7, 8, 9]:
			self.screen.pixel[pos.x + 0][pos.y + 0] = color
		if digit in [0, 2, 3, 5, 6, 7, 8, 9, 22]:
			self.screen.pixel[pos.x + 1][pos.y + 0] = color
		if digit in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 22]:
			self.screen.pixel[pos.x + 2][pos.y + 0] = color
		if digit in [0, 4, 5, 6, 8, 9]:
			self.screen.pixel[pos.x + 0][pos.y + 1] = color
		if digit in [0, 1, 2, 3, 4, 7, 8, 9, 22]:
			self.screen.pixel[pos.x + 2][pos.y + 1] = color
		if digit in [0, 2, 4, 5, 6, 8, 9]:
			self.screen.pixel[pos.x + 0][pos.y + 2] = color
		if digit in [2, 3, 4, 5, 6, 8, 9, 22]:
			self.screen.pixel[pos.x + 1][pos.y + 2] = color
		if digit in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 22]:
			self.screen.pixel[pos.x + 2][pos.y + 2] = color
		if digit in [0, 2, 6, 8]:
			self.screen.pixel[pos.x + 0][pos.y + 3] = color
		if digit in [0, 1, 3, 4, 5, 6, 7, 8, 9]:
			self.screen.pixel[pos.x + 2][pos.y + 3] = color
		if digit in [0, 2, 3, 5, 6, 8, 9]:
			self.screen.pixel[pos.x + 0][pos.y + 4] = color
		if digit in [0, 2, 3, 5, 6, 8, 9, 22]:
			self.screen.pixel[pos.x + 1][pos.y + 4] = color
		if digit in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 22]:
			self.screen.pixel[pos.x + 2][pos.y + 4] = color
		if digit in [22]:
			self.screen.pixel[pos.x + 1][pos.y + 3] = color

	def draw_time(self, color, colon = True):
		now = datetime.datetime.now()

		self.draw_digit(now.minute % 10, Point(13, 5), color)
		self.draw_digit(math.floor(now.minute / 10), Point(9, 5), color)

		if colon:
			self.screen.pixel[7][7] = color
			self.screen.pixel[7][9] = color

		self.draw_digit(now.hour % 10, Point(3, 5), color)
		if math.floor(now.hour / 10) == 1:
			self.draw_digit(1, Point(-1, 5), color)
		if math.floor(now.hour / 10) == 2:
			self.draw_digit(22, Point(-1, 5), color)


	def draw(self, colon = True):
		self.screen.clear()
		self.draw_time(Color(255, 255, 255), colon)
		self.screen.update()
	
	def tick(self):
		self.draw(False)
		time.sleep(0.5)
		self.draw(True)
		time.sleep(0.5)
