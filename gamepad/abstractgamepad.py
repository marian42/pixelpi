class AbstractGamepad(object):
	UP = 11
	DOWN = 12
	LEFT = 13
	RIGHT = 14
	
	btn_count = 15

	def __init__(self, verbose = False):
		self.verbose = verbose
		self.button = [False for i in range(self.btn_count)]
		
		self.on_press = None
		self.on_release = None
		
	def press(self, btn):
		self.button[btn] = True
		if self.verbose:
			print('Pressed ' + str(btn))
		if self.on_press != None:
			self.on_press(btn)
		
	def release(self, btn):
		self.button[btn] = False
		if self.verbose:
			print('Released ' + str(btn))
		if self.on_release != None:
			self.on_release(btn)