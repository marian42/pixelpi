# From http://nessy.info/?p=62, modified

from input import *
import time
from thread import start_new_thread

def _process_byte(byte, button):
	if byte == ['01', '00', button, '01', '01', '00', '00', '00']:
		press(int(button) - 19)
	elif byte == ['01', '00', button, '01', '00', '00', '00', '00']:
		release(int(button) - 19)

def _run():
	byte = []
	while True:
		# read from the device pipe and set the byte
		for bit in _pipe.read(1):
			byte.append('%02X' % ord(bit))

			# 8 bits make a byte
			if len(byte) == 8:

				if byte[2] in ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29']:
					_process_byte(byte, byte[2])

				if byte[0] == '03':
					# Arrow Up
					if byte == ['03', '00', '01', '00', '01', '00', '00', '00']:
						press(Key.UP)

					# Arrow Down					
					if byte == ['03', '00', '01', '00', 'FE', '00', '00', '00']:
						press(Key.DOWN)
						
					# Arrow Left
					if byte == ['03', '00', '00', '00', '01', '00', '00', '00']:
						press(Key.LEFT)

					# Arrow Right				
					if byte == ['03', '00', '00', '00', 'FE', '00', '00', '00']:
						press(Key.RIGHT)

					# Release Arrow					
					if byte == ['03', '00', '01', '00', '80', '00', '00', '00'] or byte == ['03', '00', '00', '00', '80', '00', '00', '00']:
						for btn in [Key.UP, Key.DOWN, Key.LEFT, Key.RIGHT]:
							if key_state[btn]:
								release(btn)

				# empty byte
				byte = []

_pipe = None
try:
	_pipe = open('/dev/input/by-id/usb-Logitech_Logitech_Dual_Action-event-joystick', 'r')
	available_input_methods.append('gamepad')
	start_new_thread(_run, ())
except IOError:
	print("No gamepad connected")