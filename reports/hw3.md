Homework 3 - Histogram Equalization
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
$ python hw3.py
```

This program will finish all three tasks assigned in this homework and export result images to the folder `results`, including:
1. `histogram_equalization.bmp`
2. `histogram_equalization_div3.bmp`

### Implementation Detail
```python
def histogram_equalization(img):
    result = Image.new('L', img.size)
    size = img.width * img.height
    hist = histogram(img)
    
    result.putdata(map(lambda k: sum(hist[:k]) * 255 / size, img.getdata()))
    return result
```
This code fragment implements **histogram equalization** and performs this algorithm on the original image `img` to produce the result image `result`. It utilizes `histogram`, which is completed in last homework, to get the *histogram* information used in performing *histogram equalization*. The code `lambda k: sum(hist[:k])` is used to implement the following equation given in the course material:
$$s_k=255\sum^k_{j=0}\frac{n_j}{n}$$
The code `map` surrounding that lambda function performs the following mapping given in the course material:
$$I(imhe, i, j) = s_k, where\ k=I(im, i, j)$$

### Benchmark Tests and Result Images
#### Perform Histogram Equalization on Original Benchmark Image
![Original image](https://i.imgur.com/DODJ0Zw.png)

![Histogram equalization performed on original image](https://i.imgur.com/UktvRdn.png)

#### Perform Histogram Equalization on Darkened Benchmark Image
The benchmark image for this test has been darkened by dividing intensity of each pixel of the image with `3`.

![Darkened original image with intensity of each pixel divided by 3](https://i.imgur.com/kYurLbV.png)

![Histogram equalization performed on darkened image](https://i.imgur.com/h0ef1J6.png)


