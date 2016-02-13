from animation import *
import time
import os
import random
import input

class Cycle(Module):
	def __init__(self, screen, location, interval = 20):
		super(Cycle, self).__init__(screen)

		input.on_press.append(self.key_press)
		self.paused = False
		
		self.subfolders = self.load_subfolders(location)

		self.animations = [None for i in range(len(self.subfolders))]
		
		self.interval = interval

		self.history = []
		self.history_position = -1
		self.next_animation = time.time()

	def load_subfolders(self, location):
		if location[:1] != '/':
			location = location + '/'
		
		if not os.path.exists(location):
			raise Exception("Path " + location + " not found")
		subfolders = [x[0] for x in os.walk(location)]
		
		subfolders = subfolders[1:]

		if len(subfolders) == 0:
			raise Exception("No animations found in " + location)

		return subfolders

	def get_current_animation(self):
		if self.history_position < 0:
			return None

		index = self.history[self.history_position]
		if self.animations[index] == None:
			self.animations[index] = Animation(self.screen, self.subfolders[index])
		return self.animations[index]
		
	def next(self, pick_random):
		if self.get_current_animation() != None:			
			self.get_current_animation().stop()
		
		
		if self.history_position < len(self.history) - 1:
			self.history_position += 1
			index = self.history[self.history_position]
		else:
			if pick_random:
				index = random.randint(0, len(self.animations) - 1)
				self.history_position += 1
			else:
				index = (self.history[self.history_position] + 1) % len(self.animations)
				self.history_position += 1
			self.history.append(index)	

		self.get_current_animation().start()
		
	def tick(self):
		if not self.paused and time.time() > self.next_animation:
			self.next(pick_random = True)
			self.next_animation += self.interval
		time.sleep(0.1)

	def on_stop(self):
		if self.get_current_animation() != None:
			self.get_current_animation().stop()

	def key_press(self, key):
		if key == input.Key.RIGHT:
			self.next(pick_random = False)
		if key == input.Key.LEFT:
			if self.history_position > 0:
				self.get_current_animation().stop()
				self.history_position -= 1
				self.get_current_animation().start()
		if key == input.Key.A or key == input.Key.ENTER:
			self.paused = not self.paused
			if not self.paused:
				self.next_animation = time.time() + self.interval
			self.get_current_animation().stop()
			icon = Animation(self.screen, "icons/pause" if self.paused else "icons/play", interval = 800, autoplay = False)
			icon.play_once()			
			self.get_current_animation().start()
