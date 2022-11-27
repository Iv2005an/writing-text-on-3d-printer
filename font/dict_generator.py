from PIL import Image
import glob

png_count = glob.glob('*.png')
indexes = []
for png in png_count:
    with Image.open(png) as symbol:
        width, height = symbol.size
        pixels = list(symbol.getdata())
        pixels = [255 - pixels[i][0] for i in range(width * height)]
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        a = 0
        index = []
        for s in range(len(pixels)):
            for i in range(len(pixels[s])):
                if pixels[s][i] > 0:
                    index.append([s / 10, i / 10, pixels[s][i]])
                    a += 1
        index.sort(key=lambda x: x[2], reverse=True)
        for i in range(len(index)):
            index[i].pop(-1)
        indexes.append(index)

symbol = [i[:-4] for i in png_count]
symbols = dict(zip(symbol, indexes))
with open('symbols.py', 'w') as file:
    file.write('symbols = ' + str(symbols))
