import collections
import random
import time
import os
import math
from helpers import *
from module import *

class AbstractPuzzleFeature(object):
	def draw(self, screen):
		pass

	def check(self, path):
		pass

class MandatoryNode(AbstractPuzzleFeature):
	def __init__(self, puzzle, node):
		self.node = node
		self.puzzle = puzzle

	def check(self, path):
		return path.contains_node(self.node)

	def draw(self, screen):
		screen.pixel[self.puzzle.offset.x + self.node.x * self.puzzle.cell_size][self.puzzle.offset.y + self.node.y * self.puzzle.cell_size] = darken_color(self.puzzle.line_color, 0.1)

class ForbiddenEdge(AbstractPuzzleFeature):
	def __init__(self, puzzle, node1, node2):
		self.puzzle = puzzle
		self.node1 = node1
		self.node2 = node2

	def check(self, path):
		return not path.contains_edge(self.node1, self.node2)

	def draw(self, screen):
		for p in range(1, self.puzzle.cell_size):
			position = Point(self.puzzle.offset.x + self.node1.x * self.puzzle.cell_size + (self.node2.x - self.node1.x) * p, self.puzzle.offset.y + self.node1.y * self.puzzle.cell_size + (self.node2.y - self.node1.y) * p)
			screen.pixel[position.x][position.y] = self.puzzle.background_color

class MandatoryEdge(AbstractPuzzleFeature):
	def __init__(self, puzzle, node1, node2):
		self.puzzle = puzzle
		self.node1 = node1
		self.node2 = node2

	def check(self, path):
		return path.contains_edge(self.node1, self.node2)

	def draw(self, screen):
		position = Point(self.puzzle.offset.x + self.node1.x * self.puzzle.cell_size + (self.node2.x - self.node1.x), self.puzzle.offset.y + self.node1.y * self.puzzle.cell_size + (self.node2.y - self.node1.y))
		screen.pixel[position.x][position.y] = darken_color(self.puzzle.line_color, 0.1)

class ColorBlocks(AbstractPuzzleFeature):
	def __init__(self, puzzle):
		self.puzzle = puzzle
		self.colors = [[None for y in range(puzzle.height - 1)] for x in range(puzzle.width -1)]

	def check(self, path):
		zones = path.get_zones()

		zone_color_dict = {}

		for x in range(self.puzzle.width - 1):
			for y in range(self.puzzle.height - 1):
				if self.colors[x][y] != None:
					if zones[x][y] in zone_color_dict:
						if zone_color_dict[zones[x][y]] != self.colors[x][y]:
							return False
					else:
						zone_color_dict[zones[x][y]] = self.colors[x][y]
		return True

	def draw(self, screen):
		for x in range(self.puzzle.width - 1):
			for y in range(self.puzzle.height - 1):
				if self.colors[x][y] != None:
					for a in range(self.puzzle.cell_size - 1):
						for b in range(self.puzzle.cell_size - 1):
							position = Point(self.puzzle.offset.x + x * self.puzzle.cell_size + 1 + a, self.puzzle.offset.y + y * self.puzzle.cell_size + 1 + b)
							screen.pixel[position.x][position.y] = self.colors[x][y]

