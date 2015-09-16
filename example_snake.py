from screenfactory import create_screen
from gamepadfactory import create_gamepad
from modules.snake import *
from gamepad.virtualgamepad import *

screen = create_screen()
gamepad = create_gamepad()

snake = Snake(screen, gamepad)
while True:
	pygame.time.wait(10)
	for event in pygame.event.get():
		instance.consume_event(event)