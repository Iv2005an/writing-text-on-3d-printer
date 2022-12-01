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
            s_i = i  # text.find(' ', i)
            if p_i == 0:
                file.write(text[p_i:s_i + 1] + '\n')
            else:
                file.write(text[p_i + 1:s_i + 1] + '\n')
            p_i = s_i
            length = 0
    file.write(text[p_i + 1:])
