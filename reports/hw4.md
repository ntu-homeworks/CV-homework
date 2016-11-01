Homework 4 - Binary Morphology
=================================
R05944012 資訊網路與多媒體研究所 梁智湧

Source code are included in the folder `src`.

### Program Description
- Programming language: **Python 2.7.10**
- Used library: **Pillow 3.3.1** (Used to load/store image)
- Version control: **git**
- Benchmark: **lena.bmp**

### Usage
The benchmark image is already included in the source folder (`benchmarks/lena.bmp`). Running this program requires **Python** along with its library **Pillow**. The following commands are to install required libraries in virtual environment and execute the program, providing that **Python 2.7** and **virtualenv** are already installed.

```bash
$ # On linux
$ # Install Pillow in the virtualenv
$ cd src
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ 
$ # Run the program
$ python hw4.py
```

This program will finish all three tasks assigned in this homework and export result images to the folder `results`, including:
1. `dilation.bmp`
2. `erosion.bmp`
3. `opening.bmp`
4. `closing.bmp`
5. `hit_and_miss.bmp`

### Implementation Detail
#### PixelSet
`PixelSet` is a newly implemented helper to present the concept of the "set". It extends python's `set` and stores coordinates of some pixels. It is designed for easy transformation between a image (or pixels) and `PixelSet`.

#### Dilation
```python
def dilation(a, b):
    width, height = a.size
    result = PixelSet(filter(lambda (x, y): 0 <= x < width and 0 <= y < height,
				    [(ax + bx, ay + by) for (ax, ay) in a for (bx, by) in b]))
    result.size, result.origin = a.size, a.origin
    return result
```
`a` and `b` are both `PixelSet`s. The algorithm follows the steps provided in the course slide.

#### Erosion
```python
def erosion(a, b):
    width, height = a.size
    result = PixelSet([(x, y) for x in range(width) for y in range(height) 
					   if all([(x + bx, y + by) in a for (bx, by) in b])])
    result.size, result.origin = a.size, a.origin
    return result
```
`a` and `b` are both `PixelSet`s. The algorithm follows the steps provided in the course slide.

#### Opening
```python
def opening(b, k):
    return dilation(erosion(b, k), k)
```

#### Closing
```python
def closing(b, k):
    return erosion(dilation(b, k), k)
```

#### Hit and Miss
```python
def hit_and_miss(a, j, k):
    result = erosion(a, j) & erosion(a.complement, k)
    result.size, result.origin = a.size, a.origin
    return result
```

### Benchmark and Result Images

![Original binarized image](https://i.imgur.com/LLoOTi2.png)

![Dilation](https://i.imgur.com/edDuR08.png)

![Erosion](https://i.imgur.com/0f1YvNR.png)

![Opening](https://i.imgur.com/PzNIqwN.png)

![Closing](https://i.imgur.com/RztlJB4.png)

![Hit and Miss](https://i.imgur.com/S4CUImu.png)


