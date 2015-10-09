import config

def create_screen():
	if config.virtual_hardware:
		from screen.virtualscreen import VirtualScreen
		return VirtualScreen()
	else:
		from screen.screen import Screen
		return Screen()