import pygame
from modules.cycle import Cycle
from screenfactory import create_screen
import time
import config

screen = create_screen()

cycle = Cycle(screen, 'animations')
cycle.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.01)