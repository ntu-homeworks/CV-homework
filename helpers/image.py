from PIL.Image import Image

class Pixels2D(object):
    
    def __init__(self, pixels_or_image, width=None, size=None):
        if isinstance(pixels_or_image, Image):
            self.data = list(pixels_or_image.getdata())
            self.width = pixels_or_image.width
        elif hasattr(pixels_or_image, '__getitem__'):
            if width == size == None:
                raise ValueError("Specify 'width' or 'size' in arguments.")

            self.data = list(pixels_or_image)
            self.width = width if width != None else size[0]
        else:
            raise ValueError("Pass 1D pixels list or image in argument 'pixels_or_image'.")

    
    def _get_index(self, xy):
        if isinstance(xy, int):
            return xy
        if isinstance(xy, tuple) and len(xy) == 2:
            x, y = xy
            return y * self.width + x
        raise IndexError()

    __getitem__ = lambda self, xy: self.data.__getitem__(self._get_index(xy))
    __setitem__ = lambda self, xy, value: self.data.__setitem__(self._get_index(xy), value)

