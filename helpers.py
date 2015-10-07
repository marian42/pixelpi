import collections
import colorsys

def Color(r, g, b):
	return r * 65536 + g * 256 + b

RGBColor = collections.namedtuple('RGBColor', 'r g b')

def int_to_color(c):
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