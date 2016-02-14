from helpers import *
import random
import time
import math

class Path:
	def __init__(self, puzzle, screen):
		self.puzzle = puzzle
		self.screen = screen
		self.steps = []

		self.offset_time = 0.2
		self.offset_start = time.clock()
		self.offset_end = self.offset_start + self.offset_time

		self.wrong = False
		self.wrong_since = None
		self.errors = []

	def animate_undo(self):
		self.offset_end = time.clock()
		self.offset_start = self.offset_end + self.offset_time

		while time.clock() < self.offset_start:
			time.sleep(0.01)
			self.puzzle.draw(self.screen)
			self.draw()
			self.screen.update()

		self.offset_start = self.offset_end - self.offset_time

	def start(self):
		self.steps = [self.puzzle.entry]

		self.offset_start = time.clock()
		self.offset_end = self.offset_start + self.offset_time
		
	def move(self, direction):
		if len(self.steps) == 0:
			return

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
		if len(self.steps) == 0:
			return

		offset = 1.0 - min(1, max(0, (time.clock() - self.offset_start) / (self.offset_end - self.offset_start)))
		
		path_color = self.puzzle.path_color
		if self.wrong:
			path_color = Color(0, 0, 0)

		if self.steps[len(self.steps) - 1] == self.puzzle.exit and offset == 0 and not self.wrong:
			path_color = blend_colors(Color(255, 255, 255), path_color, math.sin(time.clock() * 8) ** 2)

		opacity = 1
		if self.wrong_since != None:
			opacity = 1.0 - min(1, (time.clock() - self.wrong_since) / 4.0)

		for i in range(len(self.steps) - 1):
			for p in range(self.puzzle.cell_size):
				local_offset = offset
				if i != len(self.steps) - 2:
					local_offset = 0
				pixel_offset = max(0, min(1, (1 - local_offset ) * (self.puzzle.cell_size) - p + 1))
				
				position = Point(self.puzzle.offset.x + self.steps[i].x * self.puzzle.cell_size + (self.steps[i + 1].x - self.steps[i].x) * p, self.puzzle.offset.y + self.steps[i].y * self.puzzle.cell_size + (self.steps[i + 1].y - self.steps[i].y) * p)
				color = blend_colors(self.screen.pixel[position.x][position.y], path_color, pixel_offset)
				
				if opacity != 1:
					color = blend_colors(self.screen.pixel[position.x][position.y], color, opacity)

				self.screen.pixel[position.x][position.y] = color
		
		position = Point(self.puzzle.offset.x + self.steps[len(self.steps) - 1].x * self.puzzle.cell_size, self.puzzle.offset.y + self.steps[len(self.steps) - 1].y * self.puzzle.cell_size)
		color = blend_colors(self.screen.pixel[position.x][position.y], path_color, 1.0 -  min(1, max(0, offset * self.puzzle.cell_size)))
		if opacity != 1:
			color = blend_colors(self.screen.pixel[position.x][position.y], color, opacity)
		self.screen.pixel[position.x][position.y] = color

		if self.steps[len(self.steps) -1] == self.puzzle.exit and offset == 0:
			color = path_color

			if opacity != 1:
				color = blend_colors(self.screen.pixel[self.puzzle.exit_on_screen.x][self.puzzle.exit_on_screen.y], color, opacity)

			self.screen.pixel[self.puzzle.exit_on_screen.x][self.puzzle.exit_on_screen.y] = color

		if len(self.steps) > 0:
			for x in range(3):
				for y in range(3):
					color = path_color
					if len(self.steps) == 1:
						color = blend_colors(path_color, self.puzzle.line_color, offset)

					pos = Point(self.puzzle.offset.x + x + self.steps[0].x * self.puzzle.cell_size - 1, self.puzzle.offset.y + y + self.steps[0].y * self.puzzle.cell_size - 1)

					if opacity != 1:
						color = blend_colors(self.screen.pixel[pos.x][pos.y], color, opacity)

					self.screen.pixel[pos.x][pos.y] = color

		if self.wrong:
			for error in self.errors:
				self.screen.pixel[error.x][error.y] = blend_colors(self.screen.pixel[error.x][error.y], Color(255, 0, 0), math.sin(time.clock() * 8) ** 2)

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

	def check(self):
		if self.steps[len(self.steps) - 1] != self.puzzle.exit:
			return False

		for feature in self.puzzle.features:
			if not feature.check(self):
				return False
		return True

	def fill_zone(self, x, y, value):
		queue = [Point(x, y)]
		self.zones[x][y] = value

		while len(queue) != 0:
			block = queue.pop(0)

			if block.x > 0 and self.zones[block.x - 1][block.y] == -1 and not self.contains_edge(block, Point(block.x, block.y + 1)):
				self.zones[block.x - 1][block.y] = value
				queue.append(Point(block.x - 1, block.y))
			if block.y > 0 and self.zones[block.x][block.y - 1] == -1 and not self.contains_edge(block, Point(block.x + 1, block.y)):
				self.zones[block.x][block.y - 1] = value
				queue.append(Point(block.x, block.y - 1))
			if block.x < self.puzzle.width - 2 and self.zones[block.x + 1][block.y] == -1 and not self.contains_edge(Point(block.x + 1, block.y), Point(block.x + 1, block.y + 1)):
				self.zones[block.x + 1][block.y] = value
				queue.append(Point(block.x + 1, block.y))
			if block.y < self.puzzle.height - 2 and self.zones[block.x][block.y + 1] == -1 and not self.contains_edge(Point(block.x, block.y  + 1), Point(block.x + 1, block.y + 1)):
				self.zones[block.x][block.y + 1] = value
				queue.append(Point(block.x, block.y + 1))

	def get_zones(self):
		self.zones = [[-1 for y in range(self.puzzle.height - 1)] for x in range(self.puzzle.width -1)]
		
		zone_index = 0

		for x in range(self.puzzle.width - 1):
			for y in range(self.puzzle.height - 1):
				if self.zones[x][y] == -1:
					self.fill_zone(x, y, zone_index)
					zone_index += 1

		self.zone_count = zone_index
		return self.zones