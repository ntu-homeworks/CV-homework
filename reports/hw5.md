Homework 5 - Grey Scale Morphology
=================================
R05944012 資訊網路與多媒體研究所 梁智湧

Source code are included in the folder `src`.

### Program Description
- Programming language: **Python 2.7.10**
- Used library: **Pillow 3.3.1** (Used to load/store image)
- Version control: **git**
- Benchmark: **lena.bmp** and **the octagon kernel (3-5-5-5-3, all zeros)**

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
(venv) $ python hw5.py
```

This program will finish all four tasks assigned in this homework and export result images to the folder `results`, including:
1. `grey_dilation.bmp`
2. `grey_erosion.bmp`
3. `grey_opening.bmp`
4. `grey_closing.bmp`

> Notice that due to the algorithm implemented, the execution of this program is time consuming. With some efforts on speedup, it probably takes *7~8 minutes* to complete all the tasks.

### Implementation Detail
#### Helpers (in addition to those implemented in previous assignments)
##### Coor (implemented in `heplers/image.py`)
`Coor` is a simple python class that extends `tuple`, with overloaded operators `+` and `-`, to help manipulate with coordinates of images.

##### Rect2D (implemented in `heplers/image.py`)
`Rect2D` is a simple python class that represents a rectangle in 2D space. Constructed with two diagonal 2D coordinates, it overloads the operator `in` to easily check if a given coordinate is contained in this rectangle. `Rect2D` is also iterable to traverse all the contained coordinates.

##### ImageFunction (implemented in `heplers/image.py`)
The common algorithm for *grey scale morphology* adopted in this program treats an image as a function. For example, map a 2D coordinate to an intensity value to represent a pixel. As a result, a python class `ImageFunction` is implemented as a helper for the computations of all grey scale morphology operators completed in this program.

As to represent an image, `ImageFunction` provides interfaces, `from_image` and `to_image`, to transform itself between an image. In addition, it is callable since it is a class acting as a function, and the domain of that function can be accessed through an iteratable attribute `domain`. The attribute `domain` is internally stored as a python `set` to meet the mathematical meaning of a set.

The following code demonstrates the constructions of `ImageFunction`s from the image of `lena.bmp` and the octagon kernel:
```python
# Construct the image of "lena".
img_func = ImageFunction.from_image(Image.open('benchmarks/lena.bmp'))

# Construct the octagon kernel (3-5-5-5-3 with all values as 0).
oct_kernel = ImageFunction(
    func=lambda (x, y): 0,
    domain=(
        Coor((x, y))
        for x in xrange(-2, 3) for y in xrange(-2, 3)
        if not(x in (-2, 2) and y in (-2, 2))
    )
)
```

#### Operators of Grey Scale Morphology
There is a class `GreyscaleMorphology` in this program extending from `BinaryMorphology` to wrap and provide all the required operators.

##### Dilation
```python
@classmethod
def dilation(cls, f, k):
    return ImageFunction(
        func=lambda x: max(
            [f(x - z) + k(z) for z in k.domain if x - z in f.domain]
        ),
        domain=(x_minus_z + z for z in k.domain for x_minus_z in f.domain)
    )
```
The implementation follows the algorithm provided in the course slide:
$$f:F \to E \text{ and } k:K \to E, \text{ then } f \oplus k: F \oplus K \to E \\
(f \oplus k)(x) = max\{f(x-z) + k(z) \mid z \in K, x-z \in F\}$$

The result of the operator **dilation** is also a function. Following the algorithm, the domain of the result function is defined as $\{x \mid z \in K, x-z \in F\}$, and the mapped value of the result function is defined as the **maximum** value of $f(x-z)+k(z)$ for any $x-z \in F$ and $z \in K$.

##### Erosion
```python
@classmethod
def erosion(cls, f, k):
    return ImageFunction(
        func=lambda x: max(0, min(
            [f(x + z) - k(z) for z in k.domain if x + z in f.domain]
        )),
        domain=(x_add_z - z for z in k.domain for x_add_z in f.domain)
    )
```
The implementation follows the algorithm provided in the course slide:
$$f:F \to E \text{ and } k:K \to E, \text{ then } f \ominus k: F \ominus K \to E \\
(f \ominus k)(x) = min\{f(x+z) - k(z) \mid z \in K, x+z \in F\}$$

The result of the operator **erosion** is also a function. Following the algorithm, the domain of the result function is defined as $\{x \mid z \in K, x+z \in F\}$, and the mapped value of the result function is defined as the minimum value of $f(x+z)-k(z)$ for any $x+z \in F$ and $z \in K$.

##### Opening and Closing
Extended from `BinaryMorphology`, `opening` and `closing` still perform `cls.dilation(cls.erosion(b, k), k)` and `cls.erosion(cls.dilation(b, k), k)`, respectively.

#### Speedup for Opening and Closing
The operations of *opening* and *closing* has an extremely high time complexity when the algorithm used to compute *dilation* and *erosion* in this program is adopted. This is because it recalculates many values that shall be filtered out while taking the maximum or minimum values of something.

To simplify the time complexity, a lookup-table method is utilized to speedup the execution. Implemented as a python class `ExtractedGreyscaleMorphology` extending from `GreyscaleMorphology`, it replaces each of the result functions of `dilation` and `erosion` with a lookup-table-based function. Although increasing the space complexity, this method can give the calculation a speedup more than 10x.

### Benchmark and Result Images

#### Original
![Original](https://i.imgur.com/gdJGRSk.png)

#### Grey Scale Dilation
![Grey scale dilation](https://i.imgur.com/XNXni6C.png)

#### Grey Scale Erosion
![Grey scale erosion](https://i.imgur.com/dnUieua.png)

#### Grey Scale Opening
![Grey scale opening](https://i.imgur.com/P3IMcAY.png)

#### Grey Scale Closing
![Grey scale closing](https://i.imgur.com/JlfebUX.png)
