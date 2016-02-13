from animation import *
import time
from os import listdir
import pygame.image
import input

class Gallery(Module):
	def __init__(self, screen):
		super(Gallery, self).__init__(screen)

		input.on_press.append(self.key_press)
		self.paused = False
		
		self.filenames = self.load_filenames("gallery")

		self.images = [None for i in range(len(self.filenames))]
		
		self.interval = 5
		self.position = 0

		self.next_animation = time.time()

	def load_filenames(self, location):
		if location[:1] != '/':
			location = location + '/'
		
		if not os.path.exists(location):
			raise Exception("Path " + location + " not found")
		
		filenames = [location + f for f in listdir(location) if f.endswith(".bmp")]
		filenames.sort()
		
		if len(filenames) == 0:
			raise Exception("No bitmaps found in " + location)

		return filenames

	def move(self, amount):
		self.position = (self.position + amount) % len(self.filenames)
		if self.images[self.position] == None:
			self.load(self.position)
		self.draw()

	def load(self, index):
		try:
			bmp = pygame.image.load(self.filenames[index])
		except Exception:
			print('Error loading ' + self.filenames[index])
			raise

		pixel_array = pygame.PixelArray(bmp)
		
		self.images[index] = [[pixel_array[x, y] for y in range(16)] for x in range(16)]

	def draw(self):
		self.screen.pixel = self.images[self.position]
		self.screen.update()

	def tick(self):
		if not self.paused and time.time() > self.next_animation:
			self.move(1)
			self.next_animation += self.interval
		time.sleep(0.1)

	def key_press(self, key):
		if key == input.Key.RIGHT:
			self.move(1)
			self.next_animation = time.time() + self.interval
		if key == input.Key.LEFT:
			self.move(-1)
			self.next_animation = time.time() + self.interval
		if key == input.Key.A or key == input.Key.ENTER:
			self.paused = not self.paused
			if not self.paused:
				self.next_animation = time.time() + self.interval
			icon = Animation(self.screen, "icons/pause" if self.paused else "icons/play", interval = 800, autoplay = False)
			icon.play_once()			
			self.draw()