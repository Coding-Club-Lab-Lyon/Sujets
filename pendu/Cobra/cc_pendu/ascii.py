pendu_ascii = '''_________________
   ||   //      |
   ||  //       |
   || //        _
   ||//        (_)
   ||          \|/
   ||           |
   ||          / \\
   ||
==========='''
pendu_num = '''33333333333333333
   22   44      5
   22  44       5
   22 44        6
   2244        666
   22          a7b
   22           7
   22          8 9
   22
11111111111'''

class Pendu:
    def __init__(self):
        self.step = 0
    def __str__(self):
        pendu_grid = pendu_ascii.split('\n')
        pendu_numgrid = pendu_num.split('\n')
        base = [[" "]* len(pendu_grid[i]) for i in range(len(pendu_grid))]
        for i in range(self.step + 1):
            i_hex = hex(i)[2:]
            for y, line in enumerate(pendu_numgrid):
                for x, char in enumerate(line):
                    if char == i_hex:
                        base[y][x] = pendu_grid[y][x]
        return '\n'.join([''.join(line) for line in base])
    def set_step(self, step):
        if step < 0 or step > 11:
            raise ValueError("Step must be between 0 and 11")
        self.step = step