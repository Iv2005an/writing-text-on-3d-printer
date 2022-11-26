symbols = {'1': [[2, 1], [0, 3], [5, 3]], '7': [[1, 1], [4, 1], [2, 4]]}
with open('text.txt') as file:
    text = file.read()
gcode = ''
for i in range(len(text)):
    for xy in range(len(symbols[text[i]])):
        gcode += 'G1 X' + str(symbols[text[xy]][0][0])
print(gcode)
with open('text.gcode', 'w') as gcode:
    gcode.write('G21\nG90\nG4 S5\nG28 X Y Z10\n')
