import sys
import os
sys.path.append(os.path.dirname(os.path.realpath('')))

from Cycle import *
from screenfactory import create_screen
from thread import start_new_thread

screen = create_screen()

cycle = Cycle(screen, 'animations')

start_new_thread(cycle.run, ())

while True:
	pygame.time.wait(10)
	for event in pygame.event.get():
		pass