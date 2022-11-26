with open('text.txt', encoding='utf-8') as file:
    text = file.readlines()
    i = 0
    while i < len(text):
        if len(text[i]) > 27:
            s_i = text[i].rfind(' ', 0, 27)
            if s_i == -1:
                s_i = text[i].find(' ')
            text.append(text[i][s_i:])
            text[i] = text[i][:s_i] + '\n'
            if text[i].find(' ') == 0:
                text[i] = text[i][1:]
            i += 1
            for n in range(len(text) - 1, 0, -1):
                if n > i:
                    text[n], text[n - 1] = text[n - 1], text[n]
            if text[i].find(' ') == 0:
                text[i] = text[i][1:]
        else:
            i += 1
    file.close()
with open('text_r.txt', 'w') as file:
    for i in range(len(text)):
        file.write(text[i])
