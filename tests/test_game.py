import pytest

from board import EMPTY
from game import Game

# to start testing with a new board so no other tests get affected with each other
@pytest.fixture
def game():
    """A fresh game for each test."""
    return Game()

# helper function that plays a list of moves in order
def play_all(game, moves):
    """Play a list of (row, col) moves in order."""
    for row, col in moves:
        game.play(row, col)

# making sure if X moves first 
def test_x_moves_first(game):
    assert game.current_player() == "X"

# passing the turn to other player after valid move
def test_turns_alternate_after_valid_moves(game):
    assert game.play(0, 0) is True
    assert game.current_player() == "O"
    assert game.play(1, 1) is True
    assert game.current_player() == "X"

# making sure the taken cell is not played again and being rejected, and the sane player tries again
def test_taken_cell_does_not_use_up_the_turn(game):
    game.play(0, 0)
    assert game.play(0, 0) is False
    assert game.current_player() == "O"
    assert game.get_board().cell(0, 0) == "X"

# playing out off the board and negative cells is rejected and smae player gets to play again
def test_off_board_move_does_not_use_up_the_turn(game):
    assert game.play(-1, 0) is False
    assert game.play(3, 3) is False
    assert game.current_player() == "X"
    assert len(game.get_board().empty_cells()) == 9

# a new game has no winner and is stil in progress
def test_new_game_is_not_over(game):
    assert game.is_over() is False
    assert game.get_winner() is None

# testing by marking top row with X and checking for the win
def test_completing_a_row_wins_the_game(game):
    play_all(game, [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)])
    assert game.get_winner() == "X"
    assert game.is_over() is True
    assert game.is_draw() is False

# Once someone is won, no further moves are accepted
def test_no_moves_are_accepted_after_a_win(game):
    play_all(game, [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)])
    assert game.play(2, 2) is False
    assert game.get_board().cell(2, 2) == EMPTY

# full board with no winner is a draw
def test_full_board_with_no_winner_is_a_draw(game):
    # X O X
    # X O O
    # O X X
    play_all(game, [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0),
                    (1, 2), (2, 1), (2, 0), (2, 2)])
    assert game.is_draw() is True
    assert game.is_over() is True
    assert game.get_winner() is None
