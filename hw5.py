from PIL import Image
from helpers.image import ImageFunction
from hw4 import BinaryMorphology

class GreyscaleMorphology(BinaryMorphology):
    # Arguments are expected to be `ImageFunction`s.

    @classmethod
    def dilation(cls, a, b):
        return a

    @classmethod
    def erosion(cls, a, b):
        return a

    @classmethod
    def hit_and_miss(cls, a, j, k):
        raise AttributeError('There is no greysclae "Hit and Miss" operation.')

if __name__ == '__main__':
    img = Image.open('benchmarks/lena.bmp')

    img_func = ImageFunction.from_image(img)

    oct_kernel = ImageFunction(
        func=lambda (x, y): 0,
        domain=(
            (x, y) 
            for x in xrange(-2, 3) for y in xrange(-2, 3)
            if not(x in (-2, 2) and y in (-2, 2))
        )
    )

    GreyscaleMorphology.dilation(img_func, oct_kernel).to_image('L', img.size).save('results/grey_dilation.bmp')
    GreyscaleMorphology.erosion(img_func, oct_kernel).to_image('L', img.size).save('results/grey_erosion.bmp')
    GreyscaleMorphology.opening(img_func, oct_kernel).to_image('L', img.size).save('results/grey_opening.bmp')
    GreyscaleMorphology.closing(img_func, oct_kernel).to_image('L', img.size).save('results/grey_closing.bmp')

