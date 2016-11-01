from PIL import Image
from hw2 import thresholding
from helpers.image import PixelSet

def dilation(a, b):
    width, height = a.size
    result = PixelSet(filter(lambda (x, y): 0 <= x < width and 0 <= y < height, [(ax + bx, ay + by) for (ax, ay) in a for (bx, by) in b]))
    result.size, result.origin = a.size, a.origin
    return result

def erosion(a, b):
    width, height = a.size
    result = PixelSet([(x, y) for x in range(width) for y in range(height) if all([(x + bx, y + by) in a for (bx, by) in b])])
    result.size, result.origin = a.size, a.origin
    return result

def opening(b, k):
    return dilation(erosion(b, k), k)

def closing(b, k):
    return erosion(dilation(b, k), k)

def hit_and_miss(a, j, k):
    result = erosion(a, j) & erosion(a.complement, k)
    result.size, result.origin = a.size, a.origin
    return result

if __name__ == '__main__':
    img = Image.open('benchmarks/lena.bmp')
    white_set = PixelSet.from_image(thresholding(img, 128), value=1)

    oct_kernel = PixelSet.from_pixels([
        0, 1, 1, 1, 0,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        0, 1, 1, 1, 0,
    ], size=(5, 5), value=1, origin=(2, 2))

    dilation(white_set, oct_kernel).to_image().save('results/dilation.bmp')
    erosion(white_set, oct_kernel).to_image().save('results/erosion.bmp')
    opening(white_set, oct_kernel).to_image().save('results/opening.bmp')
    closing(white_set, oct_kernel).to_image().save('results/closing.bmp')

    j = PixelSet.from_pixels([
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        1, 1, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 0, 0, 0, 0,
    ], size=(5, 5), value=1, origin=(1, 2))
    k = PixelSet.from_pixels([
        0, 0, 0, 0, 0,
        0, 1, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
    ], size=(5, 5), value=1, origin=(1, 2))

    hit_and_miss(white_set, j, k).to_image().save('results/hit_and_miss.bmp')

