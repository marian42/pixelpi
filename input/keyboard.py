import pygame
from input import *

class UnknownKeyException(Exception):
	pass

keycode_list = [
	(pygame.K_LEFT, Key.LEFT),
	(pygame.K_RIGHT, Key.RIGHT),
	(pygame.K_UP, Key.UP),
	(pygame.K_DOWN, Key.DOWN),
	(pygame.K_0, Key.HOME),
	(pygame.K_1, 1),
	(pygame.K_2, 2),
	(pygame.K_3, 3),
	(pygame.K_4, 4),
	(pygame.K_5, 5),
	(pygame.K_6, 6),
	(pygame.K_7, 7),
	(pygame.K_8, 8),
	(pygame.K_9, 9),
	(pygame.K_BACKSPACE, Key.BACK),
	(pygame.K_RETURN, Key.ENTER)
]
		
def _keycode_to_int( keycode):
	for relation in keycode_list:
		if (relation[0] == keycode):
			return relation[1]
	raise UnknownKeyException
			
def _keyboard_tick():
	for event in pygame.event.get():
		_consume_event(event)

def _consume_event(event):
	try:
		if event.type == pygame.KEYDOWN:
			press(_keycode_to_int(event.key))
		if event.type == pygame.KEYUP:
			release(_keycode_to_int(event.key))
	except UnknownKeyException:
		if event.type == pygame.KEYDOWN:
			print("Unknown key pressed. Use arrow keys and number keys.")

on_tick.append(_keyboard_tick)
available_input_methods.append('keyboard')