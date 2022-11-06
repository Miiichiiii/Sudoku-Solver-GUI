from copy import deepcopy


class Sudoku:
    def __init__(self, l):
        self.sudoku = deepcopy(l)
        self.notDefined = []
        self.notDefinedIndex = 0

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

    def getFirstNotDefined(self):
        # Get the first element which has no value
        if self.notDefinedIndex >= len(self.notDefined):
            return None
        return self.notDefined[self.notDefinedIndex]

    def backtrack(self):
        if start := self.getFirstNotDefined():  # Get the first not defined cell. If there is no such element, then the sudoku is solved
            x, y = start
        else:
            return True
        for i in self.getPossibilities(x, y):  # Get all the possible values for the current cell
            self.write(x, y, i)  # Write first such value to the Sudoku
            self.notDefinedIndex += 1
            if self.backtrack():  # Make a recursive call. If the return value is true, this means the sudoku solution has been found
                return True
            self.notDefinedIndex -= 1
            # if false then the next possible value has to be tested
        self.write(x, y, None)
        return False  # The Sudoku has no valid solution

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
                if value in rows[y] or value in columns[x] or value in blocks[y // 3][x // 3]:  # If the value is already in the row, column or block, then the sudoku is not valid
                    return False

                # Add the current value to the current: row, column, block.
                rows[y].add(value)
                columns[x].add(value)
                blocks[y // 3][x // 3].add(value)

        return True

    def solveSimple(self):
        changed = True
        while changed:  # Do-while until no element has changed in one iteration
            changed = False
            for coords in self.getNotDefined():  # Get the coordinates of the empty cells
                l = self.getPossibilities(*coords)  # Get the possible values for the current cell
                if len(l) == 1:  # If there is only one possible value
                    self.write(*coords, l[0])  # Write it to the sudoku
                    changed = True

    def isSolved(self):
        # Return true if the sudoku is solved
        return True if not self.getNotDefined() else False

    def solve(self):
        self.solveSimple()  # Try to solve it the more efficient but less comprehensive way
        if self.isSolved():  # Check if the sudoku is now solved
            return self.sudoku
        self.notDefined = self.getNotDefined()  # Needed for an efficient getFirstNotDefinied method which will be used in backtrack
        self.backtrack()
        return self.sudoku

    def __str__(self):
        s = ""
        for y in self.sudoku:
            s += ", ".join((map(str, y))) + "\n"
        return s
