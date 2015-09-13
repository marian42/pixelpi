# Use this to switch between virtual and LED screen for examples
use_virtual_screen = True

def create_screen():
	if use_virtual_screen:
		from virtualscreen import VirtualScreen
		return VirtualScreen()
	else:
		from Screen import Screen
		return Screen()