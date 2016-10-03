Homework 1 - Basic Image Manipulation
=================================
R05944012 資訊網路與多媒體研究所 梁智湧

Part 1
---------
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
$ python hw1.py
```

This program will finish three tasks assigned in the part 1 of this homework, exporting result images, including `upside_down.bmp`, `left_side_right.bmp`, and `diagonally_mirror.bmp`, to the folder `results`.

### Implementation Detail
#### 1. Upside Down
```python
def upside_down(img):
	data = Pixels2D(img)

	for x in range(img.width):
		for y in range(img.height / 2):
			data[x, y], data[x, img.height - 1 - y] = data[x, img.height - 1 - y], data[x, y]

	result = Image.new(img.mode, img.size)
	result.putdata(data.data)
	result.save('results/upside_down.bmp')
```

`Pixels2D` is a self-made helper to convert image to a 2D-list. The algorithm is to iterate all columns of the image and swap the upper pixel data and lower pixel data to reverse each column. After finishing the processing, export the image to a file.

#### 2. Right Side Left
```python
def right_side_left(img):
	data = Pixels2D(img)

	for y in range(img.height):
		for x in range(img.width / 2):
			data[x, y], data[img.width - 1 - x, y] = data[img.width - 1 - x, y], data[x, y]

	result = Image.new(img.mode, img.size)
	result.putdata(data.data)
	result.save('results/right_side_left.bmp')
```

The algorithm is to iterate all rows of the image, and then swap left pixel data and right pixel data to reverse each row. After finishing the processing, export the image to a file.

#### 3. Diagonally Mirror
```python
def diagonally_mirror(img):
	data = Pixels2D(img)

	for y in range(img.height):
		for x in range(y):
			data[x, y] = data[y, x]

	result = Image.new(img.mode, img.size)
	result.putdata(data.data)
	result.save('results/diagonally_mirror.bmp')
```

The algorithm is to give each pixel of bottom-left of the image, with coordinate `(x, y)`, the pixel data of `(y, x)`. After finishing the processing, export the image to a file.

### Result Images
| Original | Upside Down | Right Side Left | Diagonally Mirror |
|:--------:|:-----------:|:---------------:|:-----------------:|
| ![Original Lena](https://i.imgur.com/oJbJsKM.png) | ![Upside Down](https://i.imgur.com/m6rOMHy.png) | ![Right Side Left](https://i.imgur.com/sLHJwGU.png) | ![Diagonally Mirror](https://i.imgur.com/C0in0LX.png) |


Part 2
----------

### Software Description
- Software: **Microsoft Office Powerpoint 2016 on Mac**
- Version: **15.22 (160506)**
- Environment: **OS X EI Capitan (10.11.6) on Macbook (12", 2015)**

### Steps to process assigned tasks
#### 1. Rotate 45 degree clockwise
##### i. Load image
![Load Image](https://i.imgur.com/KRM5Vsi.png)
Drag the source image into the canvas in the **PowerPoint**.

##### ii. Rotate image
![Rotate Image](https://i.imgur.com/sUXhwzS.png)
Drag the rotation button on top of the image clockwise until the degree label shown next to the mouse pointer becomes `45°`.

##### iii. Export image
![Export Image](https://i.imgur.com/oYaTKhY.png)
Right click on the image and select **Export to image**.

#### 2. Shrink the image to half
##### i. Load image
![Load Image](https://i.imgur.com/KRM5Vsi.png)
Drag the source image into the canvas in the **PowerPoint**.

##### ii. Open resizing tab
![Open Resizing Tab](https://i.imgur.com/oYaTKhY.png)
Right click on the image and select **大小及位置...**.

##### iii. Resize to half
![Resize to half](https://i.imgur.com/XvuuWlf.png)
Set width(**縮放寬度**) and height(**縮放高度**) to `50%`.

##### iv. Export image
![Export Image](https://i.imgur.com/oYaTKhY.png)
Right click on the image and select **Export to image**.

#### 3. Binarize the image
##### i. Load image
![Load Image](https://i.imgur.com/KRM5Vsi.png)
Drag the source image into the canvas in the **PowerPoint**.

##### ii. Binarize image
![Binarize Image](https://i.imgur.com/67KwL45.jpg)
Apply the built-in filter **黑白: 50%**, which is in the filter set **色彩** under tab **圖片格式**, to the image to binarize it at 128.

##### iii. Export image
![Export Image](https://i.imgur.com/oYaTKhY.png)
Right click on the image and select **Export to image**.

### Result Images
| Original | Rotate 45° Clockwise | Shrink to Half | Binarize to 128 |
|:--------:|:--------------------:|:--------------:|:---------------:|
| ![Original](https://i.imgur.com/doxglYc.png) | ![Rotate 45](https://i.imgur.com/yXDld5A.jpg) | ![Shrink Half](https://i.imgur.com/0TOkSb3.jpg) | ![Binarize 128](https://i.imgur.com/EQaT1iU.jpg) |

