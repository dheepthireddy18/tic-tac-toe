# Code Review: tic-tac-toe (`feature/ai-opponents`)

**Reviewed:** 2026-11-04 · **Scope:** `ai.py`, `board.py`, `game.py`, `main.py`, `conftest.py`, `tests/`, `.github/workflows/ci.yml`
**Method:** read every file by hand, ran the test suite, and checked a few suspected bugs with short Python one-liners. No project files were changed and nothing was installed.

---

## Top 3 findings

### 1. Some digit input crashes the game (`main.py:8-12`)
`ask_for_move` checks input with `str.isdigit()` and then calls `int()`. `isdigit()` also returns `True` for characters such as `²` or `³`, but `int()` rejects them:

```text
>>> '²'.isdigit()
True
>>> int('²')
ValueError: invalid literal for int() with base 10: '²'
```

So typing `² 1` ends the program with a traceback in the middle of a game. Ctrl-D / Ctrl-C at any prompt (`main.py:7`, `main.py:28`) also prints a raw `EOFError` / `KeyboardInterrupt` traceback.
**Fix:** wrap `int()` in `try/except ValueError` (or check with `str.isdecimal()` plus `try`), and catch `EOFError`/`KeyboardInterrupt` in `main()` so the program exits cleanly.

### 2. `Game.play_computer_turn` has no guards and ignores whether the move worked (`game.py:55-58`)
- It throws away the return value of `self.play(row, col)`. If an AI ever returns a taken or off-board cell, `play` returns `False`, the turn stays with `O`, `is_computer_turn()` stays `True`, and the loop in `main.py:45-48` prints "Computer plays …" **forever**.
- With no AI it raises `AttributeError: 'NoneType' object has no attribute 'choose_move'` (checked).
- After the game is over it raises `IndexError: Cannot choose from an empty sequence` from both `EasyAI` and `HardAI` (checked).

**Fix:** at the start, `if not self.is_computer_turn(): raise RuntimeError(...)`, and raise if `self.play(...)` returns `False`. This turns a silent hang into a clear error.

### 3. The main claims are barely tested: "Hard never loses" and the whole CLI
- `tests/test_ai.py:66-75` tests "Hard never loses" with only 20 random games, with Hard always playing second. Nothing tests Hard **blocking** an opponent's win, Hard playing **first** as `X`, Hard vs Hard always drawing, or Hard choosing the quicker of two wins. The game tree is small enough to test every possible opponent line, which would actually prove the claim.
- `main.py` has **no tests at all**. That includes input parsing (finding 1), the off-board vs taken-cell messages, mode and level selection, and the result banner. With `monkeypatch` on `builtins.input` and `capsys`, these are quick to write.

---

## Tool results

| Tool | Result |
|---|---|
| `pytest` (from `.venv`) | **45 passed** in 2.74 s. Slowest: `test_hard_ai_never_loses_playing_second` at 2.59 s |
| `ruff check` | **Not run.** Ruff is not installed (not on `PATH`, not in `.venv`, not in `requirements.txt`), and the review was not allowed to install it. The PEP 8 findings below come from reading the code plus `awk`/`grep` checks for line length, trailing whitespace and the final newline. Note: ruff's default rules (`E4`, `E7`, `E9`, `F`) leave out `E501` and `E302`, so most of the style issues below would only appear with `select = ["E", "W", "D", "ANN"]` or similar. |

---

## Findings by severity

### High

