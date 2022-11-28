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
    for i in range(len(text)):  # посимвольно
        m_y = 0
        if '1234567890'.count(text[i]) > 0:  # не соединяемые символы
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
            print(text[i])
            print('else')
        if not space:
            offset_y += m_y + 1
        else:
            space = not space
    gcode.close()
