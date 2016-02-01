import collections
import colorsys

def Color(r, g, b):
	return r * 65536 + g * 256 + b

RGBColor = collections.namedtuple('RGBColor', 'r g b')

def int_to_rgb_color(c):
	b =  c & 255
	g = (c >> 8) & 255
	r = (c >> 16) & 255
	return RGBColor(r, g, b)

Point = collections.namedtuple('Point', 'x y')

def hsv_to_color(hue, saturation, value):
	t = colorsys.hsv_to_rgb(hue, saturation, value)
	return Color(int(t[0] * 255), int(t[1] * 255), int(t[2] * 255))

def rgb_to_int(c):
	return Color(c.r, c.g, c.b)

def darken_color(color, factor): # 0 is darkest, 1 is no change
	b =  color & 255
	g = (color >> 8) & 255
	r = (color >> 16) & 255
	return Color(int(r * factor), int(g * factor), int(b * factor))

def brighten_color(color, factor): # 0 is brightest, 1 is no change
	b =  color & 255
	g = (color >> 8) & 255
	r = (color >> 16) & 255
	return Color(int(255 - (255 - r) * factor), int(255 - (255 - g) * factor), int(255 - (255 - b) * factor))

def blend_colors(color1, color2, progress):
	b1 =  color1 & 255
	g1 = (color1 >> 8) & 255
	r1 = (color1 >> 16) & 255

	b2 =  color2 & 255
	g2 = (color2 >> 8) & 255
	r2 = (color2 >> 16) & 255

	inverted_progress = 1.0 - progress
	return Color(int(inverted_progress * r1 + progress * r2), int(inverted_progress * g1 + progress * g2), int(inverted_progress * b1 + progress * b2))
	