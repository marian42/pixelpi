from Animation import *
import time
import os
import random

class Cycle:
	def __init__(self, screen, location, interval = 20000):
		if location[:1] != '/':
			location = location + '/'
		
		subfolders = [x[0] for x in os.walk(location)]
		self.subfolders = subfolders[1:]
		
		self.animations = [None for i in range(len(self.subfolders))]
		self.current = None
		
		self.screen = screen
		self.interval = interval
		
	def next(self):
		if self.current != None:
			self.current.stop()
		
		index = random.randint(0, len(self.animations) - 1)
		
		if self.animations[index] == None:
			self.animations[index] = Animation(self.screen, self.subfolders[index])
			
		self.current = self.animations[index]
		self.current.start()
		
	def run(self):
		while True:
			self.next()
			time.sleep(self.interval / 1000.0)
			
if __name__ == '__main__':
	import sys

	screen = Screen()
	cycle = Cycle(screen, sys.argv[1] if len(sys.argv) > 1 else 'animations')
	cycle.run()
		