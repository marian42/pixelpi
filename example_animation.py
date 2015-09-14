import sys
import os
sys.path.append(os.path.dirname(os.path.realpath('')))

from screenfactory import create_screen
from modules.animation import *

screen = create_screen()

animation = Animation(screen, "animations/pacman")
while True:
	pygame.time.wait(10)
	for event in pygame.event.get():
		pass