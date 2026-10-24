import random
from abc import ABC, abstractmethod

# Base class for AI player
class AIPlayer(ABC):
    @abstractmethod
    def choose_move(self, board, mark):
        """Return a (row, col) tuple for an empty cell on the board."""

# picking any empty cell at random
class EasyAI(AIPlayer):
    def __init__(self, rng=None):
        if rng is None:
            rng = random.Random()
        self._rng = rng

    def choose_move(self, board, mark):
        return self._rng.choice(board.empty_cells())
