from screenfactory import create_screen
from gamepadfactory import create_gamepad
from modules.snake import *
import time
import config
import pygame

screen = create_screen()
gamepad = create_gamepad()

snake = Snake(screen, gamepad)
snake.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			snake.gamepad.consume_event(event)
	else:
		time.sleep(0.01)