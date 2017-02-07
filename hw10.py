from hw9 import GradientEdgeDetector, Mask
from PIL import Image

class ZeroCrossingEdgeDetector(GradientEdgeDetector):
    get_magnitude = lambda self, *args: self.r(0, *args)
    def get_direction(self, *args): raise NotImplementedError


class Laplacian1(ZeroCrossingEdgeDetector):
    masks = [
        Mask([0, 1, 0,
              1,-4, 1,
              0, 1, 0,]),
    ]

class Laplacian2(ZeroCrossingEdgeDetector):
    masks = [
        Mask([1, 1, 1,
              1,-8, 1,
              1, 1, 1,]),
    ]

    get_edge_mag = lambda self, threshold: super(Laplacian2, self).get_edge_mag(threshold * 3)

class MinVarLaplacian(ZeroCrossingEdgeDetector):
    masks = [
        Mask([ 2,-1, 2,
              -1,-4,-1,
               2,-1, 2,]),
    ]

    get_edge_mag = lambda self, threshold: super(MinVarLaplacian, self).get_edge_mag(threshold * 3)

class LapOfGaussian(ZeroCrossingEdgeDetector):
    masks = [
        Mask([  0,  0,  0, -1, -1, -2, -1, -1,  0,  0,  0,
                0,  0, -2, -4, -8, -9, -8, -4, -2,  0,  0,
                0, -2, -7,-15,-22,-23,-22,-15, -7, -2,  0,
               -1, -4,-15,-24,-14, -1,-14,-24,-15, -4, -1,
               -1, -8,-22,-14, 52,103, 52,-14,-22, -8, -1,
               -2, -9,-23, -1,103,178,103, -1,-23, -9, -2,
               -1, -8,-22,-14, 52,103, 52,-14,-22, -8, -1,
               -1, -4,-15,-24,-14, -1,-14,-24,-15, -4, -1,
                0, -2, -7,-15,-22,-23,-22,-15, -7, -2,  0,
                0,  0, -2, -4, -8, -9, -8, -4, -2,  0,  0,
                0,  0,  0, -1, -1, -2, -1, -1,  0,  0,  0,]),
    ]

class DiffOfGaussian(ZeroCrossingEdgeDetector):
    masks = [
        Mask([ -1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1,
               -3, -5, -8,-11,-13,-13,-13,-11, -8, -5, -3,
               -4, -8,-12,-16,-17,-17,-17,-16,-12, -8, -4,
               -6,-11,-16,-16,  0, 15,  0,-16,-16,-11, -6,
               -7,-13,-17,  0, 85,160, 85,  0,-17,-13, -7,
               -8,-13,-17, 15,160,283,160, 15,-17,-13, -8,
               -7,-13,-17,  0, 85,160, 85,  0,-17,-13, -7,
               -6,-11,-16,-16,  0, 15,  0,-16,-16,-11, -6,
               -4, -8,-12,-16,-17,-17,-17,-16,-12, -8, -4,
               -3, -5, -8,-11,-13,-13,-13,-11, -8, -5, -3,
               -1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1,]),
    ]

    def get_edge_mag(self, threshold):
        result = super(DiffOfGaussian, self).get_edge_mag(threshold)
        result.putdata(map(lambda p: int(not p), result.getdata()))
        return result


if __name__ == '__main__':
    img = Image.open('benchmarks/lena.bmp')

    Laplacian1(img).get_edge_mag(15).save('results/laplacian1.bmp')
    Laplacian2(img).get_edge_mag(15).save('results/laplacian2.bmp')
    MinVarLaplacian(img).get_edge_mag(20).save('results/min_var_laplacian.bmp')
    LapOfGaussian(img).get_edge_mag(3000).save('results/laplace_of_gaussian.bmp')
    DiffOfGaussian(img).get_edge_mag(1).save('results/diff_of_gaussian.bmp')
