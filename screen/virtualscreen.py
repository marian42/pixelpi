import pygame
import collections
from abstractscreen import AbstractScreen

# Behaves like the actual LED screen, but shows the screen content on a computer screen
class VirtualScreen(AbstractScreen):
	def __init__(self, width = 16, height = 16, led_pin = 18, led_freq_hz = 800000, led_dma = 5, led_invert = False, led_brightness = 200):		
		super(VirtualScreen, self).__init__(width, height)
		self.pixel_size = 30
		
		pygame.display.init()
		self.screen = pygame.display.set_mode([width * self.pixel_size, height * self.pixel_size], 0)
		self.surface = pygame.Surface(self.screen.get_size())	
				
	def update(self):
		for y in range(self.height):
			for x in range(self.width):
				pygame.draw.rect(self.surface, self.pixel[x][y], ((x * self.pixel_size, y * self.pixel_size), (((x+1) * self.pixel_size), (y+1) * self.pixel_size)))

		self.screen.blit(self.surface, (0, 0))
		pygame.display.flip()
		pygame.display.update()