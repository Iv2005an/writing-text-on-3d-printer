symbols = {'1': [[2.5, 0], [1, 2], [5, 2]], '7': [[1, 0], [1, 3], [5, 1]]}  # словарь
with open('text.txt') as file:  # источник
    text = file.read()
    file.close()
with open('text.gcode', 'w') as gcode:  # создание файла gcode
    gcode.write('G21\nG90\nG4 S5\nG92 X0 Y0 Z0\nG0 Z2\n')  # инициализация
    offset_y = 0
    offset_x = 0
    last_x = 0
    last_y = 0
    space = False
    for i in range(len(text)):
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
        elif text[i] == '\n':  # новая строка
            gcode.write(f'G0 X{last_x + offset_x} Y0\n')
            offset_x += 5
            offset_y = 0
            space = True
        elif text[i] == ' ':  # пробел
            gcode.write(f'G0 Y{2.5 + offset_y}\n')
            offset_y += 2.5
            space = True
        else:
            print('else')
        if not space:
            offset_y += m_y + 1
        else:
            space = not space
    gcode.close()
