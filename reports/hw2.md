Homework 2 - Basic Image Manipulation
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
$ python hw2.py
```

This program will finish all three tasks assigned in this homework and export result images to the folder `results`, including:
1. `thresholding.bmp`
2. `histogram.bmp`
3. `connected_components.bmp`, with **4-connected neighborhood dectection**

### Implementation Detail
#### 1. Thresholding
```python
def thresholding(img, at):
    result = Image.new('1', img.size)
    result.putdata(map(lambda x: int(x >= at), img.getdata()))
    return result
```
This function `thresholding` is called with an argument `at`, determining the threshold value to perform with. The algorithm is to map all the pixels in the original image to `0` or `1`, depending on whether each pixel value is greater or equal than the threshold value `at`. The result, as a `list`, is then used to generate a new 1-bit image as the return value of this function.

#### 2. Histogram
```python
def histogram(img):
    result = [0] * 256
    for p in img.getdata():
        result[p] += 1
    return result
```
The algorithm utilizes a `list` named `result`, with size `256`, to store the histogram information and iterates all the pixels in the original image to count the number of each intensity value, i.e. `0`~`255`. The function return `result` as the histogram result.

```python
def draw_histogram(result):
    height = max(result) * 4 / 3
    result_img = Image.new('1', (256, height))

    result_data = Pixels2D([1] * 256 * height, width=256)
    for x, h in enumerate(result):
        for y in range(h):
            result_data[x, height - 1 - y] = 0

    result_img.putdata(result_data.data)
    return result_img.resize((height, height))
```
The returned value from `histogram` is then passed to `draw_histogram`. This function intuitively produces an 1-bit image for the histogram result in an usual representing form. `Pixels2D` is a self-made helper to convert image to a 2D-list.

#### 3. Connected Components
```python
def connected_components(img_bin):
    pixels = Pixels2D(img_bin)
    labels = []
    pixels_label = [[-1] * img.width for h in range(img.height)]

    for y in range(img.height):
        for x in range(img.width):
            if pixels[x, y] != 1:
                continue

            result_label = -1
            if x > 0 and pixels_label[y][x-1] != -1:
                result_label = pixels_label[y][x-1]
            if y > 0 and pixels_label[y-1][x] != -1:
                _result = pixels_label[y-1][x]

                if result_label != -1 and result_label != _result:
                    for _x, _y in labels[result_label]:
                        pixels_label[_y][_x] = _result
                    labels[_result] += labels[result_label]
                    labels[result_label] = None
                
                result_label = _result

            if result_label == -1:
                result_label = len(labels)
                labels.append([(x, y)])
            else:
                labels[result_label].append((x, y))

            pixels_label[y][x] = result_label

    return filter(lambda x: type(x)==list and len(x)>=500, labels)
```
The function `connected_components` generates, as the return value, a list of effective connected components, each represented as a list containing coordinates of pixels in that connected component. It adopts **4-connected neighborhood dectection** and the **classical algorithm**, with some improving modification.

Variable `pixels` is the pixel data in the original image, while two additional lists, `labels` and `pixels_label`, are used to help the algorithm computing. `labels` is a `list`, with the index as the label number, and each effective element of it is also a `list` storing pixels that has labeled to the label number. `pixels_label` is a 2D-`list`, indexed with the coordinate corresponding to the pixel in the original image, storing the label number of each pixel.

The modified algorithm progresses as original classical algorithm (top-down and left-right), except it do not hold the information of equivalent labels. Instead, when encountering a conflict (the lefter label and upper label has different value so these two values shall be equivalent), it fix the conflict immediately. In detail, it looks up `labels` to re-label all pixels in one label to another. This modification improves the complexity in development that the original image is iterated once.

After finishing progressing the algorithm, the variable `labels` is actually the result. Finally, only effective components containing more than 500 pixels are included in the returned value.

```python
def draw_rectangle(img, left, right, top, bottom, color):
    # Draw top & bottom
    for x in range(left, right + 1):
        img.putpixel((x, top), color)
        img.putpixel((x, bottom), color)

    # Draw left & right
    for y in range(top, bottom + 1):
        img.putpixel((left, y), color)
        img.putpixel((right, y), color)
```
The function `draw_rectangle` is a helper to draw the rectangle borders on the left, right, top, and bottom side of a connected component with specified color. Arguments left, right, top, and bottom of this function are all scalars, representing the leftmost, rightmost, topmost, and bottom-most positions of the rectangle, respectively.

```python
for component in connected_components(img_bin):
        color = next(colors)
        fill_color = tuple(map(lambda c: int(c * 0.6), color))

        (left, top), (right, bottom) = component[0], component[0]
        for x, y in component:
            if x < left:
                left = x
            if x > right:
                right = x
            if y < top:
                top = y
            if y > bottom:
                bottom = y
            img_rec.putpixel((x, y), fill_color)

        draw_rectangle(img_rec, left, right, top, bottom, color)
```
To sum it up, this code fragment finds the rectangular boundaries of each connected component and draw the rectangle borders for that component. It also fills the color of each component so as to distinguish between various connected components more easily.

### Result Images
| Original | Thresholding | Histogram | Connected Components |
|:--------:|:------------:|:---------:|:--------------------:|
| ![Original](https://i.imgur.com/oJbJsKM.png) | ![Thresholding](https://i.imgur.com/plM5S5R.png) | ![Histogram](https://i.imgur.com/5cCnCtJ.png?1) | ![Connected Components](https://i.imgur.com/CkQ7av6.png) |


