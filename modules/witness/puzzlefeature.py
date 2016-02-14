from helpers import *

class AbstractPuzzleFeature(object):
	def draw(self, screen):
		pass

	def check(self, path):
		pass

class MandatoryNode(AbstractPuzzleFeature):
	def __init__(self, puzzle, node):
		self.node = node
		self.puzzle = puzzle

	def get_screen_position(self):
		return Point(self.puzzle.offset.x + self.node.x * self.puzzle.cell_size, self.puzzle.offset.y + self.node.y * self.puzzle.cell_size)

	def check(self, path):
		result = path.contains_node(self.node)
		if not result:
			path.errors.append(self.get_screen_position())
		return result

	def draw(self, screen):
		pos = self.get_screen_position()
		screen.pixel[pos.x][pos.y] = darken_color(self.puzzle.line_color, 0.1)

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

	def get_screen_position(self):
		return Point(self.puzzle.offset.x + self.node1.x * self.puzzle.cell_size + (self.node2.x - self.node1.x), self.puzzle.offset.y + self.node1.y * self.puzzle.cell_size + (self.node2.y - self.node1.y))

	def check(self, path):
		result = path.contains_edge(self.node1, self.node2)
		if not result:
			path.errors.append(self.get_screen_position())
		return result

	def draw(self, screen):
		pos = self.get_screen_position()
		screen.pixel[pos.x][pos.y] = darken_color(self.puzzle.line_color, 0.1)

class ColorBlocks(AbstractPuzzleFeature):
	def __init__(self, puzzle):
		self.puzzle = puzzle
		self.colors = [[None for y in range(puzzle.height - 1)] for x in range(puzzle.width -1)]

	def mark_error(self, path, x, y):
		for a in range(self.puzzle.cell_size - 1):
			for b in range(self.puzzle.cell_size - 1):
				position = Point(self.puzzle.offset.x + x * self.puzzle.cell_size + 1 + a, self.puzzle.offset.y + y * self.puzzle.cell_size + 1 + b)
				path.errors.append(position)

	def check(self, path):
		zones = path.get_zones()

		zone_color_dict = {}

		for x in range(self.puzzle.width - 1):
			for y in range(self.puzzle.height - 1):
				if self.colors[x][y] != None:
					if zones[x][y] in zone_color_dict:
						if zone_color_dict[zones[x][y]] != self.colors[x][y]:
							self.mark_error(path, x, y)

							marked_zone_block = False
							for u in range(self.puzzle.width - 1):
								for v in range(self.puzzle.height - 1):
									if not marked_zone_block and zones[u][v] == zones[x][y] and self.colors[u][v] == zone_color_dict[zones[x][y]]:
										self.mark_error(path, u, v)
										marked_zone_block = True

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

