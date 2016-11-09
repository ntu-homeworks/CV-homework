from PIL import Image
from hw2 import thresholding
from helpers.image import PixelSet

class BinaryMorphology(object):
    # Arguments are expected to be `PixelSet`

    @classmethod
    def dilation(cls, a, b):
        width, height = a.size
        result = PixelSet(filter(lambda (x, y): 0 <= x < width and 0 <= y < height, [(ax + bx, ay + by) for (ax, ay) in a for (bx, by) in b]))
        result.size, result.origin = a.size, a.origin
        return result

    @classmethod
    def erosion(cls, a, b):
        width, height = a.size
        result = PixelSet([(x, y) for x in range(width) for y in range(height) if all([(x + bx, y + by) in a for (bx, by) in b])])
        result.size, result.origin = a.size, a.origin
        return result

    @classmethod
    def opening(cls, b, k):
        return cls.dilation(cls.erosion(b, k), k)

    @classmethod
    def closing(cls, b, k):
        return cls.erosion(cls.dilation(b, k), k)

    @classmethod
    def hit_and_miss(cls, a, j, k):
        result = cls.erosion(a, j) & cls.erosion(a.complement, k)
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

    BinaryMorphology.dilation(white_set, oct_kernel).to_image().save('results/dilation.bmp')
    BinaryMorphology.erosion(white_set, oct_kernel).to_image().save('results/erosion.bmp')
    BinaryMorphology.opening(white_set, oct_kernel).to_image().save('results/opening.bmp')
    BinaryMorphology.closing(white_set, oct_kernel).to_image().save('results/closing.bmp')

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

    BinaryMorphology.hit_and_miss(white_set, j, k).to_image().save('results/hit_and_miss.bmp')

