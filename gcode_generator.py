symbols = {'1': [[1, 0], [4, 0]], '7': [[1, 0], [1, 3], [4, 1]]}
with open('text.txt') as file:
    text = file.read()
    file.close()
with open('text.gcode', 'w') as gcode:
    gcode.write('G21\nG90\nG4 S5\nG28 X Y\nG0 Z10\n')
    offset_y = 10
    offset_x = 0
    for i in range(len(text)):
        m_y = 0
        if '1234567890'.count(text[i]) > 0:
            xy = symbols[text[i]]
            gcode.write(f'G0 X{xy[0][0] + offset_x} Y{xy[0][1] + offset_y} Z0\n')
            for a in range(1, len(xy)):
                gcode.write(f'G1 X{xy[a][0] + offset_x} Y{xy[a][1] + offset_y}\n')
                if m_y < xy[a][1]:
                    m_y = xy[a][1]
        else:
            gcode.write(f'G0 X{xy[0][0] + offset_x} Y0 Z0\n')
            offset_x += 5
            offset_y = 0
        gcode.write('G0 Z10\n')
        offset_y += m_y + 1
    gcode.close()
