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

# ФОРМАТИРОВАНИЕ ТЕКСТА
with open('text_f.txt', 'w', encoding='utf-8') as file:
    m_y = 0
    length = 0
    p_i = 0
    s_i = 0
    for i in range(len(text)):
        if '1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюя'.count(text[i]) > 0:
            xy = symbols[text[i]]
        elif 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.count(text[i]) > 0:
            if text[i] == 'Ё':
                xy = symbols['_Е']
            elif text[i] == 'Й':
                xy = symbols['_И']
            else:
                xy = symbols[f'_{text[i]}']
        for a in range(len(xy)):
            if m_y < xy[a][1]:
                m_y = xy[a][1]
        length += m_y
        if length > 130:
            s_i = text.find(' ', i)
            if p_i == 0:
                file.write(text[p_i:s_i] + '\n')
            else:
                file.write(text[p_i + 1:s_i] + '\n')
            p_i = s_i
            length = 0
    file.write(text[p_i + 1:])

# ГЕНЕРАТОР GCODE
with open('text.gcode', 'w') as gcode:  # создание файла gcode
    gcode.write('G21\nG90\nG4 S5\nG92 X0 Y0 Z0\nG0 Z2\n')  # инициализация
    offset_y = 0
    offset_x = 0
    last_x = 0
    last_y = 0
    space = False
    for i in range(len(text)):  # посимвольно
        m_y = 0
        if '1234567890'.count(text[i]) > 0:
            xy = symbols[text[i]]
            gcode.write(f'G0 X{xy[0][0] + offset_x} Y{xy[0][1] + offset_y} Z2\nG0 Z0\n')
            for a in range(len(xy)):
                gcode.write(f'G1 X{xy[a][0] + offset_x} Y{xy[a][1] + offset_y}\n')
                if m_y < xy[a][1]:  # крайняя координата символа
                    m_y = xy[a][1]
                last_x = xy[a][0]
                last_y = xy[a][1]
            gcode.write('G0 Z2\n')  # поднятие ручки
        elif 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.count(text[i]) > 0:
            if text[i] == 'Ё':
                s = symbols['_Е']
                p_l = symbols['L^_Е']
                p_r = symbols['R^_Е']
                gcode.write(f'G0 X{s[0][0] + offset_x} Y{s[0][1] + offset_y} Z2\nG0 Z0\n')
                for a in range(len(s)):
                    gcode.write(f'G1 X{s[a][0] + offset_x} Y{s[a][1] + offset_y}\n')
                    if m_y < s[a][1]:  # крайняя координата символа
                        m_y = s[a][1]
                    last_x = s[a][0]
                    last_y = s[a][1]
                gcode.write('G0 Z2\n')  # поднятие ручки
                gcode.write(f'G0 X{p_l[0][0] + offset_x} Y{p_l[0][1] + offset_y} Z2\nG0 Z0\n')
                for a in range(len(p_l)):
                    gcode.write(f'G1 X{p_l[a][0] + offset_x} Y{p_l[a][1] + offset_y}\n')
                    if m_y < p_l[a][1]:  # крайняя координата символа
                        m_y = p_l[a][1]
                    last_x = p_l[a][0]
                    last_y = p_l[a][1]
                gcode.write('G0 Z2\n')  # поднятие ручки
                gcode.write(f'G0 X{p_r[0][0] + offset_x} Y{p_r[0][1] + offset_y} Z2\nG0 Z0\n')
                for a in range(len(p_r)):
                    gcode.write(f'G1 X{p_r[a][0] + offset_x} Y{p_r[a][1] + offset_y}\n')
                    if m_y < p_r[a][1]:  # крайняя координата символа
                        m_y = p_r[a][1]
                    last_x = p_r[a][0]
                    last_y = p_r[a][1]
                gcode.write('G0 Z2\n')  # поднятие ручки
            elif text[i] == 'Й':
                s = symbols['_И']
                p = symbols['^_И']
                gcode.write(f'G0 X{s[0][0] + offset_x} Y{s[0][1] + offset_y} Z2\nG0 Z0\n')
                for a in range(len(s)):
                    gcode.write(f'G1 X{s[a][0] + offset_x} Y{s[a][1] + offset_y}\n')
                    if m_y < s[a][1]:  # крайняя координата символа
                        m_y = s[a][1]
                    last_x = s[a][0]
                    last_y = s[a][1]
                gcode.write('G0 Z2\n')  # поднятие ручки
                gcode.write(f'G0 X{p[0][0] + offset_x} Y{p[0][1] + offset_y} Z2\nG0 Z0\n')
                for a in range(len(p)):
                    gcode.write(f'G1 X{p[a][0] + offset_x} Y{p[a][1] + offset_y}\n')
                    if m_y < p[a][1]:  # крайняя координата символа
                        m_y = p[a][1]
                    last_x = p[a][0]
                    last_y = p[a][1]
                gcode.write('G0 Z2\n')  # поднятие ручки
            else:
                xy = symbols[f'_{text[i]}']
                gcode.write(f'G0 X{xy[0][0] + offset_x} Y{xy[0][1] + offset_y} Z2\nG0 Z0\n')
                for a in range(len(xy)):
                    gcode.write(f'G1 X{xy[a][0] + offset_x} Y{xy[a][1] + offset_y}\n')
                    if m_y < xy[a][1]:  # крайняя координата символа
                        m_y = xy[a][1]
                    last_x = xy[a][0]
                    last_y = xy[a][1]
                gcode.write('G0 Z2\n')  # поднятие ручки
        elif 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'.count(text[i]) > 0:  # соединяемые символы
            xy = symbols[text[i]]
            if i > 0:
                if 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'.count(text[i - 1]) > 0:
                    gcode.write('G1')
                else:
                    gcode.write('G0')
            gcode.write(f' X{xy[0][0] + offset_x} Y{xy[0][1] + offset_y}\nG0 Z0\n')
            for a in range(len(xy)):
                gcode.write(f'G1 X{xy[a][0] + offset_x} Y{xy[a][1] + offset_y}\n')
                if m_y < xy[a][1]:  # крайняя координата символа
                    m_y = xy[a][1]
                last_x = xy[a][0]
                last_y = xy[a][1]
        elif text[i] == '\n':  # новая строка
            gcode.write(f'G0 X{last_x + offset_x} Y0 Z2\n')
            offset_x += 5
            offset_y = 0
            space = True
        elif text[i] == ' ':  # пробел
            gcode.write(f'G0 Y{2.5 + offset_y} Z2\n')
            offset_y += 2.5
            space = True
        else:
            print('else: ' + text[i])
        if not space:
            offset_y += m_y + 1
        else:
            space = not space
    gcode.close()
