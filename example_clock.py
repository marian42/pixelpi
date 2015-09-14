from screenfactory import create_screen
from modules.clock import Clock
import pygame

screen = create_screen()

clock = Clock(screen)
clock.start()

while True:
	pygame.time.wait(10)
	for event in pygame.event.get():
		pass