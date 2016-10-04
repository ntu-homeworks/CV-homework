from PIL import Image
from helpers.image import Pixels2D

def thresholding(img, at):
    result = Image.new('1', img.size)
    result.putdata(map(lambda x: int(x >= at), img.getdata()))
    return result

def histogram(img):
    result = [0] * 256
    for p in img.getdata():
        result[p] += 1
    return result

def draw_histogram(result):
    height = max(result) * 4 / 3
    result_img = Image.new('1', (256, height))

    result_data = Pixels2D([1] * 256 * height, width=256)
    for x, h in enumerate(result):
        for y in range(h):
            result_data[x, height - 1 - y] = 0

    result_img.putdata(result_data.data)
    return result_img.resize((height, height))

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

def draw_rectangle(img, left, right, top, bottom, color):
    # Draw top & bottom
    for x in range(left, right + 1):
        img.putpixel((x, top), color)
        img.putpixel((x, bottom), color)

    # Draw left & right
    for y in range(top, bottom + 1):
        img.putpixel((left, y), color)
        img.putpixel((right, y), color)


if __name__ == '__main__':
    img = Image.open('benchmarks/lena.bmp')

    # 1
    img_bin = thresholding(img, 128)
    img_bin.save('results/thresholding.bmp')

    # 2
    draw_histogram(histogram(img)).save('results/histogram.bmp')

    # 3
    RAINBOW = ((255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (127, 0, 255), (255, 0, 255))

    img_rec = Image.new('RGB', img.size)
    img_rec.putdata(map(lambda p: (p*255, p*255, p*255), img_bin.getdata()))
    colors = iter(RAINBOW)
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
    img_rec.save('results/connected_components.bmp')

