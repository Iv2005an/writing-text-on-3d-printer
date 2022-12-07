from PIL import Image
import glob
import sys

# ГЕНЕРАТОР СЛОВАРЯ
png_count = glob.glob('font/*.png')
indexes = []
for png in png_count:
    with Image.open(png) as im:
        width, height = im.size
        pixels = list(im.getdata())  # получение массива пикселей
        pixels = [255 - pixels[i][0] for i in range(width * height)]  # инверсия массива
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]  # разбиение по строкам
        index = []
        for s in range(len(pixels)):
            for i in range(len(pixels[s])):
                if pixels[s][i] > 0:  # отсеивание белых пикселей
                    index.append([s / 10, i / 10, pixels[s][i]])  # получение данных пикселя:[x, y, цвет]
        index.sort(key=lambda x: x[2], reverse=True)  # сортировка по убыванию(от чёрного к белому)
        for i in range(len(index)):  # удаление цвета из массива
            index[i].pop(-1)
        indexes.append(index)  # массив с координатами
symbols = dict(zip([i[5:-4] for i in png_count], indexes))  # создание словаря

# ИСТОЧНИК
try:
    with open('text.txt', encoding='utf-8') as t:
        text = t.read()
except FileNotFoundError:
    print('the "text.txt" file was not found')
    input()
    sys.exit()

# ФОРМАТИРОВАНИЕ ТЕКСТА
with open('text_f.txt', 'w') as file:
    first = True
    el = False
    length = 0


    def max_y(symbol):
        try:
            axes = symbols[symbol]
        except KeyError:
            print(f'the "font/{symbol}.png" file was not found')
            input()
            sys.exit()
        m_y = 0
        for i in range(1, len(axes)):
            if m_y < axes[i][1]:  # крайняя координата символа
                m_y = axes[i][1]
                m_y += 1
                return m_y


    while i < len(text):  # посимвольно
        if '1234567890абвгдежзиклмнопрстуфхцчшщъыьэюяabcdefghklmnopqrstuvwxyz'.count(text[i]) > 0:
            length += max_y(text[i])
        elif 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ'.count(text[i]) > 0:
            length += max_y(f'_{text[i]}')
        elif text[i] == 'Ё':
            length += max_y('_Е')
        elif text[i] == 'Й':
            length += max_y('_И')
        elif text[i] == 'ё':
            length += max_y('е')
        elif text[i] == 'й':
            length += max_y('и')
        elif text[i] == 'i':
            length += max_y('i')
        elif text[i] == 'j':
            length += max_y('j')
        elif ',-()[]{}'.count(text[i]) > 0:
            length += max_y(text[i])
        elif text[i] == '.':
            length += max_y('dot')
        elif text[i] == ':':
            length += max_y('^dot')
        elif text[i] == ';':
            length += max_y('^dot')
        elif text[i] == '?':
            length += max_y('^q')
        elif text[i] == '!':
            length += max_y('ex')
        elif text[i] == '"':
            if first:
                length += max_y('_,,L')
                length += max_y('_,,R')
                first = False
            else:
                length += max_y('^,,L')
                length += max_y('^,,R')
                first = True
        elif text[i] == '\n':  # новая строка
            length = 0
            i += 1
            continue
        elif text[i] == ' ':  # пробел
            length += 2.5
        else:
            print(f'"{text[i]}" not supported, remove from "text.txt"')
            el = True
        if length > 65:
            text = text[:i] + '\n' + text[i:]
            length = 0
        i += 1
    if el:
        input()
    file.write(text)
