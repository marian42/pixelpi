from screenfactory import create_screen
from gamepadfactory import create_gamepad
from modules.tetris import *
import time
import config

screen = create_screen()
gamepad = create_gamepad()

tetris = Tetris(screen, gamepad)
while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			tetris.gamepad.consume_event(event)
	else:
		time.sleep(0.01)