from PIL import Image
from hw2 import histogram, draw_histogram

def histogram_equalization(img):
    result = Image.new('L', img.size)
    size = img.width * img.height
    hist = histogram(img)
    
    result.putdata(map(lambda k: sum(hist[:k]) * 255 / size, img.getdata()))
    return result

if __name__ == '__main__':
    img = Image.open('benchmarks/lena.bmp')

    histogram_equalization(img).save('results/histogram_equalization.bmp')

    img_div3 = Image.new('L', img.size)
    img_div3.putdata(map(lambda p: p / 3, img.getdata()))
    histogram_equalization(img_div3).save('results/histogram_equalization_div3.bmp')

