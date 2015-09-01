from Screen import *
import os.path
import pygame.image
import time
from thread import start_new_thread
import ConfigParser

def int_to_color(c):
	b =  c & 255
	g = (c >> 8) & 255
	r = (c >> 16) & 255
	return Color(r, g, b)

class Animation:
	def load_frames(self):
		self.frames = []
		i = 0
		while os.path.isfile(self.folder + str(i) + '.bmp'):
			try:
				bmp = pygame.image.load(self.folder + str(i) + '.bmp')
			except Exception:
				print('Error loading ' + str(i) + '.bmp from ' + self.folder)
				raise
			arr = pygame.PixelArray(bmp)
			
			frame = [[int_to_color(arr[x, y]) for y in range(16)] for x in range(16)]
			self.frames.append(frame)
			
			i += 1
		
	def is_single_file(self):
		return os.path.isfile(self.folder + '0.bmp') and not os.path.isfile(self.folder + '1.bmp')
	
	def load_single(self):
		self.frames = []
		bmp = pygame.image.load(self.folder + '0.bmp')
		framecount = bmp.get_height() / 16
		arr = pygame.PixelArray(bmp)
			
		for index in range(framecount):
			frame = [[int_to_color(arr[x, y + 16 * index]) for y in range(16)] for x in range(16)]
			self.frames.append(frame)
	
	def load_interval(self):
		cfg = ConfigParser.ConfigParser()
		cfg.read(self.folder + 'config.ini')
		return cfg.getint('animation', 'hold')

	def __init__(self, screen, folder, interval = None, autoplay = True):
		if folder[:-1] != '/':
			folder = folder + '/'
		
		self.folder = folder
		self.screen = screen
		
		try:
			if self.is_single_file():
				self.load_single()
			else: self.load_frames()
			
			if len(self.frames) == 0:
				raise Exception('No frames found in animation ' + self.folder)
			
			self.screen.pixel = self.frames[0]
		except Exception:
			print('Failed to load ' + folder)
			raise
		
		self.screen.update()
		
		if interval == None:
			try:
				self.interval = self.load_interval()
			except:
				print('No interval info found.')
				self.interval = 100
		else: self.interval = interval
		
		self.pos = 0
		self.running = False
		if autoplay:
			self.start()
		
	def run(self):
		while self.running:
			self.pos += 1
			if self.pos >= len(self.frames):
				self.pos = 0
			self.screen.pixel = self.frames[self.pos]
			self.screen.update()
			time.sleep(self.interval / 1000.0)
			
	def start(self):
		if self.running:
			return
			
		print('Starting ' + self.folder)
		self.running = True
		start_new_thread(self.run, ())
		
	def stop(self):
		self.running = False

	def play_once(self):
		for frame in self.frames:
			self.screen.pixel = frame
			self.screen.update()
			time.sleep(self.interval / 1000.0)
		
if __name__ == '__main__':
	import sys

	screen = Screen()
	animation = Animation(screen, sys.argv[1])
	while True:
		time.sleep(1)