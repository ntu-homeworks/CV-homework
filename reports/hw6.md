Homework 6 - Yokoi Connectivity Number
==================================
R05944012 資訊網路與多媒體研究所 梁智湧

Source code are included in the folder `src`.

### Program Description
- Programming language: **Python 2.7.10**
- Used library: **Pillow 3.3.1** (Used to load/store image)
- Version control: **git**
- Benchmark: **downsampled lena.bmp** with size `64 * 64`.

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
(venv) $ python hw6.py
```

This program will finish all tasks assigned in this homework and export the result to the folder `results`, including:
1. `yokoi.txt`

### Implementation Detail
#### Utility: Downsampling
```python
def downsampling(img, size):
    width, height = size
    ratio_x, ratio_y = img.width / width, img.height / height
    pixels = Pixels2D(img)

    result = Image.new(img.mode, size)
    result.putdata([pixels[x * ratio_x, y * ratio_y] for y in xrange(height)
                                                     for x in xrange(width)])
    return result
```
This utility downsample the image given in the parameters `img` to the size `size` which is also passed in the parameters. Following the homework specifications, the left-top-most one is chosen as the sample pixel.

#### Yokoi Connectivity Number
```python
class YokoiConnNumber(object):
    def __new__(cls, img):
        return [
            str(cls._f(img, (x, y))) if img.getpixel((x, y)) != 0 else ' '
            for y in xrange(img.height) for x in xrange(img.width)
        ]
```
Although `YoloiConnNumber` is actually a python class, it has the same usage of a python function. For example, user may get the processed result (Yokoi connectivity number) in this way:
```python
img = thresholding(Image.open('lena.bmp'), 128)
yokoi = YokoiConnNumber(img)
```

The algorithm designed here is actually the one mentioned in the course slides, where `cls._f`, described below, has the same semantic with $f$. All the 1's pixel are mapped with `cls._f` and each get a numeric symbol in `0~5` as result. On the other hand, each of the other pixels, i.e. the 0's pixels, is mapped to a single space ` `.

##### $f$
```python
@classmethod
def _f(cls, img, (center_x, center_y)):
    pixels = Pixels2D(img)

    x = map(lambda (_x, _y): pixels[_x, _y] 
                             if 0 <= _x < img.width and 0 <= _y < img.height else 0,
            map(lambda (_x, _y): (center_x + _x, center_y + _y), [
                (0, 0), (1, 0), (0, -1), (-1, 0), (0, 1),
                (1, 1), (1, -1), (-1, -1), (-1, 1),
            ])
        )

    a = map(cls._h, [
            (x[0], x[1], x[6], x[2]),
            (x[0], x[2], x[7], x[3]),
            (x[0], x[3], x[8], x[4]),
            (x[0], x[4], x[5], x[1]),
        ])

    return 5 if all(ai == 'r' for ai in a) else a.count('q')
```
The last line of code of this class method implements $f$:
$$f(a_1, a_2, a_3, a_4) = \begin{cases}5 & \text{ if }a_1=a_2=a_3=a_4=r \\
n & \text{ where } n = \#\{a_k\mid a_k=q\}, \text{ otherwise}\end{cases}$$

This method is actually a little more complicated than implementing only $f$. It first try to retrieve all the values in the symbolic domain $x_i \text{ for } i \in [0,8]$ and stores them in the list `x`. After that, it calculates the values $a_1$, $a_2$, $a_3$, and $a_4$, which are also mentioned in the course slides, with the method `cls._h` and stores these four results in the list `a`. Finally, it can achieve the original purpose of $f$ and determine the return value. The method `cls._h` has the semantic of $h$, which is mentioned in the course slides, and is described below.

##### $h$
```python
@classmethod
def _h(cls, (b, c, d, e)):
    if b != c:
        return 's'
    if b == c == d == e:
        return 'r'
    return 'q'
```
The implementation of `cls._h` totally follows the definition of $h$:
$$h(b,c,d,e)=\begin{cases}q & \text{ if }b=c\text{ and }(d\neq b \text{ or } e \neq b) \\
r & \text{ if }b=c\text{ and }(d=b \text{ and } e=b) \\
s & \text{ if }b \neq c\end{cases}$$

#### Export the result to file
The result of Yokoi connectivity number of the benchmark `lena.bmp` can be retrieved, with the help of the class `YokoiConnNumber`, in this way (implemented in `main`):
```python
img = Image.open('benchmarks/lena.bmp')
bin_img = thresholding(img, 128)
small_img = downsampling(bin_img, (64, 64))

yokoi = YokoiConnNumber(small_img)
```
`yokoi` in previous code fragment stores the result. The following code layouts and writes the result to an output file, preserving the original look of the benchmark:
```python
with open('results/yokoi.txt', 'w') as f:
    f.write(
        '\n'.join(
            ''.join(yokoi[i : i + small_img.width])
            for i in xrange(0, len(yokoi), small_img.width)
        )
    )
```

### Benchmark and Result
The benchmark is the downsampled `lena.bmp` with width and height both 64 pixels.

![The downsampled benchmark](https://i.imgur.com/D2N7rs2.png)

The result is included in next page. Notice that the result is slightly different with the reference answer attached in the course slides because **that provided answer discards all isolated pixels** (which should be values of `0`s) and shows only spaces on such pixels instead. As the concern of the correctness of the result, I personally recommend that the content of the course slides shall have a revise.
