from PIL import Image
from helpers.image import Pixels2D
from hw2 import thresholding

def downsampling(img, size):
    width, height = size
    ratio_x, ratio_y = img.width / width, img.height / height
    pixels = Pixels2D(img)

    result = Image.new(img.mode, size)
    result.putdata([pixels[x * ratio_x, y * ratio_y] for y in xrange(height) for x in xrange(width)])
    return result

class SymbolicOperator(object):

    @classmethod
    def _x(cls, pixels, size, center):
        width, height = size
        center_x, center_y = center

        return map(lambda (_x, _y): pixels[_x, _y] if 0 <= _x < width and 0 <= _y < height else 0,
            map(lambda (_x, _y): (center_x + _x, center_y + _y), [
                (0, 0), (1, 0), (0, -1), (-1, 0), (0, 1), (1, 1), (1, -1), (-1, -1), (-1, 1),
            ])
        )

class YokoiConnNumber(SymbolicOperator):

    def __new__(cls, img):
        return [
            str(cls._f(img, (x, y))) if img.getpixel((x, y)) != 0 else ' '
            for y in xrange(img.height) for x in xrange(img.width)
        ]

    @classmethod
    def _f(cls, img, (center_x, center_y)):
        pixels = Pixels2D(img)

        x = cls._x(pixels, img.size, (center_x, center_y))

        a = map(cls._h, [
                (x[0], x[1], x[6], x[2]),
                (x[0], x[2], x[7], x[3]),
                (x[0], x[3], x[8], x[4]),
                (x[0], x[4], x[5], x[1]),
            ])

        return 5 if all(ai == 'r' for ai in a) else a.count('q')

    @classmethod
    def _h(cls, (b, c, d, e)):
        if b != c:
            return 's'
        if b == c == d == e:
            return 'r'
        return 'q'

if __name__ == '__main__':
    img = Image.open('benchmarks/lena.bmp')
    bin_img = thresholding(img, 128)
    small_img = downsampling(bin_img, (64, 64))

    yokoi = YokoiConnNumber(small_img)
    with open('results/yokoi.txt', 'w') as f:
        f.write(
            '\n'.join(
                ''.join(yokoi[i : i + small_img.width])
                for i in xrange(0, len(yokoi), small_img.width)
            )
        )

