import collections
import random
import time
import pygame
import os
import thread
import math
import input

from thread import start_new_thread
from modules.animation import *

from helpers import *

class Particle:
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.vy = 0
		self.color = color

	def step(self, dt):
		self.y += dt * self.vy
		self.vy += dt * 250

class Tetromino:
	def __init__(self, blocks, color):
		self.color = color
	
		self.width = 0
		self.height = 0
		for block in blocks:
			self.width = max(self.width, block.x + 1)
			self.height = max(self.height, block.y + 1)
		
		self.map = [[False for y in range(self.height)] for x in range(self.width)]
		for block in blocks:
			self.map[block.x][block.y] = True
			
	def rotate(self, amount = 1):
		if amount < 1:
			return self
		if amount > 1:
			return self.rotate(amount - 1).rotate()
			
		blocks = []
		for x in range(self.width):
			for y in range(self.height):
				if self.map[x][y]:
					blocks.append(Point(self.height - y - 1, x))
		return Tetromino(blocks, self.color)

class Tetris(Module):
	tetrominos = [
		Tetromino([Point(0,0), Point(1,0), Point(2,0), Point(3,0)], Color(0, 255, 255)),
		Tetromino([Point(0,0), Point(1,0), Point(0,1), Point(1,1)], Color(255, 255, 0)),
		Tetromino([Point(0,0), Point(1,0), Point(2,0), Point(1,1)], Color(255, 0, 255)),
		Tetromino([Point(0,0), Point(1,0), Point(2,0), Point(2,1)], Color(0, 0, 255)),
		Tetromino([Point(0,0), Point(1,0), Point(2,0), Point(0,1)], Color(255, 127, 0)),
		Tetromino([Point(1,0), Point(2,0), Point(0,1), Point(1,1)], Color(0, 255, 0)),
		Tetromino([Point(0,0), Point(1,0), Point(1,1), Point(2,1)], Color(255, 0, 0)),
	]
	
	COOLDOWN = 0.03

	def __init__(self, screen):
		super(Tetris, self).__init__(screen)
		
		self.level_width = 10
		self.level_height = 16
		
		self.draw_lock = thread.allocate_lock()
		self.game_lock = thread.allocate_lock()
		
		input.on_press.append(self.enqueue_key)
		self.lastinput = 0
		
		self.new_game()
		self.start()
		
	def new_game(self):
		self.score = 0
		self.level = [[None for y in range(self.level_height)] for x in range(self.level_height)]
		self.pick_tetromino()
		self.next_step = time.clock()
		self.key_queue = []
	
	def draw_background(self):
		self.screen.clear(Color(255,255,255))
		
	def draw_blocks(self):
		for y in range(self.level_height):
			for x in range(self.level_width):
				if self.level[x][y] != None:
					self.screen.pixel[x + (self.screen.width - self.level_width) / 2][y + (self.screen.height - self.level_height) / 2] = self.level[x][y]
				else: self.screen.pixel[x + (self.screen.width - self.level_width) / 2][y + (self.screen.height - self.level_height) / 2] = Color(0, 0, 0)
				
	def draw_tetromino(self):
		for x in range(self.current_tetromino.width):
			for y in range(self.current_tetromino.height):
				if self.current_tetromino.map[x][y]:
					a = x + (self.screen.width - self.level_width) / 2 + self.tetromino_pos.x
					b = y + (self.screen.height - self.level_height) / 2 + self.tetromino_pos.y
					if a >= 0 and b >= 0 and a < self.screen.width and b < self.screen.height:
						self.screen.pixel[a][b] = self.current_tetromino.color
	
	def draw_ghost(self):
		pos = self.tetromino_pos
		while self.fits(self.current_tetromino, Point(pos.x, pos.y + 1)):
			pos = Point(pos.x, pos.y + 1)
		
		dark_color = darken_color(self.current_tetromino.color, 0.03)
		for x in range(self.current_tetromino.width):
			for y in range(self.current_tetromino.height):
				if self.current_tetromino.map[x][y]:
					self.screen.pixel[x + (self.screen.width - self.level_width) / 2 + pos.x][y + (self.screen.height - self.level_height) / 2 + pos.y] = dark_color
	
	def draw(self):
		self.screen.clear()
		self.draw_background()
		self.draw_blocks()
		if self.current_tetromino != None:
			self.draw_ghost()
			self.draw_tetromino()
	
	def draw_and_update(self):
		self.draw()
	
		with self.draw_lock:
			self.screen.update()
		
	def pick_tetromino(self):
		self.current_tetromino = random.choice(self.tetrominos).rotate(random.randint(0, 3))
		self.tetromino_pos = Point(self.level_width / 2 - self.current_tetromino.width / 2, 0)
	
	def put_tetromino(self):
		for x in range(self.current_tetromino.width):
			for y in range(self.current_tetromino.height):
				if self.current_tetromino.map[x][y]:
					self.level[x + self.tetromino_pos.x][y + self.tetromino_pos.y] = self.current_tetromino.color
		self.current_tetromino = None
		
	def fits(self, tetromino, position):
		for x in range(tetromino.width):
			for y in range(tetromino.height):
				if tetromino.map[x][y] and (
					x + position.x < 0
					or x + position.x >= self.level_width
					or y + position.y >= self.level_height
					or (y >= 0 and self.level[x + position.x][y + position.y] != None)):
					return False
		return True
		
	def game_over(self):
		print('GAME OVER - Score: ' + str(self.score))

		self.current_tetromino = None		
		self.draw_and_update()
		time.sleep(1)

		particles = []
		line = self.level_height - 1

		last = time.clock()
		detach_next = time.clock()

		while line >= 0 or len(particles) > 0:
			if not self.running:
				return

			now = time.clock()
			dt = now - last
			last = now

			if now > detach_next and line >= 0:
				detach_next += 0.05

				blocks = [x for x in range(self.level_width) if self.level[x][line] != None]
				if len(blocks) == 0:
					line -= 1
					continue
				block = random.choice(blocks)
				particle = Particle(x = block, y = line, color = self.level[block][line])
				self.level[block][line] = None
				particles.append(particle)

			for p in particles:
				p.step(dt)

			particles = [p for p in particles if p.y < self.level_height]	
			
			self.draw()
			for p in particles:
				self.screen.pixel[p.x + (self.screen.width - self.level_width) / 2][int(math.floor(p.y)) + (self.screen.height - self.level_height) / 2] = p.color

			self.screen.update()

		animation = Animation(self.screen, 'tetris/gameover', autoplay = False)
		animation.play_once()

		self.new_game()
		
	def step(self):
		if self.fits(self.current_tetromino, Point(self.tetromino_pos.x, self.tetromino_pos.y + 1)):
			self.tetromino_pos = Point(self.tetromino_pos.x, self.tetromino_pos.y + 1)
		else:
			self.put_tetromino()
			self.check_full_lines()
			self.pick_tetromino()
			if not self.fits(self.current_tetromino, self.tetromino_pos):
				self.game_over()
	
	def tick(self):
		if time.clock() > self.next_step:
			with self.game_lock:
				self.step()
			self.draw_and_update()
			self.next_step += 0.12
		self.check_key_queue()
		self.check_keys()
		time.sleep(0.001)

	def enqueue_key(self, button):
		self.key_queue.append(button)

	def check_key_queue(self):
		while len(self.key_queue) > 0:
			self.on_key_down(self.key_queue[0])
			self.key_queue = self.key_queue[1:]
			
	def on_key_down(self, button):
		with self.game_lock:
			if button == input.Key.Y or button == input.Key.UP:
				center = Point(self.tetromino_pos.x + self.current_tetromino.width / 2, self.tetromino_pos.y + self.current_tetromino.height / 2)
				rotated = self.current_tetromino.rotate()
				new_pos = Point(center.x - rotated.width / 2, center.y - rotated.height / 2)
				if self.fits(rotated, new_pos):
					self.current_tetromino = rotated
					self.tetromino_pos = new_pos
					self.lastinput = time.clock()
					self.draw_and_update()
					
			if button == input.Key.A:
				while self.fits(self.current_tetromino, Point(self.tetromino_pos.x, self.tetromino_pos.y + 1)):
					self.tetromino_pos = Point(self.tetromino_pos.x, self.tetromino_pos.y + 1)
				self.step()
				self.draw_and_update()
			
			self.check_keys(keydown = True)
		if button == input.Key.SELECT:
			self.new_game()
			
	def get_full_lines(self):
		result = []
		for y in range(self.level_height):
			empty = False
			for x in range(self.level_width):
				if self.level[x][y] == None:
					empty = True
			if not empty:
				result.append(y)
		return result
		
	def check_full_lines(self):
		lines = self.get_full_lines()
		if len(lines) == 0:
			return
		
		self.score += len(lines)

		blinks = 4
		for i in range(blinks):
			self.draw()
			for line in lines:
				for x in range(16):
					self.screen.pixel[x][line] = Color(255, 255, 255)
			with self.draw_lock:
				self.screen.update()
			time.sleep(0.02)
			
			self.draw_and_update()
			time.sleep(0.02)
			
		for line in lines:
			for y in reversed(range(line)):
				for x in range(self.level_width):
					self.level[x][y + 1] = self.level[x][y]
			self.draw_and_update()

		self.next_step = time.clock()
				
	def check_keys(self, keydown = False):
		if input.key_state[input.Key.LEFT] and time.clock() - self.lastinput > self.COOLDOWN:
			if self.fits(self.current_tetromino, Point(self.tetromino_pos.x - 1, self.tetromino_pos.y)):
				self.tetromino_pos = Point(self.tetromino_pos.x - 1, self.tetromino_pos.y)
				self.lastinput = time.clock()
				if keydown:
					self.lastinput += self.COOLDOWN * 1.5
				self.draw_and_update()
		if input.key_state[input.Key.RIGHT] and time.clock() - self.lastinput > self.COOLDOWN:
			if self.fits(self.current_tetromino, Point(self.tetromino_pos.x + 1, self.tetromino_pos.y)):
				self.tetromino_pos = Point(self.tetromino_pos.x + 1, self.tetromino_pos.y)
				self.lastinput = time.clock()
				if keydown:
					self.lastinput += self.COOLDOWN	* 1.5		
				self.draw_and_update()
		if input.key_state[input.Key.DOWN] and time.clock() - self.lastinput > self.COOLDOWN:
			if self.fits(self.current_tetromino, Point(self.tetromino_pos.x, self.tetromino_pos.y + 1)):
				self.tetromino_pos = Point(self.tetromino_pos.x, self.tetromino_pos.y + 1)
				self.lastinput = time.clock()
				if keydown:
					self.lastinput += self.COOLDOWN	* 1.5
				self.draw_and_update()
	