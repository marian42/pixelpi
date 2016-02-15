import os.path
import pygame.image
import time
import ConfigParser
from helpers import *
from modules import Module

class Animation(Module):
	def __init__(self, screen, folder, interval = None, autoplay = True):
		super(Animation, self).__init__(screen)

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
		if autoplay:
			self.start()


	def load_frames(self):
		self.frames = []
		i = 0
		while os.path.isfile(self.folder + str(i) + '.bmp'):
			try:
				bmp = pygame.image.load(self.folder + str(i) + '.bmp')
			except Exception:
				print('Error loading ' + str(i) + '.bmp from ' + self.folder)
				raise
			pixel_array = pygame.PixelArray(bmp)
			
			frame = [[pixel_array[x, y] for y in range(16)] for x in range(16)]
			self.frames.append(frame)
			
			i += 1
		
	def is_single_file(self):
		return os.path.isfile(self.folder + '0.bmp') and not os.path.isfile(self.folder + '1.bmp')
	
	def load_single(self):
		self.frames = []
		bmp = pygame.image.load(self.folder + '0.bmp')
		framecount = bmp.get_height() / 16
		pixel_array = pygame.PixelArray(bmp)
			
		for index in range(framecount):
			frame = [[pixel_array[x, y + 16 * index] for y in range(16)] for x in range(16)]
			self.frames.append(frame)
	
	def load_interval(self):
		cfg = ConfigParser.ConfigParser()
		cfg.read(self.folder + 'config.ini')
		return cfg.getint('animation', 'hold')

	def tick(self):
		self.pos += 1
		if self.pos >= len(self.frames):
			self.pos = 0
		self.screen.pixel = self.frames[self.pos]
		self.screen.update()
		time.sleep(self.interval / 1000.0)
		
	def on_start(self):
		print('Starting ' + self.folder)

	def play_once(self):
		for frame in self.frames:
			self.screen.pixel = frame
			self.screen.update()
			time.sleep(self.interval / 1000.0)