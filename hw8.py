from hw5 import ExtractedGreyscaleMorphology as Morphology
from PIL import Image
from helpers.image import Pixels2D, ImageFunction, Coor
import random
import math

class NoiseMaker(object):

    def __init__(self, img):
        self.img = img

    def gen_gaussian_noise(self, amplitude):
        result = Image.new(self.img.mode, self.img.size)
        result.putdata(map(lambda p: p + amplitude * random.gauss(0, 1), self.img.getdata()))
        return result

    def gen_sap_noise(self, threshold):
        threshold /= 2

        def fn(p):
            uniform = random.uniform(0, 1)
            return 0 if uniform < threshold \
                else 255 if uniform > 1 - threshold \
                else p

        result = Image.new(self.img.mode, self.img.size)
        result.putdata(map(fn, self.img.getdata()))
        return result


class NoiseRemover(object):
    oct_kernel = ImageFunction(
        func=lambda (x, y): 0,
        domain=(
            Coor((x, y))
            for x in xrange(-2, 3) for y in xrange(-2, 3)
            if not(x in (-2, 2) and y in (-2, 2))
        )
    )

    def __init__(self, img):
        self.img = img
        self.pixels = Pixels2D(img)
        self.function = ImageFunction.from_image(img)

    box_filter = lambda self, size: self._process_box(size, lambda l: sum(l) / len(l))
    median_filter = lambda self, size: self._process_box(size, lambda l: sorted(l)[len(l) / 2])

    open_then_close = lambda self: Morphology.closing(
        Morphology.opening(self.function, self.oct_kernel),
        self.oct_kernel
    ).to_image('L', self.img.size)

    close_then_open = lambda self: Morphology.opening(
        Morphology.closing(self.function, self.oct_kernel),
        self.oct_kernel
    ).to_image('L', self.img.size)

    def _process_box(self, size, fn):
        if size[0] != size[1]:
            raise ValueError()
        size = size[0]

        result = Image.new(self.img.mode, self.img.size)
        result.putdata([
            fn(self._get_box((x, y), size))
            for y in xrange(self.img.height) for x in xrange(self.img.width)
        ])
        return result

    def _get_box(self, coor, size):
        rng = range(- size / 2, size / 2 + 1)
        
        return map(self.pixels.__getitem__, filter(lambda (x, y): 0 <= x < self.img.width and 0 <= y < self.img.height, [
            (coor[0] + x, coor[1] + y)
            for x in rng for y in rng
        ]))


def snr(simg, nimg):
    spixels, npixels = [img.getdata() for img in (simg, nimg)]
    nn = float(len(spixels))

    smu = sum(spixels) / nn
    nmu = sum(n - s for s, n in zip(spixels, npixels)) / nn
    vs = sum((s - smu) ** 2 for s in spixels) / nn
    vn = sum((n - s - nmu) ** 2 for s, n in zip(spixels, npixels)) / nn
    return 20 * math.log10(math.sqrt(vs) / math.sqrt(vn))

if __name__ == '__main__':
    # Read benchmark "lena"
    img = NoiseMaker(Image.open('benchmarks/lena.bmp'))

    # Make noise on benchmarks
    noises = {}
    noises['gauss10'], noises['gauss30'] = [NoiseRemover(img.gen_gaussian_noise(amplitude)) for amplitude in (10, 30)]
    noises['sap005'], noises['sap01'] = [NoiseRemover(img.gen_sap_noise(threshold)) for threshold in (0.05, 0.1)]

    # Perform cleaning
    results = {
        name: {
            'box33': noise.box_filter((3, 3)), 'box55': noise.box_filter((5, 5)),
            'median33': noise.median_filter((3, 3)), 'median55': noise.median_filter((5, 5)),
            'open_close': noise.open_then_close(), 'close_open': noise.close_then_open()
        }
        for name, noise in noises.iteritems()
    }

    # Store noise pictures (4 pictures)
    map(lambda (k, v): v.img.save("results/%s/noise.bmp" % k), noises.iteritems())

    # Store results (24 pictures)
    map(lambda (name, result): result.save(name), [
        ("results/%s/%s.bmp" % (name, fltr), result)
        for name, noise in results.iteritems()
        for fltr, result in noise.iteritems()
    ])

    # Calculate SNR of processed images and noise images
    SNRs = {
        "%s/%s" % (name, fltr): snr(img.img, result)
        for name, noise in results.iteritems()
        for fltr, result in noise.iteritems()
    }
    SNRs.update({
        "%s" % name: snr(img.img, noise.img)
        for name, noise in noises.iteritems()
    })
    print SNRs

