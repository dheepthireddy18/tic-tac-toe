# tic-tac-toe

Tic-Tac-Toe is a game that runs in the terminal on a 3x3 board. This game has 2 ways to play, two people can play each other on one keyboard, or one person can play `X` against a computer as their opponent `O` with 2 difficulty levels: 
- Easy: picks a random empty cell
- Hard: uses the minimax algorithm and never loses

## Requirements:

- Python 3.10 or later
- pytest (installed from `requirements.txt`)

## Setup:

```bash
git clone https://github.com/dheepthireddy18/tic-tac-toe.git
cd tic-tac-toe
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## How to run:

```bash
python main.py
```

- Prompts you with 2 options choose:
`1` - for two players
`2` - user to play against the computer
- If you choose option `2`, it prompts you to pick between 2 difficulty levels, you play `X` and move first.
- enter your moves as row and columns, numbered from 1, separated by a space. For example, `2 3` is row 2, column 3.

A taken cell or a cell which is off the board, or input that is not two numbers prompts a message to let you try again without losing your turn. The board is printed after every move, and the game announces the winner or a draw.

## Running Tests:

```bash
pytest
or
pytest -v
```