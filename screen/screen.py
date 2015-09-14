from neopixel import *

class Screen:
	def __init__(self, width = 16, height = 16, led_pin = 18, led_freq_hz = 800000, led_dma = 5, led_invert = False, led_brightness = 200):
		self.width = width
		self.height = height
		
		self.strip = Adafruit_NeoPixel(width * height, led_pin, led_freq_hz, led_dma, led_invert, led_brightness)
		self.strip.begin()
		
		self.pixel = [[Color(0,0,0) for y in range(height)] for x in range(width)]
		
	def clear(self, color = Color(0,0,0)):
		for x in range(self.width):
			for y in range(self.height):
				self.pixel[x][y] = color
				
	def update(self):
		for y in range(self.height):
			for x in range(self.width):
				if y % 2 == 0:
					self.strip.setPixelColor(y * self.width + x, self.pixel[x][y])
				else: self.strip.setPixelColor(y * self.width + self.width - 1 - x, self.pixel[x][y])
		self.strip.show()