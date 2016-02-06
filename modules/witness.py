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

		self.background_color = hsv_to_color(random.random(), 1, 0.4)
		self.line_color = darken_color(self.background_color, 0.4)
		self.path_color = brighten_color(self.background_color, 0.4)

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

	def create_random_path(self, screen):
		# Start by making a simple path

		dx = self.exit.x - self.entry.x
		dy = self.exit.y - self.entry.y

		steps = [Point(dx / abs(dx), 0) for i in range(abs(dx))]
		steps += [Point(0, dy / abs(dy)) for i in range(abs(dy))]
		random.shuffle(steps)

		path = Path(self, screen)
		for step in steps:
			path.steps.append(Point(path.steps[len(path.steps) - 1].x + step.x, path.steps[len(path.steps) - 1].y + step.y))

		# Randomly extend the path
		for i in range(random.randint(0, 9)):
			path.extend()

		return path
		

class Path:
	def __init__(self, puzzle, screen):
		self.puzzle = puzzle
		self.screen = screen
		self.steps = [puzzle.entry]

		self.offset_time = 0.2
		self.offset_start = time.clock()
		self.offset_end = self.offset_start + self.offset_time

	def animate_undo(self):
		self.offset_end = time.clock()
		self.offset_start = self.offset_end + self.offset_time

		while time.clock() < self.offset_start:
			time.sleep(0.01)
			self.puzzle.draw(self.screen)
			self.draw()
			self.screen.update()

		self.offset_end = time.clock()
		self.offset_start = self.offset_end - 1

		
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

	def contains_node(self, point):
		for step in self.steps:
			if step == point:
				return True
		return False

	def contains_edge(self, point1, point2):
		for i in range(len(self.steps) - 1):
			if (self.steps[i] == point1 and self.steps[i + 1] == point2) or (self.steps[i] == point2 and self.steps[i + 1] == point1):
				return True
		return False

	# Makes a random change to the path that either keeps the length or extends it
	def extend(self):
		blocks = []

		# Find all blocks that can be used to extend the path
		# Block must contain an existing edge and two empty nodes
		for x in range(self.puzzle.height - 1):
			for y in range(self.puzzle.width - 1):
				nodes = [Point(x, y), Point(x + 1, y), Point(x + 1, y + 1), Point(x, y + 1)]

				nodes_in_path = 0
				for node in nodes:
					if self.contains_node(node):
						nodes_in_path += 1

				if nodes_in_path != 2:
					continue

				contains_edge = False
				for i in range(4):
					if self.contains_edge(nodes[i], nodes[(i + 1) % 4]):
						contains_edge = True

				if contains_edge:
					blocks.append(Point(x, y))

		if len(blocks) == 0:
			return

		# Chose a block in which to extend the path
		block = random.choice(blocks)

		nodes = [Point(block.x, block.y), Point(block.x + 1, block.y), Point(block.x + 1, block.y + 1), Point(block.x, block.y + 1)]

		#Extend
		to_add = []

		for node in nodes:
			if not self.contains_node(node):
				to_add.append(node)

		entry = None

		for node in self.steps:
			if entry == None and node in nodes:
				entry = node

		if entry.x != to_add[0].x and entry.y != to_add[0].y:
			to_add = to_add[::-1]

		self.steps.insert(self.steps.index(entry) + 1, to_add[0])
		self.steps.insert(self.steps.index(entry) + 2, to_add[1])

class WitnessGame(Module):
	def __init__(self, screen, gamepad):
		super(WitnessGame, self).__init__(screen)
		self.gamepad = gamepad
		
		self.puzzle = Puzzle()
		self.path = Path(self.puzzle, screen)		
		
		self.gamepad.on_press.append(self.on_key_down)

		self.key_queue = []
	
	def draw(self):
		self.puzzle.draw(self.screen)
		self.path.draw()
		self.screen.update()
		
	def tick(self):
		if (len(self.key_queue) != 0):
			self.handle_key(self.key_queue.pop(0))

		self.draw()
		time.sleep(0.01)

	def on_key_down(self, key):
		self.key_queue.append(key)

	def handle_key(self, key):		
		if key == self.gamepad.UP:
			self.path.move(Point(0, -1))
		if key == self.gamepad.DOWN:
			self.path.move(Point(0, 1))
		if key == self.gamepad.LEFT:
			self.path.move(Point(-1, 0))
		if key == self.gamepad.RIGHT:
			self.path.move(Point(1, 0))
		if key == 2:
			self.path = self.puzzle.create_random_path(self.screen)
