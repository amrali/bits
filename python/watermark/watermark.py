import sys

from random import randint
from PIL import Image

def load_image(filename):
    img = Image.open(filename)
    print("Opening image {}:".format(filename), img.format, img.size, img.mode)
    return img

def watermark(image):
    box = (690, 420, 810, 430)
    region = image.crop(box)
    data = region.load()

    for x in range(120):
        if randint(0,1) == 0:
            row_vals = (255, 255, 255, 0)
        else:
            row_vals = (0, 0, 0, 50)

        for y in range(10):
            data[x,y] = row_vals

    image.paste(region, box)

def main():
    if len(sys.argv) < 2:
        print("must supply a filename")
        return

    filename = sys.argv[1]

    for i in range(62):
        img = load_image(sys.argv[1])

        watermark(img)

        filename = 'letter-' + str(i).zfill(2) + '.png'
        img.save(filename)
        print("Generated", filename)
        img.close()

if __name__ == '__main__':
    main()
