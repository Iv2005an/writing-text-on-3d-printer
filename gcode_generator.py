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

# ГЕНЕРАТОР GCODE
with open('text.gcode', 'w') as gcode:  # создание файла gcode
    gcode.write('G21\nG90\nG4 S5\nG92 X0 Y0 Z0\nG0 Z2 F6000\n')  # инициализация
    offset_y = 0
    offset_x = 0
    last_x = 0
    last_y = 0
    first = True
    el = False

    try:
        with open('font/connected.txt', encoding='utf-8') as u:
            connected = u.read()
    except FileNotFoundError:
        print('the "font/connected.txt" file was not found')
        input()
        sys.exit()


    def xy(symbol, ind):
        try:
            axes = symbols[symbol]
        except KeyError:
            print(f'the "font/{symbol}.png" file was not found')
            input()
            sys.exit()
        global offset_x, offset_y, m_y, last_y, last_x
        if ind > 0 and connected.count(text[ind]) > 0 \
                and connected.count(text[ind - 1]) > 0:
            gcode.write(f'G1 X{axes[0][0] + offset_x} Y{axes[0][1] + offset_y} F3600\n')  # перемещение к точке
        else:
            gcode.write(
                f'G0 X{axes[0][0] + offset_x} Y{axes[0][1] + offset_y} F6000\nG0 Z0 F6000\n')  # перемещение к точке
        for i in range(1, len(axes)):
            gcode.write(f'G1 X{axes[i][0] + offset_x} Y{axes[i][1] + offset_y} F3600\n')  # написание символа
            if m_y < axes[i][1]:  # крайняя координата символа
                m_y = axes[i][1]
            last_x = axes[i][0]
            last_y = axes[i][1]
        if ind < len(text) - 1:
            if not connected.count(text[ind]) > 0 \
                    or not connected.count(text[ind + 1]) > 0:
                gcode.write('G0 Z2 F6000\n')  # поднятие ручки


    for i in range(len(text)):  # посимвольно
        m_y = 0
        if '1234567890абвгдежзиклмнопрстуфхцчшщъыьэюяabcdefghklmnopqrstuvwxyz'.count(text[i]) > 0:
            xy(text[i], i)
        elif 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ'.count(text[i]) > 0:
            xy(f'_{text[i]}', i)
        elif text[i] == 'Ё':
            xy('_Е', i)
            xy('L^_Е', i)
            xy('R^_Е', i)
        elif text[i] == 'Й':
            xy('_И', i)
            xy('^_И', i)
        elif text[i] == 'ё':
            xy('е', i)
            xy('L^е', i)
            xy('R^е', i)
        elif text[i] == 'й':
            xy('и', i)
            xy('^и', i)
        elif text[i] == 'i':
            xy('i', i)
            xy('^i', i)
        elif text[i] == 'j':
            xy('j', i)
            xy('^j', i)
        elif ',-()[]{}'.count(text[i]) > 0:
            xy(text[i], i)
        elif text[i] == '.':
            xy('dot', i)
        elif text[i] == ':':
            xy('_dot', i)
            xy('^dot', i)
        elif text[i] == ';':
            xy('_,', i)
            xy('^dot', i)
        elif text[i] == '?':
            xy('_q', i)
            xy('^q', i)
        elif text[i] == '!':
            xy('dot', i)
            xy('ex', i)
        elif text[i] == '"':
            if first:
                xy('_,,L', i)
                xy('_,,R', i)
                first = False
            else:
                xy('^,,L', i)
                xy('^,,R', i)
                first = True
        elif text[i] == '\n':  # новая строка
            offset_x += 5
            offset_y = 0
        elif text[i] == '\t':
            offset_y += 10
        elif text[i] == ' ':  # пробел
            offset_y += 2.5
        else:
            print(f'"{text[i]}" not supported, remove from "text.txt"')
            el = True
        if not ' \n'.count(text[i]) > 0:
            offset_y += m_y + 1
    if el:
        input()
