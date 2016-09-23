from helpers.image import Pixels2D
from PIL import Image

def upside_down(img):
	data = Pixels2D(img)

	for x in range(img.width):
		for y in range(img.height / 2):
			data[x, y], data[x, img.height - 1 - y] = data[x, img.height - 1 - y], data[x, y]

	result = Image.new(img.mode, img.size)
	result.putdata(data.data)
	result.save('results/upside_down.bmp')

if __name__ == '__main__':
	img = Image.open('benchmarks/lena.bmp')
	
	# 1
	upside_down(img)

