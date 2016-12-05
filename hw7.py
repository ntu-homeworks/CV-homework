from hw6 import SymbolicOperator, downsampling
from helpers.image import Pixels2D
from PIL import Image

class InteriorBorder(SymbolicOperator, Pixels2D):
    connectivity = 8

    def __init__(self, *args, **kwargs):
        super(InteriorBorder, self).__init__(*args, **kwargs)

        if not hasattr(self, "size"):
            raise ValueError("`size` is required to initialize `%s`." % self.__class__)

        self.data = [
            0 if self[x, y] == 0
            else 'i' if all(X == 1 for X in self._x(self, self.size, (x, y))[0:self.connectivity])
            else 'b'
            for y in xrange(self.size[1]) for x in xrange(self.size[0])
        ]


class PairRelationship(SymbolicOperator, Pixels2D):
    connectivity = 8
    l = 'b'
    m = 'i'
    theta = 1

    def __init__(self, *args, **kwargs):
        super(SymbolicOperator, self).__init__(*args, **kwargs)

        if not hasattr(self, "size"):
            raise ValueError("`size` is required to initialize `%s`." % self.__class__)

        h = lambda a, m: 1 if a == m else 0
        self.data = [
            'p' if sum(h(X, self.m) for X in self._x(self, self.size, (x, y)))
                >= self.theta and self[x, y] == self.l
            else 'q'
            for y in xrange(self.size[1]) for x in xrange(self.size[0])
        ]


class ConnectedShrink(SymbolicOperator):
    connectivity = 8

    @classmethod
    def _f(cls, a, x0):
        return 0 if a.count(1) == 1 else x0

    @classmethod
    def _a(cls, x):
        return map(cls._h, (
            (x[0], x[1], x[6], x[2]),
            (x[0], x[2], x[7], x[3]),
            (x[0], x[3], x[8], x[4]),
            (x[0], x[4], x[5], x[1]),
        ))

    @classmethod
    def _h(cls, (b, c, d, e)):
        if cls.connectivity == 4:
            return 1 if b == c and (b != d or b != e) else 0
        if cls.connectivity == 8:
            return 1 if b != c and (b == d or b == e) else 0


class Thinning(ConnectedShrink, Pixels2D):
    
    def __init__(self, original_img, marked_img):
        width, height = original_img.size
        self.size = original_img.size
        self.data = list(original_img.data)

        for y in xrange(height):
            for x in xrange(width):
                X = self._x(self, self.size, (x, y))
                a = self._a(X)

                if self._f(a, self[x, y]) == 0 and marked_img[x, y] == 'p':
                    self[x, y] = 0

