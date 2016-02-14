from helpers import *
import random
from path import *

from puzzlefeature import *

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
