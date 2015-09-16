from screenfactory import create_screen
from gamepadfactory import create_gamepad
from modules.tetris import *
from gamepad.virtualgamepad import *

screen = create_screen()
gamepad = create_gamepad()

tetris = Tetris(screen, gamepad)
while True:
	pygame.time.wait(10)
	for event in pygame.event.get():
		instance.consume_event(event)