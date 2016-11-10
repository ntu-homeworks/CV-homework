from helpers.image import Pixels2D
from PIL import Image

def upside_down(img):
	data = Pixels2D(img)

	for x in xrange(img.width):
		for y in xrange(img.height / 2):
			data[x, y], data[x, img.height - 1 - y] = data[x, img.height - 1 - y], data[x, y]

	result = Image.new(img.mode, img.size)
	result.putdata(data.data)
	result.save('results/upside_down.bmp')

def right_side_left(img):
	data = Pixels2D(img)

	for y in xrange(img.height):
		for x in xrange(img.width / 2):
			data[x, y], data[img.width - 1 - x, y] = data[img.width - 1 - x, y], data[x, y]

	result = Image.new(img.mode, img.size)
	result.putdata(data.data)
	result.save('results/right_side_left.bmp')

def diagonally_mirror(img):
	data = Pixels2D(img)

	for y in xrange(img.height):
		for x in xrange(y):
			data[x, y] = data[y, x]

	result = Image.new(img.mode, img.size)
	result.putdata(data.data)
	result.save('results/diagonally_mirror.bmp')

if __name__ == '__main__':
	img = Image.open('benchmarks/lena.bmp')
	
	# 1
	upside_down(img)

	# 2
	right_side_left(img)

	# 3
	diagonally_mirror(img)

