symbols = {1: [0.1, 0.5, 0.8, 0.5], 2: [0.1, 0.5, 0.8, 0.5], 3: [0.1, 0.5, 0.8, 0.5],
           4: [0.1, 0.5, 0.8, 0.5], 5: [0.1, 0.5, 0.8, 0.5], 6: [0.1, 0.5, 0.8, 0.5],
           7: [0.1, 0.5, 0.8, 0.5], 8: [0.1, 0.5, 0.8, 0.5], 9: [0.1, 0.5, 0.8, 0.5],
           0: [0.1, 0.5, 0.8, 0.5]}

with open('text.txt') as file:
    text = file.readlines()
    file.close()
for i in range(len(text[0])):
    print(symbols[int(text[0][i])])

gcode = open('text.gcode', 'w')
gcode.write('G21\nG90\nG28 X Y\n')
gcode.close()
