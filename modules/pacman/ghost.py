from helpers import *
import time
import random

class Ghost(object):
	ROAM = 0
	CHASE = 1
	FLEE = 2
	GOHOME = 3

	home = Point(8, 6)

	def __init__(self, game, color, initial_delay):
		self.game = game
		self.color = color
		self.pos = self.home

		self.set_mode(self.ROAM)
		self.next_move = time.clock() + initial_delay
		self.destination = None

	def get_mode_end(self):
		if self.mode == self.CHASE:
			return time.clock() + 6
		if self.mode == self.ROAM:
			return time.clock() + 5
		if self.mode == self.FLEE:
			return time.clock() + 10
		if self.mode == self.GOHOME:
			return None

	def set_mode(self, mode):
		self.mode = mode
		self.destination = None
		self.next_mode = self.get_mode_end()

	def get_next_mode(self):
		if self.mode == self.ROAM:
			return self.CHASE
		if self.mode == self.CHASE:
			return self.ROAM
		if self.mode == self.FLEE:
			return self.ROAM
		if self.mode == self.GOHOME:
			return self.ROAM

	def get_interval(self):
		if self.mode == self.CHASE:
			return 0.2
		if self.mode == self.FLEE:
			return 0.6
		if self.mode == self.ROAM:
			return 0.3
		return 0.4

	def get_random_place(self):
		p = Point(random.randint(0, 15), random.randint(0, 14))
		while self.game.walls[p.y][p.x] == 1:
			p = Point(random.randint(0, 15), random.randint(0, 14))
		return p

	def get_destination(self):
		if self.destination != None and self.destination != self.pos:
			return self.destination

		if self.mode == self.CHASE:
			self.destination = self.game.pacman
		if self.mode == self.GOHOME:
			self.destination = self.home
		if self.mode == self.FLEE:
			self.destination = self.get_random_place()
		if self.mode == self.ROAM:
			self.destination = self.get_random_place()
		return self.destination

	def get_color(self):
		if self.mode == self.FLEE:
			if self.next_mode - time.clock() < 4:
				return Color(88, 88, 221) if round(time.clock() * 5) % 2 == 0 else self.color
			return Color(88, 88, 221)
		if self.mode == self.GOHOME:
			return Color(255, 255, 255)
		return self.color

	def draw(self):
		self.game.screen.pixel[self.pos.x][self.pos.y] = self.get_color()

	def move(self):
		direction_map = self.game.get_direction_map(self.get_destination())
		direction = direction_map[self.pos.x][self.pos.y]
		old = self.pos
		if (direction != None):
			self.pos = Point((self.pos.x + direction.x + 16) % 16, (self.pos.y + direction.y + 16) % 16)

	def next_mode_is_due(self):
		return ((self.next_mode != None and self.next_mode < time.clock())
			or (self.mode == self.GOHOME and self.pos == self.home))

	def tick(self):
		if self.next_mode_is_due():
			self.set_mode(self.get_next_mode())

		if self.next_move < time.clock():
			self.next_move += self.get_interval()
			self.move()