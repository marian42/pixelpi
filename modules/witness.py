import collections
import random
import time
import os
import math
from helpers import *
from module import *

class Puzzle:
	def __init__(self):
		self.width = 5
		self.height = 5
		self.cell_size = 3
		
		self.entry = Point(0, 4)
		self.exit = Point(4, 0)
		
		self.offset = Point(2 if self.entry.x == 0 else 1, 2 if self.entry.y == 0 else 1)
		self.exit_on_screen = Point(self.offset.x + self.exit.x * self.cell_size, self.offset.y + self.exit.y * self.cell_size + (-1 if self.exit.y == 0 else 1))

		self.background_color = Color(235, 174, 10)
		self.line_color = darken_color(self.background_color, 0.5)
		self.path_color = brighten_color(self.background_color, 0.5)

	def draw(self, screen):
		screen.clear(self.background_color)

		for x in range(self.width):
			for y in range(self.height):
				screen.pixel[self.offset.x + x * self.cell_size][self.offset.y + y * self.cell_size] = self.line_color

				if x != self.width - 1:
					for i in range(self.cell_size):
						screen.pixel[self.offset.x + x * self.cell_size + i][self.offset.y + y * self.cell_size] = self.line_color
				if y != self.height - 1:
					for i in range(self.cell_size):
						screen.pixel[self.offset.x + x * self.cell_size][self.offset.y + y * self.cell_size + i] = self.line_color

		for x in range(3):
			for y in range(3):
				screen.pixel[self.offset.x + x + self.entry.x * self.cell_size - 1][self.offset.y + y + self.entry.y * self.cell_size - 1] = self.line_color

		screen.pixel[self.exit_on_screen.x][self.exit_on_screen.y] = self.line_color

class Path:
	def __init__(self, puzzle, screen):
		self.puzzle = puzzle
		self.screen = screen
		self.steps = [puzzle.entry]

		self.offset_time = 0.25
		self.offset_start = time.clock()
		self.offset_end = self.offset_start + self.offset_time

	def animate_undo(self):
		self.offset_end = time.clock()
		self.offset_start = self.offset_end + self.offset_time

		while time.clock() < self.offset_start:
			time.sleep(0.1)

		self.offset_end = time.clock()

		
	def move(self, direction):
		if abs(direction.x) + abs(direction.y) != 1:
			return

		next = Point(self.steps[len(self.steps )- 1].x + direction.x, self.steps[len(self.steps) - 1].y + direction.y)

		if next.x < 0 or next.y < 0 or next.x >= self.puzzle.width or next.y >= self.puzzle.height:
			return

		if len(self.steps) > 1 and self.steps[len(self.steps) - 2] == next:
			self.animate_undo()
			self.steps.pop()
			return

		if next in self.steps:
			return

		self.offset_start = time.clock()
		self.offset_end = self.offset_start + self.offset_time
		
		self.steps.append(next)

	def draw(self):
		offset = 1.0 - min(1, max(0, (time.clock() - self.offset_start) / (self.offset_end - self.offset_start)))
		print offset
		
		for i in range(len(self.steps) - 1):
			for p in range(self.puzzle.cell_size):
				#local_offset = max(0, min(1, i - (len(self.steps) - 1) + offset))
				local_offset = offset
				if i != len(self.steps) - 2:
					local_offset = 0
				pixel_offset = max(0, min(1, (1 - local_offset ) * (self.puzzle.cell_size) - p + 1))
				color = blend_colors(self.puzzle.line_color, self.puzzle.path_color, pixel_offset)
				self.screen.pixel[self.puzzle.offset.x + self.steps[i].x * self.puzzle.cell_size + (self.steps[i + 1].x - self.steps[i].x) * p][self.puzzle.offset.y + self.steps[i].y * self.puzzle.cell_size + (self.steps[i + 1].y - self.steps[i].y) * p] = color
		
		color = blend_colors(self.puzzle.line_color, self.puzzle.path_color, 1.0 -  min(1, max(0, offset * self.puzzle.cell_size)))
		self.screen.pixel[self.puzzle.offset.x + self.steps[len(self.steps) - 1].x * self.puzzle.cell_size][self.puzzle.offset.y + self.steps[len(self.steps) - 1].y * self.puzzle.cell_size] = color

		if self.steps[len(self.steps) -1] == self.puzzle.exit and offset == 0:
			self.screen.pixel[self.puzzle.exit_on_screen.x][self.puzzle.exit_on_screen.y] = self.puzzle.path_color

		if len(self.steps) > 0:
			for x in range(3):
				for y in range(3):
					color = self.puzzle.path_color
					if len(self.steps) == 1:
						color = blend_colors(self.puzzle.path_color, self.puzzle.line_color, min(1, max(0, offset)))

					self.screen.pixel[self.puzzle.offset.x + x + self.steps[0].x * self.puzzle.cell_size - 1][self.puzzle.offset.y + y + self.steps[0].y * self.puzzle.cell_size - 1] = color



class WitnessGame(Module):
	def __init__(self, screen, gamepad):
		super(WitnessGame, self).__init__(screen)
		self.gamepad = gamepad
		
		self.puzzle = Puzzle()
		self.path = Path(self.puzzle, screen)		
		
		self.gamepad.on_press.append(self.on_key_down)
	
	def draw(self):
		self.puzzle.draw(self.screen)
		self.path.draw()
		self.screen.update()
		
	def tick(self):
		self.draw()
		time.sleep(0.01)
		
	def on_key_down(self, key):
		if key == self.gamepad.UP:
			self.path.move(Point(0, -1))
		if key == self.gamepad.DOWN:
			self.path.move(Point(0, 1))
		if key == self.gamepad.LEFT:
			self.path.move(Point(-1, 0))
		if key == self.gamepad.RIGHT:
			self.path.move(Point(1, 0))