| # | File:Line | Finding |
|---|---|---|
| H1 | `main.py:8-12` | `isdigit()`/`int()` mismatch crashes on input like `²`. No handling for `EOFError`/`KeyboardInterrupt` (see Top 3 #1). |
| H2 | `game.py:55-58` | `play_computer_turn` ignores `play()`'s result, so an invalid AI move hangs the program. It also crashes when there is no AI or the game is over (see Top 3 #2). |

### Medium

| # | File:Line | Finding |
|---|---|---|
| M1 | `tests/test_ai.py:66-75` | "Never loses" is only checked with random sampling, Hard playing second. Blocking, playing first and preferring a faster win are not tested (see Top 3 #3). |
| M2 | `main.py` (whole file) | No tests for any function: `ask_for_move`, `ask_for_choice`, `choose_game`, `play`, `show_result`. |
| M3 | `board.py:16-19` | The `'''A 3x3 tic-tac-toe game board.'''` string sits **above** `class Board`, so it is not a docstring. It is a no-op expression, and `Board.__doc__` is `None` (checked). Move it inside the class. |
| M4 | all modules | **Docstrings (PEP 257):** no module docstrings in any file. Almost every function and class is described with a `#` comment above the `def` instead of a docstring, so `help()` and IDEs show nothing. Only `AIPlayer.choose_move` (`ai.py:13`), `HardAI._minimax` (`ai.py:38`) and `Game.play` (`game.py:36-39`) have real docstrings. `Board`, `Game`, `AIPlayer`, `EasyAI` and `HardAI` all have `__doc__ == None`. |
| M5 | all modules | **Type hints:** none anywhere. Good places to start: `Board.place_mark(self, row: int, col: int, mark: str) -> bool`, `empty_cells() -> list[tuple[int, int]]`, `AIPlayer.__init__(self, rng: random.Random \| None = None)`, `choose_move(self, board: Board, mark: str) -> tuple[int, int]`, `Game.get_winner() -> str \| None`. |
| M6 | `game.py:23`, `game.py:31` | Misleading comments. `get_winner` says "return either Win or None", but it returns `"X"`, `"O"` or `None`. `is_over` says "True if someone has won", but it is also `True` for a draw (full board). |

### Low

| # | File:Line | Finding |
|---|---|---|
| L1 | `ai.py:23`, `game.py:47` | **DRY:** the "other player" toggle is written twice. Also, `ai.py:23` uses the literals `"X"`/`"O"` while `game.py:4-5` defines the constants `X`/`O`, and the tests use literals too. Put the marks and an `other(mark)` helper in one module (for example `board.py`) and import them. |
| L2 | `board.py:22, 26, 36, 66-69` | **DRY:** the board size `3` is a magic number in five places, and the separator `"--+---+--"` assumes 3 columns. Add a `SIZE = 3` constant. |
| L3 | `main.py:17-23`, `main.py:62-64` | **DRY/KISS:** `print("-" * 80)` appears 6 times, and each banner is padded with hand-counted `*`/`<` characters, so the lines have different widths (93, 114, 94 chars). A small `banner(text)` helper using `text.center(80, "*")` would fix both. |
| L4 | `main.py:51-55` | **KISS / coupling:** `Game.play` only returns `bool`, so the UI asks the board again to work out *why* the move failed. Returning a reason (an enum or a raised exception) would keep that logic in one place. |
| L5 | `board.py:30-31`, `39-41`, `48-50` | Off-board cells are handled three different ways: `cell()` raises `ValueError`, `place_mark()` returns `False`, and `remove_mark()` silently does nothing. Choose one approach and document it. |
| L6 | `board.py:39-45` | `place_mark` accepts any string. `place_mark(0, 0, " ")` returns `True` but leaves the cell empty, and `place_mark(0, 0, "Q")` is accepted (both checked). `Game` only passes `X`/`O`, so this can't happen today, but a check is cheap. |
| L7 | `ai.py:21-53` | **Performance:** plain minimax with no pruning or memoisation. Choosing a move takes about 0.12 s when Hard plays second, but about **1.1 s** on an empty board (checked). That is fine today, but it would be noticeable if Hard ever played first. Alpha-beta pruning or `functools.cache` on the board state would fix it. |
| L8 | `ai.py:22-35` | **DRY (minor):** `choose_move` repeats the place/score/undo loop from `_minimax`. This is acceptable because it collects ties for random choice, but a comment saying so would help. |
| L9 | `game.py:16-25` | Java-style getters (`get_board`, `get_winner`, `current_player`). `@property` is the usual Python style. This is a style choice, not a defect. |
| L10 | `conftest.py` | An empty file that is only there so pytest puts the repo root on `sys.path`. Add a one-line comment saying so, or replace it with `pythonpath = ["."]` in a `pyproject.toml` `[tool.pytest.ini_options]` section. |
| L11 | `.github/workflows/ci.yml:13-19` | CI only runs `pytest`: there is no lint step. It tests only Python 3.12, while the README says "3.10 or later". Add a `ruff check` step and a `python-version` matrix (`3.10`–`3.13`). |
| L12 | `game.py:19`; `tests/test_game.py:31, 38, 45` | Typos: "whoevers", "sane player", "smae player", "stil". |

### PEP 8 style (Low)

| Rule | Locations |
|---|---|
| **E501** line > 79 chars | `ai.py:38, 51` · `board.py:34, 36 (106), 38` · `game.py:38, 52` · `main.py:7, 18, 22, 35 (123), 38 (126), 53, 55, 63` · `tests/test_ai.py:14, 77` · `tests/test_board.py:28, 46, 99` · `tests/test_game.py:8, 31 (100), 38` |
| **E302** expected 2 blank lines | `ai.py:5, 16, 21` · `board.py:16/19` · `game.py:7` · `main.py:5, 15, 26, 34, 43, 61` · most top-level `def`s in `tests/test_ai.py`, `tests/test_board.py`, `tests/test_game.py` |
| **E225** missing whitespace around operator | `board.py:26` (`col <3`) |
| **W291** trailing whitespace | `game.py:15, 23` · `main.py:4` · `tests/test_game.py:20` |
| **W292** no newline at end of file | `board.py:70` · `game.py:58` |
| **E265** block comment should start with `# ` | `tests/test_ai.py:1` (`#Tests…`) |
| Naming | `board.py:36` uses `rows`/`cols` as single-index loop variables. Use `row`/`col` as everywhere else. |
| Import order | `tests/test_game.py:1-2`: put `import random` before `import pytest` (standard library first, then third-party, as `tests/test_ai.py` already does). |

---

## Untested cases

**`board.py`**
- `cell()` with a **negative** index (only `(3, 0)` is tested, `tests/test_board.py:33-35`). This is the case the comment at `tests/test_board.py:27` warns about.
- `remove_mark()` on an off-board cell (expected to do nothing silently).
- `place_mark()` with an invalid mark (`" "`, `""`, `"Q"`).

**`game.py`**
- **A win on the 9th move:** the board is full *and* there is a winner. `is_draw()` must be `False` and `get_winner()` must be the winner. The code handles this correctly, but it is the classic edge case and nothing tests it.
- `O` winning (only `X` wins are tested).
- `current_player()` after a win (it stays on the winner, because `play` doesn't switch turns after a win).
- `is_computer_turn()` is `False` once a game against the computer is over.
- `play_computer_turn()` with no AI, after game over, or when the AI returns an invalid move (finding H2).
- `play()` on a drawn (full) board returns `False`.

**`ai.py`**
- HardAI **blocks** an immediate opponent win.
- HardAI as `X` (moving first), including on an empty board.
- HardAI vs HardAI always ends in a draw.
- HardAI chooses an immediate win over a slower forced win (the `10 - depth` scoring).
- An exhaustive test that HardAI never loses against *every* opponent move sequence, instead of 20 random games.
- `EasyAI`/`HardAI` on a full board (currently raises `IndexError`; decide whether that is the intended behaviour).

**`main.py`** (no tests at all)
- `ask_for_move`: valid input, wrong number of values, non-numeric, negative (`-1 2`), Unicode digits (`² 1`), extra whitespace.
- `ask_for_choice`: rejects bad input and asks again.
- `choose_game`: returns a game with no AI, with `EasyAI` or with `HardAI` for each option.
- `play`: shows the off-board message vs the taken-cell message, and the 1-based numbers in "Computer plays".
- `show_result`: draw banner vs winner banner.

---

## What's working well
- The code is split cleanly into model (`Board`), rules (`Game`), strategy (`AIPlayer` subclasses) and UI (`main.py`), and the UI is the only place that does I/O.
- Injecting `random.Random` into the AIs makes them easy to test deterministically. The tests use this well.
- Off-board negative indices are rejected on purpose (`board.py:26`), which avoids Python's `grid[-1]` behaviour, and there is a test for it.
- The tests are short, named after the behaviour they check, use fixtures and `parametrize` (for example all 8 win lines), and check that the AIs leave the board unchanged after searching.
