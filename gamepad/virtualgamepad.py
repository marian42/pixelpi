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
		if (keycode == pygame.K_LEFT):
			return self.LEFT
		if (keycode == pygame.K_RIGHT):
			return self.RIGHT
		if (keycode == pygame.K_UP):
			return self.UP
		if (keycode == pygame.K_DOWN):
			return self.DOWN

			
	def consume_event(self, event):
		if event.type == pygame.KEYDOWN:
			self.press(self.keycode_to_int(event.key))
		if event.type == pygame.KEYUP:
			self.release(self.keycode_to_int(event.key))

instance = VirtualGamepad()