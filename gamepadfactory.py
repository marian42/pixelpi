# Use this to switch between virtual and LED screen for examples
use_virtual_gamepad = True

def create_gamepad():
	if use_virtual_gamepad:
		from gamepad.virtualgamepad import instance
		return instance
	else:
		from gamepad.gamepad import Gamepad
		return Gamepad()