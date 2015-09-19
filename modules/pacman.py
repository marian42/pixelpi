import collections
import random
import time
import os
import math
from helpers import *
from module import *

class Pacman(Module):
	walls = [
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
		[1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
		[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
		[1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
		[1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
		[1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
		[1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
		[1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1],
		[1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	]

	pill_spots = [Point(1, 1), Point(14, 1), Point(1, 13), Point(14, 13)]

	food_spots = [
		Point(3, 1), Point(5, 1), Point(10, 1), Point(12, 1),
		Point(1, 3), Point(3, 3), Point(5, 3), Point(10, 3), Point(12, 3), Point(14, 3),
		Point(1, 5), Point(3, 5), Point(5, 5), Point(10, 5), Point(12, 5), Point(14, 5),
		Point(1, 7), Point(3, 7), Point(5, 7), Point(10, 7), Point(12, 7), Point(14, 7),
		Point(1, 9), Point(3, 9), Point(5, 9), Point(10, 9), Point(12, 9), Point(14, 9),
		Point(1, 11), Point(3, 11), Point(5, 11), Point(10, 11), Point(12, 11), Point(14, 11),
		Point(3, 13), Point(5, 13), Point(10, 13), Point(12, 13)
	]

	step_interval = 0.2
	wall_color = Color(0, 0, 234)
	food_color = Color(61, 44, 42)
	pill_color = Color(255, 184, 174)
	pacman_color = Color(255, 255, 0)
	cherry_color = Color(255, 0, 0)

	def __init__(self, screen, gamepad):
		super(Pacman, self).__init__(screen)
		self.gamepad = gamepad
		self.gamepad.on_press.append(self.on_key_down)

		self.new_game()

	def new_game(self):
		self.lives = 3

		self.new_level()

	def new_level(self):
		self.pacman = Point(8, 9)
		self.dir = Point(-1, 0)
		self.new_dir = self.dir
		self.next_step = time.clock() + self.step_interval
		self.food = self.food_spots[:]
		self.pills = self.pill_spots[:]

	def draw_walls(self):
		for x in range(16):
			for y in range(16):
				if self.walls[y][x] == 1:
					self.screen.pixel[x][y] = self.wall_color
	
	def draw(self):
		self.screen.clear()
		self.draw_walls()

		for pill in self.pills:
			self.screen.pixel[pill.x][pill.y] = self.pill_color

		for food in self.food:
			self.screen.pixel[food.x][food.y] = self.food_color

		for i in range(self.lives):
			self.screen.pixel[1 + 2 * i][15] = self.pacman_color

		brightness = 0.2 + 0.8 * math.sin(time.clock() / self.step_interval / 2 * math.pi + 0.5 * math.pi)**2
		self.screen.pixel[self.pacman.x][self.pacman.y] = Color(self.pacman_color.r * brightness, self.pacman_color.g * brightness, self.pacman_color.b * brightness)

		self.screen.update()

	def get_nex_step(self, direction):
		return Point((self.pacman.x + direction.x + 16) % 16, (self.pacman.y + direction.y + 16) % 16)

	def move(self):
		next = self.get_nex_step(self.new_dir)

		if self.walls[next.y][next.x] == 0:
			self.pacman = next
			self.dir = self.new_dir
		else:
			next = self.get_nex_step(self.dir)
			if self.walls[next.y][next.x] == 0:
				self.pacman = next

		if self.pacman in self.food:
			self.food.remove(self.pacman)

		if self.pacman in self.pills:
			self.pills.remove(self.pacman)

		if len(self.food) == 0 and len(self.pills) == 0:
			self.new_level()

	def tick(self):
		self.draw()

		if time.clock() > self.next_step:
			self.next_step += self.step_interval
			self.move() 

		time.sleep(0.005)
		
	def on_key_down(self, key):
		if key == self.gamepad.UP:
			self.new_dir = Point(0, -1)
		if key == self.gamepad.DOWN:
			self.new_dir = Point(0, 1)
		if key == self.gamepad.LEFT:
			self.new_dir = Point(-1, 0)
		if key == self.gamepad.RIGHT:
			self.new_dir = Point(1, 0)