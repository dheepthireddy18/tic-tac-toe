import pytest

from board import Board, EMPTY

@pytest.fixture
def board():
    """A fresh, empty board for each test."""
    return Board()

def test_new_board_is_empty(board):
    assert len(board.empty_cells()) == 9
    for row in range(3):
        for col in range(3):
            assert board.cell(row, col) == EMPTY

def test_place_mark_puts_mark_on_cell(board):
    assert board.place_mark(1, 1, "X") is True
    assert board.cell(1, 1) == "X"
    assert (1, 1) not in board.empty_cells()

def test_cannot_place_on_taken_cell(board):
    board.place_mark(0, 0, "X")                 # Arrange
    result = board.place_mark(0, 0, "O")        # Act
    assert result is False                      # Assert
    assert board.cell(0, 0) == "X"

# negatives matter: Python's grid[-1] would quietly use the last row
@pytest.mark.parametrize("row, col", [(-1, 0), (0, -1), (-1, -1), (3, 0), (0, 3), (5, 5)])
def test_off_board_moves_are_rejected(board, row, col):
    assert board.place_mark(row, col, "X") is False
    assert len(board.empty_cells()) == 9

def test_reading_off_board_cell_raises(board):
    with pytest.raises(ValueError):
        board.cell(3, 0)

def test_remove_mark_empties_the_cell(board):
    board.place_mark(2, 2, "O")
    board.remove_mark(2, 2)
    assert board.cell(2, 2) == EMPTY
    assert len(board.empty_cells()) == 9

def test_empty_cells_skips_marked_cells(board):
    board.place_mark(0, 1, "X")
    board.place_mark(2, 0, "O")
    assert board.empty_cells() == [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)]

def test_new_board_is_not_full(board):
    assert board.is_full() is False

def test_board_is_full_after_nine_marks(board):
    for row, col in board.empty_cells():
        board.place_mark(row, col, "X")
    assert board.is_full() is True

# every winning line counts: 3 across, 3 down and both diagonals
@pytest.mark.parametrize("line", [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
], ids=["row0", "row1", "row2", "col0", "col1", "col2", "diag", "anti_diag"])
def test_win_on_every_line(board, line):
    for row, col in line:
        board.place_mark(row, col, "X")
    assert board.has_won("X") is True
    assert board.has_won("O") is False


def test_new_board_has_no_winner(board):
    assert board.has_won("X") is False
    assert board.has_won("O") is False


def test_mixed_line_is_not_a_win(board):
    board.place_mark(0, 0, "X")
    board.place_mark(0, 1, "O")
    board.place_mark(0, 2, "X")
    assert board.has_won("X") is False


def test_full_board_with_no_winner_is_draw(board):
    # X O X
    # X O O
    # O X X
    for i, mark in enumerate("XOXXOOOXX"):
        board.place_mark(i // 3, i % 3, mark)
    assert board.is_full() is True
    assert board.has_won("X") is False
    assert board.has_won("O") is False

def test_board_prints_as_a_grid(board):
    board.place_mark(0, 0, "X")
    board.place_mark(1, 1, "O")
    assert str(board) == "X |   |  \n--+---+--\n  | O |  \n--+---+--\n  |   |  "
