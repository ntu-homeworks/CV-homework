from PIL import Image
from helpers.image import Pixels2D

def thresholding(img, at):
	result = Image.new('1', img.size)
	result.putdata(map(lambda x: int(x >= at), img.getdata()))
	return result

def histogram(img):
	result = [0] * 256
	for p in img.getdata():
		result[p] += 1
	return result

def draw_histogram(result):
	height = max(result) * 4 / 3
	result_img = Image.new('1', (256, height))

	result_data = Pixels2D([1] * 256 * height, width=256)
	for x, h in enumerate(result):
		for y in range(h):
			result_data[x, height - 1 - y] = 0

	result_img.putdata(result_data.data)
	return result_img.resize((height, height))

if __name__ == '__main__':
	img = Image.open('benchmarks/lena.bmp')

	# 1
	thresholding(img, 128).save('results/thresholding.bmp')

	# 2
	draw_histogram(histogram(img)).save('results/histogram.bmp')

