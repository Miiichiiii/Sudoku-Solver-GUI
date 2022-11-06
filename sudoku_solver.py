from copy import deepcopy


class Sudoku:
    def __init__(self, l):
        self.sudoku = deepcopy(l)

    def getBlock(self, x, y):
        # Return the block that contains the cell with coordinates x and y
        return [u for i in self.sudoku[y * 3:y * 3 + 3] for u in i[x * 3:x * 3 + 3]]

    def getRow(self, y):
        # Return the current row
        return self.sudoku[y]

    def getColumn(self, x):
        # Return the current column
        return [y[x] for y in self.sudoku]

    def getNotDefined(self):
        # Return a list with coordinates, which points to empty cells
        return [(x, y) for y, e in enumerate(self.sudoku) for x, _ in enumerate(e) if not self.getElem(x, y)]

    def getElem(self, x, y):
        # Return the current value of the cell
        return self.sudoku[y][x]

    def getPossibilities(self, x, y):
        # Return all the numbers that are possible for the current cell
        f = set()
        for y0, x0, b0 in zip(self.getRow(y), self.getColumn(x), self.getBlock(x // 3, y // 3)):
            f.add(y0)
            f.add(x0)
            f.add(b0)
        # Go through all numbers that are already used in the row, column and block
        # 'Invert' the result
        return [x for x in range(1, 10) if x not in f]

    def write(self, x, y, item):
        # Write the item to the cell
        self.sudoku[y][x] = item

    def get_first_not_defined(self):
        # Search in the Sudoku for the first element which has no value
        # Probally inefficient TODO
        for y in range(9):
            for x in range(9):
                if not self.sudoku[y][x]:
                    return x, y

    def backtreck(self):
        if start := self.get_first_not_defined():
            x, y = start
        else:
            return True
        for i in self.getPossibilities(x, y):
            self.write(x, y, i)
            if self.validate():
                if self.backtreck():
                    return True
        self.write(x, y, None)
        return False

    def validate(self):
        # Returns true if the sudoku is valid, false otherwise
        rows = [set() for _ in range(9)]
        columns = [set() for _ in range(9)]
        blocks = [[set() for _ in range(3)] for _ in range(3)]

        for y in range(9):
            for x in range(9):
                value = self.sudoku[y][x]
                if not value:  # If the cell has no value, continue
                    continue
                if value in rows[y] or value in columns[x] or value in blocks[y // 3][
                    x // 3]:  # If the value is already in the row, column or block, then the sudoku is not valid
                    return False

                # Add the current value to the current: row, column, block.
                rows[y].add(value)
                columns[x].add(value)
                blocks[y // 3][x // 3].add(value)

        return True

    def solve_simple(self):
        changed = True
        while changed:
            changed = False
            for x in self.getNotDefined():
                l = self.getPossibilities(*x)
                if len(l) == 1:
                    self.write(*x, l[0])
                    changed = True

    def is_solved(self):
        # Return true if the sudoku is solved
        return True if not self.getNotDefined() else False

    def solve(self):
        self.solve_simple()
        if self.is_solved():
            return self.sudoku
        self.backtreck()
        return self.sudoku

    def __str__(self):
        s = ""
        for y in self.sudoku:
            s += ", ".join((map(str, y))) + "\n"
        return s
