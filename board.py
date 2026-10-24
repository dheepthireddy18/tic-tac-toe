# the value of a cell nobody has played yet
EMPTY = " "

# all 8 ways to win, as lists of cells: 3 rows, 3 columns, 2 diagonals
WIN_LINES = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]

'''
A 3x3 tic-tac-toe game board.
'''
class Board:
    def __init__(self):
        # for creating an empty 3x3 grid.
        self._grid = [[EMPTY] * 3 for _ in range(3)]

    # returns if the mentioned cell is on board or not
    def is_on_board(self, row, col):
        return 0 <= row < 3 and 0 <= col <3

    def cell(self, row, col):
        # return the mark at row, col counting from 0
        if not self.is_on_board(row, col):
            raise ValueError(f"({row}, {col}) is off the board")
        return self._grid[row][col]

    # this function returns a list of (row, col) tuples for every cell with no mark
    def empty_cells(self):
        return [(rows, cols) for rows in range(3) for cols in range(3) if self._grid[rows][cols] == EMPTY]

    # to mark the specific cell, returns True if placed, False if it is already taken
    def place_mark(self, row, col, mark):
        if not self.is_on_board(row, col):
            return False
        if self._grid[row][col] != EMPTY:
            return False
        self._grid[row][col] = mark
        return True

    # to clear the specific cell value
    def remove_mark(self, row, col):
        if self.is_on_board(row, col):
            self._grid[row][col] = EMPTY

    # return True if no cells are left empty
    def is_full(self):
        return not self.empty_cells()

    # return True if the mark filled any one of the 8 winning lines
    def has_won(self, mark):
        for line in WIN_LINES:
            if all(self._grid[row][col] == mark for row, col in line):
                return True
        return False

    def __str__(self):
        # Return the board as text with lines between the cells.
        lines = []
        for i, row in enumerate(self._grid):
            lines.append(" | ".join(row))
            if i < 2:
                lines.append("--+---+--")
        return "\n".join(lines)