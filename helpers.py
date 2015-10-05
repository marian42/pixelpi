import collections
import colorsys

Color = collections.namedtuple('Color', 'r g b')

def int_to_color(c):
	b =  c & 255
	g = (c >> 8) & 255
	r = (c >> 16) & 255
	return Color(r, g, b)

Point = collections.namedtuple('Point', 'x y')

def hsv_to_color(hue, saturation, value):
	t = colorsys.hsv_to_rgb(hue, saturation, value)
	return Color(int(t[0] * 255), int(t[1] * 255), int(t[2] * 255))
