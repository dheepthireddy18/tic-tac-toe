## Goal:
To create a Tic-Tac-Toe game on a 3x3 board, which runs in terminal. Two people can play with each other on one keyboard, and one person can play with X as their mark to play with, against a computer opponent as O as its mark at Easy or Hard difficulty.

## Requirements:

| ID |Requirements|Verification|
|----|------------|------------|
|REQ-1|X always goes first|By starting a new game and verify that X moves first and O cannot move before X. Restart the game and verify that X goes first again.|
|REQ-2|The game should always display a 3×3 board with nine cells.|Starting the game and verifying that the board and all nine cells are displayed.|
|REQ-3|The human player play as X, and the AI play as O.|Starting a new game and verify that the human moves are marked X and AI moves are marked O.|
|REQ-4|A player should only be allowed to place a mark in an empty cell.|Attempt to select an occupied cell and verify that its mark does not change.|
|REQ-5|The game should detect a draw when all nine cells are occupied and neither player has won.|Play a draw sequence and verify that the game announces a draw.|
|REQ-6|The game should detect a win when a player places three matching marks in a row, column, or diagonal.|Test all eight possible winning lines and verify that the correct winner is announced.|
|REQ-7|The game should stop further moves after a win or draw.|Finish a game and attempt another move; verify that the board remains unchanged.|
|REQ-8|The game shall display the updated board after every valid move.|Make several moves and verify that the board is displayed after each move, showing the updated marks in the correct cells|

## Components
- **board.py**: Creates a 3×3 grid `_grid` and it places and answers questions about the grid.
- **ai.py**: An abstract base class that defines `choose_move(board, mark)`, the one method every computer player must provide.
- **ai.py**: Implements EasyAI and HardAI as subclasses of the abstract AIPlayer class.
- **game.py**: Runs the rules of a match, whose turn it is, applying moves, and whether the game is won, drawn or still going without printing or reading input.
- **main.py**: Handles everything the player sees and types: menus, prompts, and printing the board and results.
- **tests/**: For checking Board, Game and the AI classes with pytest, using seeded randomness.

## Decisions

### 1: How to store the grid
- **Options:** a nested list (3 rows of 3), a flat list of 9 cells.
- **Chosen:** a nested list, built with a list comprehension.
- **Why:** A nested list represents the board naturally as 3 rows of 3 cells, which makes it easy to access a cell using its row and column coordinates. These coordinates can also be used by the fixed list of winning lines to check for a win.

### 2: How to check for a win.
- **Options:** Fixed list of all 8 winning lines (3 rows, 3 columns, 2 diagonals) as cell coordinates and check each one; loop over rows, columns and the two diagonals with separate code for each direction; or check only the lines through the last move placed.
- **Chosen:** a fixed list of the 8 winning lines, checked in single loop inside.
- **Why:** On a 3x3 board there are only 8 ways to win, so listing them makes the rules visible at a glance and leaves less room for off-by-one mistakes in diagonal loops.