import random
from abc import ABC, abstractmethod

# Base class for every AI player; holds the random generator they all share
class AIPlayer(ABC):
    def __init__(self, rng=None):
        if rng is None:
            rng = random.Random()
        self._rng = rng

    @abstractmethod
    def choose_move(self, board, mark):
        """Return a (row, col) tuple for an empty cell on the board."""

# picking any empty cell at random
class EasyAI(AIPlayer):
    def choose_move(self, board, mark):
        return self._rng.choice(board.empty_cells())

# using minimax to find the best move, so it never loses on 3x3
class HardAI(AIPlayer):
    def choose_move(self, board, mark):
        opponent = "O" if mark == "X" else "X"
        best_score = None
        best_moves = []
        for row, col in board.empty_cells():
            board.place_mark(row, col, mark)          # try the move
            score = self._minimax(board, mark, opponent, False, 1)
            board.remove_mark(row, col)               # undo it
            if best_score is None or score > best_score:
                best_score = score
                best_moves = [(row, col)]
            elif score == best_score:
                best_moves.append((row, col))
        return self._rng.choice(best_moves)

    def _minimax(self, board, mark, opponent, my_turn, depth):
        """Score the board for mark: positive if mark can force a win, negative if it loses."""
        # base case: the game is over
        if board.has_won(mark):
            return 10 - depth
        if board.has_won(opponent):
            return depth - 10
        if board.is_full():
            return 0
        # recursive case: try every move for whoever plays next
        to_move = mark if my_turn else opponent
        scores = []
        for row, col in board.empty_cells():
            board.place_mark(row, col, to_move)
            scores.append(self._minimax(board, mark, opponent, not my_turn, depth + 1))
            board.remove_mark(row, col)
        return max(scores) if my_turn else min(scores)
