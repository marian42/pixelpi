from thread import start_new_thread
from helpers import *

class Module(object):
	def __init__(self, screen, autoplay = True):
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

		if getattr(self, "on_start", None) != None and callable(getattr(self, "on_start", None)):
			self.on_start()
 		
	def stop(self):
		self.running = False