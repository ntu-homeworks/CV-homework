Homework 8: Noise Removal
========================
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
(venv) $ python hw8.py
```

This program will finish all tasks assigned in this homework and export the result to the folder `results`, including:
```
gauss10
├── box33.bmp
├── box55.bmp
├── close_open.bmp
├── median33.bmp
├── median55.bmp
├── noise.bmp
└── open_close.bmp
gauss30
├── box33.bmp
├── box55.bmp
├── close_open.bmp
├── median33.bmp
├── median55.bmp
├── noise.bmp
└── open_close.bmp
sap005
├── box33.bmp
├── box55.bmp
├── close_open.bmp
├── median33.bmp
├── median55.bmp
├── noise.bmp
└── open_close.bmp
sap01
├── box33.bmp
├── box55.bmp
├── close_open.bmp
├── median33.bmp
├── median55.bmp
├── noise.bmp
└── open_close.bmp
```

### Implementation Detail
#### Noise Generation
The program follows the definition described in the course slide to generate **Gaussian noise** and **salt-and-peppers noise**. The *Gaussian random number* and *uniform random number* are generated with built-in python library `random`.

##### Gassian noise
```python
def gen_gaussian_noise(self, amplitude):
    result = Image.new(self.img.mode, self.img.size)
    result.putdata(map(lambda p: p + amplitude * random.gauss(0, 1), self.img.getdata()))
    return result
```

##### SAP noise
```python
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
```

#### Block Generation and Processing (used in box and median filters)
The following shared code are used in box filter and median filter to generate blocks and to process them. The processing unit use the parameter `fn` to process a block.
```python
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
```

#### Box Filter
The box filter has `_procsss_box` to get the mean of a block.
```python
box_filter = lambda self, size: self._process_box(size, lambda l: sum(l) / len(l))
```

#### Median Filter
The median filter has `_process_box` to get the median of a block.
```python
median_filter = lambda self, size: self._process_box(size, lambda l: sorted(l)[len(l) / 2])
```

#### Opening-then-Closing Filter
This filter use opening and closing operations implemented in homework 5.
```python
open_then_close = lambda self: Morphology.closing(
    Morphology.opening(self.function, self.oct_kernel),
    self.oct_kernel
).to_image('L', self.img.size)
```

#### Closing-then-Opening Filter
This filter use opening and closing operations implemented in homework 5.
```python
close_then_open = lambda self: Morphology.opening(
    Morphology.closing(self.function, self.oct_kernel),
    self.oct_kernel
).to_image('L', self.img.size)
```

#### SNR Calculation
This method just follows the definition on the course slide.
```python
def snr(simg, nimg):
    spixels, npixels = [img.getdata() for img in (simg, nimg)]
    nn = float(len(spixels))

    smu = sum(spixels) / nn
    nmu = sum(n - s for s, n in zip(spixels, npixels)) / nn
    vs = sum((s - smu) ** 2 for s in spixels) / nn
    vn = sum((n - s - nmu) ** 2 for s, n in zip(spixels, npixels)) / nn
    return 20 * math.log10(math.sqrt(vs) / math.sqrt(vn))
