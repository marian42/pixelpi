import config

def create_gamepad():
	if config.virtual_hardware:
		from gamepad.virtualgamepad import instance
		return instance
	else:
		from gamepad.gamepad import Gamepad
		return Gamepad()