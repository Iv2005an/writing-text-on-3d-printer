from PIL import Image
import glob

# ГЕНЕРАТОР СЛОВАРЯ
png_count = glob.glob('font/*.png')
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

symbol = [i[5:-4] for i in png_count]
symbols = dict(zip(symbol, indexes))

# ИСТОЧНИК
with open('text.txt', encoding='utf-8') as file:
    text = file.read()
    file.close()

# ГЕНЕРАТОР GCODE
with open('text.gcode', 'w') as gcode:  # создание файла gcode
    gcode.write('G21\nG90\nG4 S5\nG92 X0 Y0 Z0\nG0 Z2\n')  # инициализация
    offset_y = 0
    offset_x = 0
    last_x = 0
    last_y = 0
    space = False


    def xy(axes, ind):
        global offset_x, offset_y, m_y, last_y, last_x
        if ind > 0 and 'абвгдежзиклмнопрстуфхцчшщъыьэюя'.count(
                text[ind]) > 0 and 'абвгдежзиклмнопрстуфхцчшщъыьэюя'.count(text[ind - 1]) > 0:
            gcode.write(f'G1 X{axes[0][0] + offset_x} Y{axes[0][1] + offset_y}\n')
        else:
            gcode.write(f'G0 X{axes[0][0] + offset_x} Y{axes[0][1] + offset_y}\nG0 Z0\n')
        for i in range(1, len(axes)):
            gcode.write(f'G1 X{axes[i][0] + offset_x} Y{axes[i][1] + offset_y}\n')
            if m_y < axes[i][1]:  # крайняя координата символа
                m_y = axes[i][1]
            last_x = axes[i][0]
            last_y = axes[i][1]
        if ind < len(text) - 1:
            if not 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'.count(text[ind + 1]) > 0:
                gcode.write('G0 Z2\n')  # поднятие ручки


    for i in range(len(text)):  # посимвольно
        m_y = 0
        if '1234567890'.count(text[i]) > 0:
            xy(symbols[text[i]], i)
        elif 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.count(text[i]) > 0:
            if text[i] == 'Ё':
                s = symbols['_Е']
                p_l = symbols['L^_Е']
                p_r = symbols['R^_Е']
                xy(s, i)
                xy(p_l, i)
                xy(p_r, i)
            elif text[i] == 'Й':
                s = symbols['_И']
                p = symbols['^_И']
                xy(s, i)
                xy(p, i)
            else:
                s = symbols[f'_{text[i]}']
                xy(s, i)
        elif 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'.count(text[i]) > 0:  # соединяемые символы
            if text[i] == 'ё':
                s = symbols['е']
                p_l = symbols['L^е']
                p_r = symbols['R^е']
                xy(s, i)
                xy(p_l, i)
                xy(p_r, i)
            elif text[i] == 'й':
                s = symbols['и']
                p = symbols['^и']
                xy(s, i)
                xy(p, i)
            else:
                s = symbols[text[i]]
                xy(s, i)
        elif text[i] == '\n':  # новая строка
            offset_x += 5
            offset_y = 0
            space = True
        elif text[i] == ' ':  # пробел
            offset_y += 2.5
            space = True
        else:
            print('else: ' + text[i])
        if not space:
            offset_y += m_y + 1
        else:
            space = not space
    gcode.close()
