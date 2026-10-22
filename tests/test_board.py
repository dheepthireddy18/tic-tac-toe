import pytest 

from board import Board, EMPTY

# for checking if the new board has 9 empty cells
def test_new_board_empty():
    board = Board()
    assert len(board.empty_cells()) == 9
    for row in range(3):
        for col in range(3):
            assert board.get(row, col) is EMPTY

# a valid move is stored and that cell is no longer as empty
def test_place_mark():
    board = Board()
    assert board.place_mark(1,1,"X") is True
    assert board.get(1,1) == "X"
    assert (1,1) not in board.empty_cells()

# second mark on cell which is taken is rejected and the first mark stays
def test_taken_cell_rejected():
    board = Board()
    board.place_mark(0,0,"X")
    assert board.place_mark(0,0,'O') is False
    assert board.get(0,0) == "X"

# checking the positions, including negatives, which are to be rejected and change nothing.
@pytest.mark.parametrize("row, col", [(-1, 0), (0, -1), (-1, -1), (3, 0), (0, 3), (5, 5)])
def test_off_board_rejected(row, col):
    board = Board()
    assert board.place_mark(row, col, "X") is False
    assert len(board.empty_cells()) == 9

# reading a cell that doesn't exist is a bug, so raises an error.
def test_get_off_board_raises():
    board = Board()
    with pytest.raises(ValueError):
        board.get(3, 0)

# remove_mark to undo a move
def test_remove_mark():
    board = Board()
    board.place_mark(2, 2, "O")
    board.remove_mark(2, 2)
    assert board.get(2, 2) is EMPTY
    assert len(board.empty_cells()) == 9


# empty_cells skips marked cells and lists the rest row by row.
def test_empty_cells_order():
    board = Board()
    board.place_mark(0, 1, "X")
    board.place_mark(2, 0, "O")
    assert board.empty_cells() == [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)]

def test_new_board_not_full():
    assert Board().is_full() is False

def test_board_full():
    board = Board()
    for row, col in board.empty_cells():
        board.place_mark(row, col, "X")
    assert board.is_full() is True