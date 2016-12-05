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