```

### Result
> Caution: This program takes about 33 minutes to finish all computations.

#### SNR
The following is the calculated SNR values compared to original benchmark `lena.bmp` output by the program. It has been formatted for a better readability.
```python
{
    'gauss10': 13.606930153797007,
    'gauss10/box33': 14.791773651914863,
    'gauss10/box55': 13.224675045258463,
    'gauss10/median33': 14.723002763456217,
    'gauss10/median55': 13.892983639592805,
    'gauss10/open_close': 13.238485397319064,
    'gauss10/close_open': 13.529692275938391,
    'gauss30': 4.165384375992301,
    'gauss30/box33': 12.600971934375176,
    'gauss30/box55': 12.384238529730787,
    'gauss30/median33': 11.668692327761882,
    'gauss30/median55': 12.283238509640757,
    'gauss30/open_close': 11.005082030592352,
    'gauss30/close_open': 11.026694940209993,
    'sap005': 3.917967472141466,
    'sap005/box33': 12.279678062214325,
    'sap005/box55': 12.085745664619019,
    'sap005/median33': 15.14561942367486,
    'sap005/median55': 14.064235354102681,
    'sap005/open_close': 11.526444035513217,
    'sap005/close_open': 11.574135196119194,
    'sap01': 0.8940125399861107,
    'sap01/box33': 10.335900705845134,
    'sap01/box55': 10.836278864456204,
    'sap01/median33': 14.980419776119088,
    'sap01/median55': 13.948186795543535,
    'sap01/open_close': 5.64812341056037,
    'sap01/close_open': 5.562129193990874,
}
```

#### Tests with Gaussian Noise at Amplitude *10*
##### The noise image
![gauss10/](https://i.imgur.com/KkGSfjN.png)
##### With $3\times3$ box filter
![gauss10/box33](https://i.imgur.com/vwurEDw.png)
##### With $5\times5$ box filter
![gauss10/box55](https://i.imgur.com/Z0elqhF.png)
##### With $3\times3$ median filter
![gauss10/median33](https://i.imgur.com/IKvixlQ.png)
##### With $5\times5$ median filter
![gauss10/median55](https://i.imgur.com/SJpMN7R.png)
##### With opening-then-closing filter
![gauss10/open_close](https://i.imgur.com/9URvcVJ.png)
##### With closing-then-opening filter
![gauss10/close_open](https://i.imgur.com/7swdJkr.png)

#### Tests with Gaussian Noise at Amplitude *30*
##### The noise image
![gauss30/](https://i.imgur.com/FnGl72H.png)
##### With $3\times3$ box filter
![gauss30/box33](https://i.imgur.com/wicLZ5f.png)
##### With $5\times5$ box filter
![gauss30/box55](https://i.imgur.com/fI3YyWt.png)
##### With $3\times3$ median filter
![gauss30/median33](https://i.imgur.com/dXhriSD.png)
##### With $5\times5$ median filter
![gauss30/median55](https://i.imgur.com/MTi1QtZ.png)
##### With opening-then-closing filter
![gauss30/open_close](https://i.imgur.com/inFFGLH.png)
##### With closing-then-opening filter
![gauss30/close_open](https://i.imgur.com/FRtVip7.png)

#### Tests with Salt-and-Pepper Noise at Threshold *0.05*
##### The noise image
![sap005/](https://i.imgur.com/Pi66LHo.png)
##### With $3\times3$ box filter
![sap005/box33](https://i.imgur.com/AwR3e6P.png)
##### With $5\times5$ box filter
![sap005/box55](https://i.imgur.com/3gj82w0.png)
##### With $3\times3$ median filter
![sap005/median33](https://i.imgur.com/eTMtsTQ.png)
##### With $5\times5$ median filter
![sap005/median55](https://i.imgur.com/lulNrVS.png)
##### With opening-then-closing filter
![sap005/open_close](https://i.imgur.com/KX6k40u.png)
##### With closing-then-opening filter
![sap005/close_open](https://i.imgur.com/spNctVB.png)

#### Tests with Salt-and-Pepper Noise at Threshold *0.1*
##### The noise image
![sap01/](https://i.imgur.com/SaSQdcS.png)
##### With $3\times3$ box filter
![sap01/box33](https://i.imgur.com/2991STe.png)
##### With $5\times5$ box filter
![sap01/box55](https://i.imgur.com/mdYQFYk.png)
##### With $3\times3$ median filter
![sap01/median33](https://i.imgur.com/zbE7cdY.png)
##### With $5\times5$ median filter
![sap01/median55](https://i.imgur.com/K5g5yHJ.png)
##### With opening-then-closing filter
![sap01/open_close](https://i.imgur.com/Tn1KBUy.png)
##### With closing-then-opening filter
![sap01/close_open](https://i.imgur.com/3whQREA.png)
