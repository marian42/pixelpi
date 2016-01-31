import sys
import time
import pygame
from abstractgamepad import AbstractGamepad;

instance = None

class VirtualGamepad(AbstractGamepad):	
	def __init__(self, verbose = False):
		super(VirtualGamepad, self).__init__(verbose)

		self.keycode_list = [
			(pygame.K_LEFT, self.LEFT),
			(pygame.K_RIGHT, self.RIGHT),
			(pygame.K_UP, self.UP),
			(pygame.K_DOWN, self.DOWN),
			(pygame.K_0, 10),
			(pygame.K_1, 1),
			(pygame.K_2, 2),
			(pygame.K_3, 3),
			(pygame.K_4, 4),
			(pygame.K_5, 5),
			(pygame.K_6, 6),
			(pygame.K_7, 7),
			(pygame.K_8, 8),
			(pygame.K_9, 9)
		]

		if instance != None:
			raise Exception("Don't create multiple virtual gamepads!")
		
	def keycode_to_int(self, keycode):
		for relation in self.keycode_list:
			if (relation[0] == keycode):
				return relation[1]
			
	def tick(self)
		for event in pygame.event.get():
			self.consume_event(event)

	def consume_event(self, event):
		if event.type == pygame.KEYDOWN:
			self.press(self.keycode_to_int(event.key))
		if event.type == pygame.KEYUP:
			self.release(self.keycode_to_int(event.key))

instance = VirtualGamepad()