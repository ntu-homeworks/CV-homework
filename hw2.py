from PIL import Image

def thresholding(img, at):
	result = Image.new('1', img.size)
	result.putdata(map(lambda x: int(x >= at), img.getdata()))
	return result

if __name__ == '__main__':
	img = Image.open('benchmarks/lena.bmp')

	# 1
	thresholding(img, 128).save('results/thresholding.bmp')

