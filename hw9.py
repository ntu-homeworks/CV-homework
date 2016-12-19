from helpers.image import Pixels2D
from PIL import Image

class ExpendedPixels2D(Pixels2D):
    def __init__(self, *args, **kwargs):
        super(ExpendedPixels2D, self).__init__(*args, **kwargs)
        if 'size' in kwargs:
            self.size = kwargs['size']
        if not hasattr(self, 'size'):
            raise ValueError("Size is required.")

    def _get_index(self, xy):
        if isinstance(xy, tuple) and len(xy) == 2:
            xy = tuple(map(lambda (c, s): 0 if c < 0 else s - 1 if c >= s else c, zip(xy, self.size)))
        return super(ExpendedPixels2D, self)._get_index(xy)


class PixelRegion(object):
    def __init__(self, pixels, coor, size):
        self.size = size
        self.data = [pixels[tuple(map(lambda c, o: c + o - self.origin, coor, (x, y)))] for y in xrange(size) for x in xrange(size)]

    origin = property(lambda self: (self.size - 1) / 2)


class Mask(object):
    def __init__(self, data):
        self.size = int(len(data) ** 0.5)
        if self.size ** 2 != len(data):
            raise ValueError("Data is not valid. (not a square?)")

        self.origin = (self.size - 1) / 2
        self.data = data

    def __rmul__(self, other):
        if isinstance(other, PixelRegion) and self.size == other.size:
            return sum(l * r for l, r in zip(self.data, other.data))
        return NotImplemented

class GradientEdgeDetector(object):
    r = lambda self, i, coor: PixelRegion(self.pixels, coor, self.masks[i].size) * self.masks[i]

    def __init__(self, img):
        self.pixels = ExpendedPixels2D(img, size=img.size)

    def get_edge_mag(self, threshold):
        result = Image.new('1', self.pixels.size)
        result.putdata([
            0 if self.get_magnitude((x, y)) >= threshold else 1
            for y in xrange(self.pixels.size[1]) for x in xrange(self.pixels.size[0])
        ])
        return result

    def get_edge_dir(self):
        raise NotImplementedError


class SOSGradientEdgeDetector(GradientEdgeDetector):
    get_magnitude = lambda self, *args: sum(self.r(i, *args) ** 2 for i in range(2)) ** 0.5
    def get_direction(self, *args): raise NotImplementedError


class MaxGradientEdgeDetector(GradientEdgeDetector):
    get_magnitude = lambda self, *args: max(self.r(i, *args) for i in range(len(self.masks)))
    def get_direction(self, *args): raise NotImplementedError


class RobertEdgeDetector(SOSGradientEdgeDetector):
    masks = [
        Mask([-1, 0,
               0, 1,]),
        Mask([ 0,-1,
               1, 0,]),
    ]

class PrewittEdgeDetector(SOSGradientEdgeDetector):
    masks = [
        Mask([-1,-1,-1,
               0, 0, 0,
               1, 1, 1,]),
        Mask([-1, 0, 1,
              -1, 0, 1,
              -1, 0, 1,]),
    ]

class SobelEdgeDetector(SOSGradientEdgeDetector):
    masks = [
        Mask([-1,-2,-1,
               0, 0, 0,
               1, 2, 1,]),
        Mask([-1, 0, 1,
              -2, 0, 2,
              -1, 0, 1,]),
    ]

class FreiChenEdgeDetector(SOSGradientEdgeDetector):
    masks = [
        Mask([-1,-2**0.5,-1,
               0,      0, 0,
               1, 2**0.5, 1,]),
        Mask([-1,      0, 1,
              -2**0.5, 0, 2**0.5,
              -1,      0, 1,])
    ]

class KirschEdgeDetector(MaxGradientEdgeDetector):
    masks = [
        Mask([-3,-3, 5,
              -3, 0, 5,
              -3,-3, 5,]),
        Mask([-3, 5, 5,
              -3, 0, 5,
              -3,-3,-3,]),
        Mask([ 5, 5, 5,
              -3, 0,-3,
              -3,-3,-3,]),
        Mask([ 5, 5,-3,
               5, 0,-3,
              -3,-3,-3,]),
        Mask([ 5,-3,-3,
               5, 0,-3,
               5,-3,-3,]),
        Mask([-3,-3,-3,
               5, 0,-3,
               5, 5,-3,]),
        Mask([-3,-3,-3,
              -3, 0,-3,
               5, 5, 5,]),
        Mask([-3,-3,-3,
              -3, 0, 5,
              -3, 5, 5,]),
    ]

class RobinsonEdgeDetector(MaxGradientEdgeDetector):
    masks = [
        Mask([-1, 0, 1,
              -2, 0, 2,
              -1, 0, 1,]),
        Mask([ 0, 1, 2,
              -1, 0, 1,
              -2,-1, 0,]),
        Mask([ 1, 2, 1,
               0, 0, 0,
              -1,-2,-1,]),
        Mask([ 2, 1, 0,
               1, 0,-1,
               0,-1,-2,]),
        None, None, None, None,
    ]

    def r(self, i, *args):
        if i >= 4:
            return -super(RobinsonEdgeDetector, self).r(i-4, *args)
        return super(RobinsonEdgeDetector, self).r(i, *args)

class NevatiaBabuEdgeDetector(MaxGradientEdgeDetector):
    masks = [
        Mask([
             100, 100, 100, 100, 100,
             100, 100, 100, 100, 100,
               0,   0,   0,   0,   0,
            -100,-100,-100,-100,-100,
            -100,-100,-100,-100,-100,
        ]),
        Mask([
             100, 100, 100, 100, 100,
             100, 100, 100,  78, -32,
             100,  92,   0, -92,-100,
              32, -78,-100,-100,-100,
            -100,-100,-100,-100,-100,
        ]),
        Mask([
             100, 100, 100,  32,-100,
             100, 100,  92, -78,-100,
             100, 100,   0,-100,-100,
             100,  78, -92,-100,-100,
             100, -32,-100,-100,-100,
        ]),
        Mask([
            -100,-100,   0, 100, 100,
            -100,-100,   0, 100, 100,
            -100,-100,   0, 100, 100,
            -100,-100,   0, 100, 100,
            -100,-100,   0, 100, 100,
        ]),
        Mask([
            -100,  32, 100, 100, 100,
            -100, -78,  92, 100, 100,
            -100,-100,   0, 100, 100,
            -100,-100, -92,  78, 100,
            -100,-100,-100, -32, 100,
        ]),
        Mask([
             100, 100, 100, 100, 100,
             -32,  78, 100, 100, 100,
            -100, -92,   0,  92, 100,
            -100,-100,-100, -78,  32,
            -100,-100,-100,-100,-100,
        ]),
    ]


if __name__ == '__main__':
    img = Image.open('benchmarks/lena.bmp')
    RobertEdgeDetector(img).get_edge_mag(12).save('results/robert.bmp')
    PrewittEdgeDetector(img).get_edge_mag(24).save('results/prewitt.bmp')
    SobelEdgeDetector(img).get_edge_mag(38).save('results/sobel.bmp')
    FreiChenEdgeDetector(img).get_edge_mag(30).save('results/frei_chen.bmp')
    KirschEdgeDetector(img).get_edge_mag(135).save('results/kirsch.bmp')
    RobinsonEdgeDetector(img).get_edge_mag(43).save('results/robinson.bmp')
    NevatiaBabuEdgeDetector(img).get_edge_mag(12500).save('results/nevatia_babu.bmp')

