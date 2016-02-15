from modules import Module
import input

from puzzle import *

class WitnessGame(Module):
	def __init__(self, screen):
		super(WitnessGame, self).__init__(screen)
		
		self.new_game()

		input.on_press.append(self.on_key_down)

		self.key_queue = []

		self.wrong_path = None

		self.draw()
		self.screen.fade_in(0.4)
	
	def draw(self):
		self.puzzle.draw(self.screen)
		self.path.draw()
		if self.wrong_path != None and len(self.path.steps) == 0:
			self.wrong_path.draw()

	def tick(self):
		if (len(self.key_queue) != 0):
			self.handle_key(self.key_queue.pop(0))

		self.draw()		
		self.screen.update()
		time.sleep(0.01)

	def on_key_down(self, key):
		self.key_queue.append(key)

	def handle_key(self, key):		
		if key == input.Key.UP:
			self.path.move(Point(0, -1))
		if key == input.Key.DOWN:
			self.path.move(Point(0, 1))
		if key == input.Key.LEFT:
			self.path.move(Point(-1, 0))
		if key == input.Key.RIGHT:
			self.path.move(Point(1, 0))
		if key == input.Key.A:
			if len(self.path.steps) == 0:
				self.wrong_path = None
				self.path.start()
				return

			if self.path.check():
				self.puzzle.solve()
				self.draw()
				self.screen.update()
				time.sleep(1)

				self.screen.fade_out(0.4)
				self.new_game()
				self.draw()
				self.screen.fade_in(0.4)

				self.path.offset_start = time.clock()
				self.path.offset_end = self.path.offset_start + self.path.offset_time
			else:
				self.wrong_path = self.path
				self.wrong_path.wrong = True
				self.wrong_path.wrong_since = time.clock()
				self.path = Path(self.puzzle, self.screen)

		if key == input.Key.B and len(self.path.steps) > 0:
			self.path = Path(self.puzzle, self.screen)

	def new_game(self):
		self.puzzle = Puzzle(self.screen)
		self.path = Path(self.puzzle, self.screen)		