# From http://nessy.info/?p=62

import sys
import time
from abstractgamepad import AbstractGamepad
from thread import start_new_thread

class Gamepad(AbstractGamepad):
	def __init__(self, verbose = False):
		super(Gamepad, self).__init__(verbose)

		self.pipe = None
		try:
			self.pipe = open('/dev/input/by-id/usb-Logitech_Logitech_Dual_Action-event-joystick', 'r')
		except IOError:
			print("No gamepad connected")
		
		self.start()

	def available(self):
		return self.pipe != None

	def start(self):
		self.running = True
		if self.available():
			start_new_thread(self.run, ())
		
	def stop(self):
		self.running = False
		
	def check(self, byte, button):
		if byte == ['01', '00', button, '01', '01', '00', '00', '00']:
			self.press(int(button) - 19)
		elif byte == ['01', '00', button, '01', '00', '00', '00', '00']:
			self.release(int(button) - 19)

	def run(self):
		byte = []
		while self.running:
			# read from the device pipe and set the byte
			for bit in self.pipe.read(1):
				byte.append('%02X' % ord(bit))

				# 8 bits make a byte
				if len(byte) == 8:

					if byte[2] in ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']:
						self.check(byte, byte[2])

					if byte[0] == '03':
						# Arrow Up
						if byte == ['03', '00', '01', '00', '01', '00', '00', '00']:
							self.press(self.UP)

						# Arrow Down					
						if byte == ['03', '00', '01', '00', 'FE', '00', '00', '00']:
							self.press(self.DOWN)
							
						# Arrow Left
						if byte == ['03', '00', '00', '00', '01', '00', '00', '00']:
							self.press(self.LEFT)

						# Arrow Right				
						if byte == ['03', '00', '00', '00', 'FE', '00', '00', '00']:
							self.press(self.RIGHT)

						# Release Arrow					
						if byte == ['03', '00', '01', '00', '80', '00', '00', '00'] or byte == ['03', '00', '00', '00', '80', '00', '00', '00']:
							for btn in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
								if self.button[btn]:
									self.release(btn)

					# empty byte
					byte = []
		time.sleep(0.010)
				
if __name__ == '__main__':
	gamepad = Gamepad(verbose = True)
	while True:
		time.sleep(1)