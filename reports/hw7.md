Homework 7 - Thinning
===================
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
(venv) $ python hw7.py
```

This program will finish all tasks assigned in this homework and export the result to the folder `results`, including:
1. `small_thinning.bmp`

### Implementation Detail
#### Abstract Class for Symbolic Operators
```python
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
```
This abstract class provides a method, `_x`, to return the values in a symbolic domain to benefit its sub-classes (`InteriorBorder`, `PairRelationship`, and `ConnectedShrink`) for more simple coding complexity. More specifically, it internally checks if a coordinate in the domain is out of the bound of the pixel and return value `0` for that pixel on such situation. The returned symbolic domain contains nine elements as the usual convention described in the course slide. The following illustrates the pixel each element represents to:
 $x_7$ | $x_2$ | $x_6$
:-----:|:-----:|:-----:
 $x_3$ | $x_0$ | $x_1$
 $x_8$ | $x_4$ | $x_5$

#### Labeling Interior/Border Pixels
```python
class InteriorBorder(SymbolicOperator, Pixels2D):
    connectivity = 8

    def __init__(self, pixels, size):
        self.data = pixels.data
        self.size = size
        self.width = size[0]

        self.data = [
            0 if self[x, y] == 0
            else 'i' if all(X == 1 for X in self._x(self, self.size, (x, y))[0:self.connectivity])
            else 'b'
            for y in xrange(self.size[1]) for x in xrange(self.size[0])
        ]
```
This operator class extends `SymbolicOperator` so it can access the symbolic domain of any pixel easily. It also extends `Pixels2D` which makes it available to be accessed through a 2-dimension coordinate specification; for example, `p[2, 5]` accesses the pixel on the third column of sixth row. The thing is same for other operators also extending `SymbolicOperator` or `Pixels2D`.

This class labels non-zero pixels to **border** pixels and **interior** pixels. Interior pixels are recognized if all elements in its symbolic domain are 1-pixels, while border pixels are other 1-pixels not recognized as interior pixels.

#### Pair Relationship
```python
class PairRelationship(SymbolicOperator, Pixels2D):
    connectivity = 8
    l = 'b'
    m = 'i'
    theta = 1

    def __init__(self, pixels, size):
        self.data = pixels.data
        self.size = size
        self.width = size[0]

        h = lambda a, m: 1 if a == m else 0
        self.data = [
            'p' if sum(h(X, self.m) for X in self._x(self, self.size, (x, y)))
                >= self.theta and self[x, y] == self.l
            else 'q'
            for y in xrange(self.size[1]) for x in xrange(self.size[0])
        ]
```
This is the class to mark if a border pixel has any interior pixel as neighborhood. The algorithm applied here **(8-connected)** is simply the on described in the course slide, as following:
$$
h(a,m)=\begin{cases}1 & \text{ if }a=m \\
0 & \text{ otherwise } \end{cases} \\
out = \begin{cases} q & \text{ if } \sum_{n=1}^8 h(x_n, m) < \theta \ \vee x_0 \neq l \\
p & \text{ if } \sum_{n=1}^8 h(x_n, m) \ge \theta \ \vee x_0 = l \end{cases}
$$

#### Connected Shrink
```python
class ConnectedShrink(SymbolicOperator):
    connectivity = 4

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
```
This class provides functions to help judge if an 1-pixel shall be remove into 0-pixel. It does not provides a straightaway interface to call with since this is not feasible in this application; i.e., this program requires connected shrink to be computed with other operators in each iteration. However, it still provides important methods ($h$, $a$, and $f$), mentioned in the course slide (for **4-connectivity**, that are helpful in each iteration:
$$
h(b,c,d,e)=\begin{cases} 1 & \text{ if }b=c \wedge(b\neq d \vee b \neq e) \\
0 & \text{ otherwise} \end{cases}
$$
$$
a_1=h(x_0,x_1,x_6,x_2) \\
a_2=h(x_0,x_2,x_7,x_3) \\
a_3=h(x_0,x_3,x_8,x_4) \\
a_4=h(x_0,x_4,x_5,x_1)
$$
$$
output=f(a_1,a_2,a_3,a_4,x_0)=\begin{cases}g & \text{ if exactly one of }a_1,a_2,a_3,a_4=1 \\
x_0 & \text{ otherwise} \end{cases}
$$

#### Thinning
```python
class Thinning(ConnectedShrink, Pixels2D):

    def __init__(self, original_img, marked_img, size):
        self.width, height = size
        self.size = size
        self.data = list(original_img.data)

        for y in xrange(height):
            for x in xrange(self.width):
                X = self._x(self, self.size, (x, y))
                a = self._a(X)

                if self._f(a, self[x, y]) == 0 and marked_img[x, y] == 'p':
                    self[x, y] = 0
```
This initializer of this class can perform one iteration of thinning operation. It requires results of previous classes as input arguments: one is original image, the other is marked image. It utilizes the helpers provided by `ConnectedShrink`, as mentioned above, to complete its jobs.

##### The auto repeater
```python
	@classmethod
    def repeat(cls, img, times):
        do = lambda x: cls(x, PairRelationship(InteriorBorder(x, img.size), img.size), img.size)

        prev = Pixels2D(img, size=img.size)
        result = do(prev)

        while prev.data != result.data and times > 0:
            result, prev = do(result), result
            times -= 1

        ret = Image.new(img.mode, img.size)
        ret.putdata(result.data)
        return ret
```
This utility helps the user to repeatedly perform thinning operation. The parameter `arg` is the operand image, and `times` is the maximum iteration count. However, it automatically stops when the results are identical for two consequent operations, so setting `times` an infinity number (`float('inf')`) makes it work until the thinning reaches the end. As reader can see in the code, it utilizes APIs (classes) designed in this assignment and feeds their results to `thinning`. This program is fully modulized and has a good maintainability.

### Result
![Result](https://i.imgur.com/uIvSr3t.png)

The original result image generated by this program is also attached in `results/`. Please refer to it if you want to look for more detail.
