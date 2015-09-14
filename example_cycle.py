import sys
import os
sys.path.append(os.path.dirname(os.path.realpath('')))

import pygame
from modules.cycle import Cycle
from screenfactory import create_screen

screen = create_screen()

cycle = Cycle(screen, 'animations')
cycle.start()

while True:
	pygame.time.wait(10)
	for event in pygame.event.get():
		pass