class Puzzle:
	def __init__(self, screen):
		self.screen = screen

		self.width = 5
		self.height = 5
		self.cell_size = 3
		
		self.entry = Point(random.choice([0, self.width - 1]), random.choice([0, self.height - 1]))

		while True:			
			self.exit = Point(random.choice([0, self.width - 1]), random.choice([0, self.height - 1]))
			if self.exit != self.entry:
				break
		
		self.offset = Point(2 if self.entry.x == 0 else 1, 2 if self.entry.y == 0 else 1)
		self.exit_on_screen = Point(self.offset.x + self.exit.x * self.cell_size, self.offset.y + self.exit.y * self.cell_size + (-1 if self.exit.y == 0 else 1))

		self.hue = random.random()
		self.background_color = hsv_to_color(self.hue, 0.9, 0.5)
		self.path_color = hsv_to_color(self.hue, 0.35, 1.0)
		self.line_color = hsv_to_color(self.hue, 1.0, 0.15)

		self.solution = self.create_random_path(self.screen)
		self.create_features()

	def solve(self):
		self.path_color = hsv_to_color(self.hue, 0.0, 1)

	def create_features(self):
		self.features = []

		total_features = random.randint(2, 8)

		available_mandatory_nodes = list(self.solution.steps)
		available_mandatory_nodes.remove(self.entry)
		available_mandatory_nodes.remove(self.exit)

		available_mandatory_edges = [(self.solution.steps[i], self.solution.steps[i + 1]) for i in range(1, len(self.solution.steps) - 1)]

		for i in range(total_features):
			feature_type = random.randint(0, 2)

			if feature_type == 0 and len(available_mandatory_nodes) > 0:
				mandatory_node = random.choice(available_mandatory_nodes)
				available_mandatory_nodes.remove(mandatory_node)
				self.features.append(MandatoryNode(self, mandatory_node))

			if feature_type == 1:
				node1 = None
				node2 = None

				while True:
					node1 = Point(random.randint(0, self.width - 2), random.randint(0, self.height - 2))
					if bool(random.getrandbits(1)):
						node2 = Point(node1.x, node1.y + 1)
					else:
						node2 = Point(node1.x + 1, node1.y)

					if not self.solution.contains_edge(node1, node2):
						break

				self.features.append(ForbiddenEdge(self, node1, node2))

			if feature_type == 2 and len(available_mandatory_edges) > 1:
				mandatory_edge = random.choice(available_mandatory_edges)
				available_mandatory_edges.remove(mandatory_edge)
				self.features.append(MandatoryEdge(self, mandatory_edge[0], mandatory_edge[1]))

		zones = self.solution.get_zones()
		if self.solution.zone_count > 1:
			found_white = False
			found_black = False

			colorblocks = ColorBlocks(self)
			for i in range(random.randint(4, 10)):
				p = Point(random.randint(0, self.width - 2), random.randint(0, self.height - 2))

				if zones[p.x][p.y] % 2 == 0:
					found_black = True
				else:
					found_white = True

				colorblocks.colors[p.x][p.y] = Color(0, 0, 0) if zones[p.x][p.y] % 2 == 0 else Color(255, 255, 255)
			
			if found_white and found_black:
				self.features.append(colorblocks)

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

		for feature in self.features:
			feature.draw(screen)

	def create_random_path(self, screen):
		# Start by making a simple path

		dx = self.exit.x - self.entry.x
		dy = self.exit.y - self.entry.y

		steps = [Point(dx / abs(dx), 0) for i in range(abs(dx))]
		steps += [Point(0, dy / abs(dy)) for i in range(abs(dy))]
		random.shuffle(steps)

		path = Path(self, screen)
		path.start()
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
		self.steps = []

		self.offset_time = 0.2
		self.offset_start = time.clock()
		self.offset_end = self.offset_start + self.offset_time

		self.wrong = False
		self.wrong_since = None

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

class WitnessGame(Module):
	def __init__(self, screen, gamepad):
		super(WitnessGame, self).__init__(screen)
		self.gamepad = gamepad
		
		self.new_game()

		self.gamepad.on_press.append(self.on_key_down)

		self.key_queue = []

		self.wrong_path = None

		self.draw()
		self.screen.fade_in(0.4)
	
	def draw(self):
		self.puzzle.draw(self.screen)
		self.path.draw()
		if self.wrong_path != None and len(self.path.steps) == 0:
			self.wrong_path.draw()

	def tick(self):
		if (len(self.key_queue) != 0):
			self.handle_key(self.key_queue.pop(0))

		self.draw()		
		self.screen.update()
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
			if len(self.path.steps) == 0:
				self.wrong_path = None
				self.path.start()
				return

			if self.path.check():
				self.puzzle.solve()
				self.draw()
				self.screen.update()
				time.sleep(1)

				self.screen.fade_out(0.4)
				self.new_game()
				self.draw()
				self.screen.fade_in(0.4)

				self.path.offset_start = time.clock()
				self.path.offset_end = self.path.offset_start + self.path.offset_time
			else:
				self.wrong_path = self.path
				self.wrong_path.wrong = True
				self.wrong_path.wrong_since = time.clock()
				self.path = Path(self.puzzle, self.screen)

		if key == 3 and len(self.path.steps) > 0:
			self.path = Path(self.puzzle, self.screen)

	def new_game(self):
		self.puzzle = Puzzle(self.screen)
		self.path = Path(self.puzzle, self.screen)
		self.errors = []
			