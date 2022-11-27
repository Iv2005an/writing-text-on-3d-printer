from PIL import Image
import glob

png_count = glob.glob('*.png')
for png in png_count:
    symbol = Image.open(png)
    weight, height = symbol.size
    symbol_pixels = list(symbol.getdata())
    for i in range(0, len(symbol_pixels), weight):
        symbol_pixels[i] = symbol_pixels[i:weight]
print('-----DEBUG-----')
print(png_count)
print(weight, height)
print(symbol.mode)
print(symbol_pixels)
