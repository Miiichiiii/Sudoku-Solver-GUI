from copy import deepcopy


class Sudoku:
    def __init__(self, l):
        self.sudoku = deepcopy(l)

    def get_block(self, x, y, list=True):
        return [[x for x in u[x * 3:x * 3 + 3]] for u in self.sudoku[y * 3:y * 3 + 3]] if not list else [u for i in self.sudoku[y * 3:y * 3 + 3] for u in i[x * 3:x * 3 + 3]]

    def get_line_horizontal(self, y):
        return self.sudoku[y]

    def get_line_vertical(self, x):
        return [y[x] for y in self.sudoku]

    def get_not_defined(self):
        return [(x, y) for y, e in enumerate(self.sudoku) for x, _ in enumerate(e) if not self.get_elem(x, y)]

    def get_elem(self, x, y):
        return self.sudoku[y][x]

    def get_possibilities(self, x, y):
        f = set()
        for y0, x0, b0 in zip(self.get_line_horizontal(y), self.get_line_vertical(x), self.get_block(int(x / 3), int(y / 3), self.sudoku)):
            f.add(y0)
            f.add(x0)
            f.add(b0)
        return [x for x in range(1, 10) if x not in f]

    def write(self, x, y, item):
        self.sudoku[y][x] = item

    def get_first_not_defined(self):
        for y in range(9):
            for x in range(9):
                if not self.sudoku[y][x]:
                    return x, y

    def backtreck(self):
        if start := self.get_first_not_defined():
            x, y = start
        else:
            return True
        for i in self.get_possibilities(x, y):
            self.write(x, y, i)
            if self.validate():
                if self.backtreck():
                    return True
        self.write(x, y, None)
        return False

    @staticmethod
    def _valid_helper(l):
        if sorted(list(filter(bool, list(set(l))))) == sorted(list(filter(bool, l))):
            return True

    def validate(self):
        for y in range(9):
            for x in range(9):
                if self._valid_helper(self.get_line_horizontal(y)):
                    if self._valid_helper(self.get_line_vertical(x)):
                        if self._valid_helper(self.get_block(x % 3, y % 3)):
                            continue
                return False
        return True


    def write_simple(self):
        changed = True
        while changed:
            changed = False
            for x in self.get_not_defined():
                l = self.get_possibilities(*x)
                if len(l) == 1:
                    self.write(*x, l[0])
                    changed = True

    def is_solved(self):
        return True if not self.get_not_defined() else False

    def solve(self):
        self.write_simple()
        if self.is_solved():
            return self.sudoku
        self.backtreck()
        return self.sudoku

    def __str__(self):
        s = ""
        for y in self.sudoku:
            s += ", ".join((map(str, y))) + "\n"
        return s
