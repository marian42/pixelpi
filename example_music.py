from screenfactory import create_screen
from modules.music import Music
import config
import time
import pygame

screen = create_screen()

music = Music(screen)
music.start()

while True:
	if config.virtual_hardware:
		pygame.time.wait(10)
		for event in pygame.event.get():
			pass
	else:
		time.sleep(0.01)