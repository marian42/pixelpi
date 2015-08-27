from Screen import *
import collections
import random
import time
import os
from gamepad import *
import math

Point = collections.namedtuple('Point', 'x y')

def random_color():
	color = []
	while not 0 in color or not 255 in color:
		color = [random.choice([0, 255]) for i in range(3)]
	return Color(color[0], color[1], color[2])

def int_to_color(c):
	b =  c & 255
	g = (c >> 8) & 255
	r = (c >> 16) & 255
	return (r, g, b)

class Snake:
	def __init__(self, sceen):
		self.screen = screen
		self.snake = [Point(screen.width / 2, screen.height / 2)]
		self.dir = Point(0, -1)
		
		self.interval = 0.15
	
		self.new_game()
		self.gamepad = Gamepad()
		self.gamepad.on_press = self.on_key_down
		
		
	def new_game(self):
		self.food_color = random_color()
		self.head_color = random_color()
		while self.food_color == self.head_color:
			self.head_color = random_color()
		self.food_color_rgb = int_to_color(self.food_color)

		self.snake = [Point(screen.width / 2, screen.height / 2)]
		self.dir = Point(0, -1)
		self.last_food = None
		
		t = 1
		start = time.clock()
		rgb = int_to_color(self.head_color)
		while time.clock() < start + t:
			self.screen.clear()
			self.screen.pixel[self.snake[0].x][self.snake[0].y] = Color(int(rgb[0] * (time.clock() - start)**2 / t), int(rgb[1] * (time.clock() - start)**2 / t), int(rgb[2] * (time.clock() - start)**2 / t))
			self.screen.update()
		
		self.next_step = time.clock() + self.interval
		self.set_food()
		
	def game_over(self):
		print('GAME OVER - Score: ' + str(len(self.snake)))
		self.food = None
		self.draw()
		time.sleep(2)
		while len(self.snake) > 1:
			self.snake = self.snake[:-1]
			self.draw()
			time.sleep(0.12)
			
		t = 4
		start = time.clock()
		rgb = int_to_color(self.head_color)
		while time.clock() < start + t:
			self.screen.clear()
			self.screen.pixel[self.snake[0].x][self.snake[0].y] = Color(int(rgb[0] * (1 - (time.clock() - start) / t)**2), int(rgb[1] * (1 - (time.clock() - start) / t)**2), int(rgb[2] * (1 - (time.clock() - start) / t)**2))
			self.screen.update()
	
		self.new_game()
	
	def set_food(self):
		self.food = self.snake[0]
		while self.food in self.snake:
			self.food = Point(random.randint(0, self.screen.width - 1), random.randint(0, self.screen.height - 1))
		self.pulse_offset = time.clock()
			
	def move(self):
		next = Point((self.snake[0].x + self.dir.x) % self.screen.width, (self.snake[0].y + self.dir.y) % self.screen.height)
		
		if next in self.snake:
			self.game_over()
			return
		
		if next == self.food:
			self.last_food = self.food
			self.set_food()
			self.snake.insert(0, next)
		else:
			for i in reversed(range(1, len(self.snake))):
				self.snake[i] = self.snake[i - 1]
			self.snake[0] = next
	
	def draw(self):
		self.screen.clear()
		
		if self.food != None:
			t = 0.6
			if self.last_food != None and time.clock() - self.pulse_offset < t:
				radius = 18
				for x in range(self.screen.width):
					for y in range(self.screen.height):
						d = ((x - self.last_food.x)** 2 + (y - self.last_food.y)**2) ** 0.5
						if (d / radius)**0.5 < (time.clock() - self.pulse_offset) / t:
							self.screen.pixel[x][y] = Color(
								max(0, int(self.food_color_rgb[0] * 0.2 * (1 - (time.clock() - self.pulse_offset) / t)**2)),
								max(0, int(self.food_color_rgb[1] * 0.2 * (1 - (time.clock() - self.pulse_offset) / t)**2)),
								max(0, int(self.food_color_rgb[2] * 0.2 * (1 - (time.clock() - self.pulse_offset) / t)**2)))
		
		for p in self.snake:
			self.screen.pixel[p.x][p.y] = Color(255, 255, 255)
		self.screen.pixel[self.snake[0].x][self.snake[0].y] = self.head_color
		
		if self.food != None:
			self.screen.pixel[self.food.x][self.food.y] = Color(
				int(self.food_color_rgb[0] * math.sin((time.clock() - self.pulse_offset) * 8) ** 2),
				int(self.food_color_rgb[1] * math.sin((time.clock() - self.pulse_offset) * 8) ** 2),
				int(self.food_color_rgb[2] * math.sin((time.clock() - self.pulse_offset) * 8) ** 2))
		
		self.screen.update()
		
	def run(self):
		while True:
			if self.next_step < time.clock():				
				self.move()
				if self.gamepad.button[1]:
					self.next_step += self.interval / 3
				else: self.next_step += self.interval
			self.draw()
			time.sleep(0.01)
			
	def on_key_down(self, key):
		next = self.dir
		if key == self.gamepad.UP:
			next = Point(0, -1)
		if key == self.gamepad.DOWN:
			next = Point(0, 1)
		if key == self.gamepad.LEFT:
			next = Point(-1, 0)
		if key == self.gamepad.RIGHT:
			next = Point(1, 0)
		
		if key == 1:
			self.next_step = time.clock()
		
		if len(self.snake) == 1 or self.snake[0].x + next.x != self.snake[1].x or self.snake[0].y + next.y != self.snake[1].y:
			self.dir = next
			
if __name__ == '__main__':
	screen = Screen()
	snake = Snake(screen)
	snake.run()