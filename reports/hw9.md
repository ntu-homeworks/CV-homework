Homework 9: General Edge Detection
==============================
網媒所 R05944012 梁智湧
Source code are included in the folder `src`.

### Program Description
- Programming language: **Python 2.7.10**
- Used library: **Pillow 3.3.1** (Used to load/store image)
- Version control: **git**
- Benchmark: **lena.bmp**.

### Usage
The benchmark image is already included in the source folder (`benchmarks/lena.bmp`). Running this program requires **Python** along with its library **Pillow**. The following commands are to install required libraries in virtual environment and execute the program, providing that **Python 2.7** and **virtualenv** are already installed.

```bash
$ # On linux
$ # Install Pillow in the virtualenv
$ cd src
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ 
(venv) $ # Run the program
(venv) $ python hw9.py
```

This program will finish all tasks assigned in this homework and export the result to the folder `results`, including:

1. `robert.bmp`
2. `prewitt.bmp`
3. `sobel.bmp`
4. `frei_chen.bmp`
5. `kirsch.bmp`
6. `robinsom.bmp`
7. `nevatia_babu.bmp`

Notice that this program takes about 10 minutes to finish all the tasks.

### Implementation Detail
#### To Expend the Image
A wrapper for `Pixels2D` (please refer my previous reports) is implemented to modify the index argument when fetching a pixel data. It changes the index to the closest bound when the index is out of bound.
```python
class ExpendedPixels2D(Pixels2D):
    def _get_index(self, xy):
        if isinstance(xy, tuple) and len(xy) == 2:
            xy = tuple(map(lambda (c, s): 0 if c < 0 else s - 1 if c >= s else c, zip(xy, self.size)))
        return super(ExpendedPixels2D, self)._get_index(xy)
```

#### To Represent a Sub-region of an Image
The class `PixelRegion` is implemented to contain a region of image data. For example, `PixelRegion(pixels, coor=(5, 10), size=3)` gets a $3\times3$ region around $(5, 10)$ from `pixels`.
```python
class PixelRegion(object):
    def __init__(self, pixels, coor, size):
        self.size = size
        self.data = [pixels[tuple(map(lambda c, o: c + o - self.origin, coor, (x, y)))] for y in xrange(size) for x in xrange(size)]

    origin = property(lambda self: (self.size - 1) / 2)
```

#### To Represent a Mask
The class `Mask` is implemented to contain a mask of automatically determined size. Its operator `*` has been overloaded to perform convolution.
```python
class Mask(object):
    def __init__(self, data):
        self.size = int(len(data) ** 0.5)
        self.data = data

    def __rmul__(self, other):
        if isinstance(other, PixelRegion) and self.size == other.size:
            return sum(l * r for l, r in zip(self.data, other.data))
        return NotImplemented
```

#### Generalized Gradient Edge Detector
This abstract class computes edge magnitude with masks and operators defined in its derived class. It can return an image containing such information through its method `get_edge_mag`.
```python
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
```

#### Operator to Calculate Sum of Square
All of **Robert**'s, **Prewitt**'s, **Sobel**'s, and **Frei & Chen**'s edge detectors calculate sum of square as the result of each pixel. The following abstract class (derived from `GradientEdgeDetector`) helps this:
```python
class SOSGradientEdgeDetector(GradientEdgeDetector):
    get_magnitude = lambda self, *args: sum(self.r(i, *args) ** 2 for i in range(2)) ** 0.5
```

#### Operator to Retrieve Maximum Value
All of **Kirsch**'s, **Robinson**'s, and **Nevatia Babu**'s edge detectors take the maximum of all convolution results as the result of each pixel. The following class helps this:
```python
class MaxGradientEdgeDetector(GradientEdgeDetector):
    get_magnitude = lambda self, *args: max(self.r(i, *args) for i in range(len(self.masks)))
```

#### Detail of each Edge Detectors
Each detector has their own masks to perform convolution calculation with. Some of them even have slidely different method to process the result. These are specified in their own derived classes.
##### Robert's Edge Detector
```python
class RobertEdgeDetector(SOSGradientEdgeDetector):
    masks = [
        Mask([-1, 0,
               0, 1,]),
        Mask([ 0,-1,
               1, 0,]),
    ]
```

##### Prewitt's Edge Detector
```python
class PrewittEdgeDetector(SOSGradientEdgeDetector):
    masks = [
        Mask([-1,-1,-1,
               0, 0, 0,
               1, 1, 1,]),
        Mask([-1, 0, 1,
              -1, 0, 1,
              -1, 0, 1,]),
    ]
```

##### Sobel's Edge Detector
```python
class SobelEdgeDetector(SOSGradientEdgeDetector):
    masks = [
        Mask([-1,-2,-1,
               0, 0, 0,
               1, 2, 1,]),
        Mask([-1, 0, 1,
              -2, 0, 2,
              -1, 0, 1,]),
    ]
```

##### Frei & Chen's Edge Detector
```python
class FreiChenEdgeDetector(SOSGradientEdgeDetector):
    masks = [
        Mask([-1,-2**0.5,-1,
               0,      0, 0,
               1, 2**0.5, 1,]),
        Mask([-1,      0, 1,
              -2**0.5, 0, 2**0.5,
              -1,      0, 1,])
    ]
```

##### Kirsch's Edge Detector
```python
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
```

##### Robinson's Edge Detector
Because half of its results can be reused in some way, the method `r` is override for a better performance.
```python
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
```

##### Nevatia Babu's Edge Detector
```python
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
```

#### The `main` Function to Call These Utilities and Set Thresholds
```python
if __name__ == '__main__':
    img = Image.open('benchmarks/lena.bmp')
    RobertEdgeDetector(img).get_edge_mag(12).save('results/robert.bmp')
    PrewittEdgeDetector(img).get_edge_mag(24).save('results/prewitt.bmp')
    SobelEdgeDetector(img).get_edge_mag(38).save('results/sobel.bmp')
    FreiChenEdgeDetector(img).get_edge_mag(30).save('results/frei_chen.bmp')
    KirschEdgeDetector(img).get_edge_mag(135).save('results/kirsch.bmp')
    RobinsonEdgeDetector(img).get_edge_mag(43).save('results/robinson.bmp')
    NevatiaBabuEdgeDetector(img).get_edge_mag(12500).save('results/nevatia_babu.bmp')
```

### Results
#### Robert's Edge Detector (Threshold: 12)
![Robert's Edge Detector](https://i.imgur.com/pqaoj6f.png)

#### Prewitt's Edge Detector (Threshold: 24)
![Prewitt's Edge Detector](https://i.imgur.com/Ldh71dE.png)

#### Sobel's Edge Detector (Threshold: 38)
![Sobel's Edge Detector](https://i.imgur.com/bPTpQSw.png)

#### Frei & Chen's Edge Detector (Threshold: 30)
![Frei & Chen's Edge Detector](https://i.imgur.com/Tf11wnk.png)

#### Kirsch's Edge Detector (Threshold: 135)
![Kirsch's Edge Detector](https://i.imgur.com/p7t7WIw.png)

#### Robinson's Edge Detector (Threshold: 43)
![Robinson's Edge Detector](https://i.imgur.com/mvgP4Y9.png)

#### Nevatia Babu's Edge Detector (Threshold: 12500)
![Nevatia Babu's Edge Detector](https://i.imgur.com/kopLJC6.png)


