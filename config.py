import configparser

filename = 'config.ini'

config = configparser.RawConfigParser()
config.read(filename)

virtual_hardware = config.getboolean('hardware', 'virtualhardware')
default_item_index = config.getint('menu', 'defaultitemindex')
brightness = config.getint('hardware', 'brightness')

use_keyboard = virtual_hardware
use_gamepad = not virtual_hardware
use_buttons = config.getboolean('hardware', 'usebuttons')
verbose_input = config.getboolean('debug', 'verboseinput')

# Only store values that are supposed to be changes
def store():
	config.set('hardware', 'brightness', brightness)
	with open(filename, 'wb') as configfile:
   		config.write(configfile)