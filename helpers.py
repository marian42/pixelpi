import collections

Color = collections.namedtuple('Color', 'r g b')

def int_to_color(c):
	b =  c & 255
	g = (c >> 8) & 255
	r = (c >> 16) & 255
	return Color(r, g, b)

Point = collections.namedtuple('Point', 'x y')