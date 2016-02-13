import config

def enum(**enums):
    return type('Enum', (), enums)

Key = enum(X = 1, Y = 4, A = 2, B = 3, L1 = 5, R1 = 6, L2 = 7, R2 = 8, SELECT = 9, HOME = 10, UP = 11, DOWN = 12, LEFT = 13, RIGHT = 14, BACK = 15, ENTER = 16)

TOTAL_KEYS = 17

_verbose = config.verbose_input
key_state = [False for i in range(TOTAL_KEYS)]

on_press = []
on_release = []
on_tick = []

available_input_methods = []
	
def press(key):
	if not key in range(TOTAL_KEYS):
		print "Unknown key!"
		return

	key_state[key] = True
	if _verbose:
		print('Pressed ' + str(key))
	for callback in on_press:
		event_handled = callback(key)
		if event_handled:
			return
		
def release(key):
	if not key in range(TOTAL_KEYS):
		print "Unknown key!"
		return

	key_state[key] = False
	if _verbose:
		print('Released ' + str(key))
	for callback in on_release:
		event_handled = callback(key)
		if event_handled:
			return

def tick():
	for callback in on_tick:
		callback()

if config.use_gamepad:
	import input.gamepad
if config.use_keyboard:
	import input.keyboard
if config.use_buttons:
	import input.buttons