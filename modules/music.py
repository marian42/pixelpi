import time
import math
from helpers import *
from modules import Module
import serial
from thread import start_new_thread

class Music(Module):
	def __init__(self, screen):
		super(Music, self).__init__(screen)
		self.serial = serial.Serial('/dev/ttyAMA0', 9600)
		self.data = [0 for i in range(7)]
		self.position = 0
		start_new_thread(self.check_serial, ())

	def check_serial(self):
		while self.running:
			try:
				byte = ord(self.serial.read())
				if byte == 255:
					self.position = 0
					print ", ".join([str(self.data[c]) for c in range(7)])
				elif self.position < 7:
					self.data[self.position] = byte
					self.position += 1
			except Exception as e:
				print e
	
	def tick(self):
		self.draw()

	def draw(self):
		self.screen.clear()

		for channel in range(7):
			self.screen.pixel[channel][0] = Color(self.data[channel], self.data[channel], self.data[channel])
		if sum(self.data) == 0:
			self.screen.pixel[7][0] = Color(255, 0, 0)
		
		self.screen.update()

	def on_stop(self):
		self.serial.close()
