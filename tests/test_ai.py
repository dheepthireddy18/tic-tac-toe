#Tests for the AI players: the abstract base class and EasyAI.
import random
import pytest

from ai import AIPlayer, EasyAI, HardAI
from board import Board
from game import Game

# empty board for each test
@pytest.fixture
def board():
    return Board()

# abstract base class only describing what an AI must do, so it cannot be created
def test_ai_player_cannot_be_created_directly():
    with pytest.raises(TypeError):
        AIPlayer()

# a subclass that forgets choose_move cannot be created either
def test_ai_without_choose_move_cannot_be_created():
    class BrokenAI(AIPlayer):
        pass

    with pytest.raises(TypeError):
        BrokenAI()

# Easy only picks an empty cell, checked across many seeds
def test_easy_ai_only_picks_empty_cells(board):
    for row, col in [(0, 0), (0, 1), (1, 1), (2, 2)]:
        board.place_mark(row, col, "X")
    for seed in range(50):
        move = EasyAI(random.Random(seed)).choose_move(board, "O")
        assert move in board.empty_cells()

# the same seed gives the same move, so tests are repeatable
def test_easy_ai_with_same_seed_makes_same_choice(board):
    first = EasyAI(random.Random(7)).choose_move(board, "O")
    second = EasyAI(random.Random(7)).choose_move(board, "O")
    assert first == second

# with only one empty cell left, Easy must pick it
def test_easy_ai_picks_the_last_empty_cell(board):
    for i, mark in enumerate("XOXXOOOX"):
        board.place_mark(i // 3, i % 3, mark)
    assert EasyAI(random.Random(1)).choose_move(board, "O") == (2, 2)

# choosing a move must not place a mark on the real board
def test_easy_ai_choose_move_leaves_board_unchanged(board):
    board.place_mark(1, 1, "X")
    before = str(board)
    EasyAI(random.Random(3)).choose_move(board, "O")
    assert str(board) == before

# Hard completes its own line when it can win this turn
def test_hard_ai_takes_a_winning_move(board):
    # O O .
    # X X .
    # . . X
    for row, col in [(1, 0), (1, 1), (2, 2)]:
        board.place_mark(row, col, "X")
    for row, col in [(0, 0), (0, 1)]:
        board.place_mark(row, col, "O")
    assert HardAI(random.Random(1)).choose_move(board, "O") == (0, 2)

# playing second against a random opponent, Hard never loses (20 seeded games)
def test_hard_ai_never_loses_playing_second():
    for seed in range(20):
        game = Game()
        easy = EasyAI(random.Random(seed))
        hard = HardAI(random.Random(seed))
        while not game.is_over():
            ai = easy if game.current_player() == "X" else hard
            row, col = ai.choose_move(game.get_board(), game.current_player())
            game.play(row, col)
        assert game.get_winner() != "X"

# Hard tries moves while searching, but must put the board back exactly as it was
def test_hard_ai_choose_move_leaves_board_unchanged(board):
    board.place_mark(0, 0, "X")
    before = str(board)
    HardAI(random.Random(3)).choose_move(board, "O")
    assert str(board) == before
