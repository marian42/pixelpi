import sys
from thread import start_new_thread
import time
import pygame

instance = None

class VirtualGamepad:
	UP = 11
	DOWN = 12
	LEFT = 13
	RIGHT = 14
	
	btn_count = 15

	keycode_list = [
		(pygame.K_LEFT, LEFT),
		(pygame.K_RIGHT, RIGHT),
		(pygame.K_UP, UP),
		(pygame.K_DOWN, UP),
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
	
	def __init__(self, verbose = False):
		self.verbose = verbose
		self.button = [False for i in range(self.btn_count)]
		
		self.on_press = None
		self.on_release = None

		if instance != None:
			raise Exception("Don't create multiple virtual gamepads!")
		
	def press(self, btn):
		self.button[btn] = True
		if self.verbose:
			print('Pressed ' + str(btn))
		if self.on_press != None:
			self.on_press(btn)
		
	def release(self, btn):
		self.button[btn] = False
		if self.verbose:
			print('Released ' + str(btn))
		if self.on_release != None:
			self.on_release(btn)

	def keycode_to_int(self, keycode):
		for relation in self.keycode_list:
			if (relation[0] == keycode):
				return relation[1]

			
	def consume_event(self, event):
		if event.type == pygame.KEYDOWN:
			self.press(self.keycode_to_int(event.key))
		if event.type == pygame.KEYUP:
			self.release(self.keycode_to_int(event.key))

instance = VirtualGamepad()