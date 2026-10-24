from board import Board

# the two marks; X always moves first
X = "X"
O = "O"

class Game:

    def __init__(self, ai=None):
        self._board = Board()
        self._current = X
        self._winner = None
        self._ai = ai

    # returning the board 
    def get_board(self):
        return self._board

    # returning the mark to whoevers turn it is
    def current_player(self):
        return self._current

    # return either Win or None 
    def get_winner(self):
        return self._winner

    # return True if board is full and nobody has won
    def is_draw(self):
        return self._winner is None and self._board.is_full()

    # return True if someone has won
    def is_over(self):
        return self._winner is not None or self._board.is_full()

    def play(self, row, col):
        """
        Placing the current mark at row, col. Return True if the move was made.
        A taken or off-board cell returns False and the same player keeps the turn.
        """
        if self.is_over():
            return False
        if not self._board.place_mark(row, col, self._current):
            return False
        if self._board.has_won(self._current):
            self._winner = self._current
        else:
            self._current = O if self._current == X else X
        return True

    # return True if it is the computer's turn to move
    def is_computer_turn(self):
        return self._ai is not None and self._current == O and not self.is_over()

    # ask the AI for a move and play it; works the same for any AI level
    def play_computer_turn(self):
        row, col = self._ai.choose_move(self._board, self._current)
        self.play(row, col)
        return row, col