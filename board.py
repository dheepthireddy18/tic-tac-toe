# default empty space in the cells before anybody plays.
EMPTY = None

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
A 3x3 tic-tac-toe grid, for marking the choices according to users choices.
'''
class Board:
    def __init__(self):
        # for creating an empty 3x3 grid.
        self._grid = [[EMPTY for _ in range(3)] for _ in range(3)]
    
    # this function returns a list of (row, col) tuples for every cell with no mark
    def empty_cells(self):
        cells = []
        for row in range(3):
            for col in range(3):
                if self._grid[row][col] is EMPTY:
                    cells.append((row, col))
        return cells

    # returns if the mentioned cell is on board or not
    def is_on_board(self, row, col):
        return 0 <= row < 3 and 0 <= col <3

    # to mark the specific cell. Return True if placed, False if it is already taken
    def place_mark(self, row, col, mark):
        if not self.is_on_board(row, col):
            return False
        if self._grid[row][col] is not EMPTY:
            return False
        self._grid[row][col] = mark
        return True

    # to clear the specific cell value
    def remove_mark(self, row, col):
        if self.is_on_board(row, col):
            self._grid[row][col] = EMPTY

    # Return the mark at the cell "X", "O" or EMPTY
    def get(self, row, col):
        if not self.is_on_board(row, col):
            raise ValueError(f"({row}, {col}) is off the board")
        return self._grid[row][col]

    # return True if no cells are left empty
    def is_full(self):
        return len(self.empty_cells()) == 0

    # return True if the mark filled any one of the 8 winning lines
    def has_won(self, mark):
        for line in WIN_LINES:
            if all(self._grid[row][col] == mark for row, col in line):
                return True
        return False