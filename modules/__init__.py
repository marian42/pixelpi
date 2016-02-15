from thread import start_new_thread
from helpers import *

class Module(object):
	def __init__(self, screen):
		self.screen = screen
		self.running = False

	def tick(self):
		raise Exception("All modules must implement tick")

	def run(self):
		while self.running:
			self.tick()

	def start(self):
		if self.running:
			return
		
		self.running = True
		start_new_thread(self.run, ())

		self.on_start()
 		
	def stop(self):
		self.running = False
		self.on_stop()

	def on_start(self):
		pass

	def on_stop(self):
		pass