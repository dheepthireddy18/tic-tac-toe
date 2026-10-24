from game import Game
from ai import EasyAI, HardAI

# asking the user to enter 2 whole numbers 
def ask_for_move(mark):
    while True:
        parts = input(f"Player {mark}, enter row and column (1-3), e.g. 2 3: ").split()
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            print("Please type two whole numbers, like 2 3.")
            continue
        # players count from 1, the board counts from 0
        return int(parts[0]) - 1, int(parts[1]) - 1

# to print if the game is won or draw
def show_result(game):
    if game.is_draw():
        print("-" * 80)
        print(" ****************************** It's a draw! ****************************** ")
        print("-" * 80)
    else:
        print("-" * 80)
        print(f" ******************************* Player {game.get_winner()} wins! ******************************")
        print("-" * 80)

# run one game where 2 people take turns
''' 
def play_two_player():
    """Run one game where two people take turns at the keyboard."""
    game = Game()
    print(game.get_board())
    while not game.is_over():
        row, col = ask_for_move(game.current_player())
        if not game.play(row, col):
            print("That cell is taken or off the board. Try again.")
            continue
        print()
        print(game.get_board())
    show_result(game)
'''

# keep asking until the player types one of the allowed choices
def ask_for_choice(prompt, choices):
    while True:
        answer = input(prompt).strip()
        if answer in choices:
            return answer
        print(f"Please type one of: {', '.join(choices)}.")

# ask for the mode and level, and build the matching Game
def choose_game():
    mode = ask_for_choice("1) Two players   2) Versus computer: ", ["1", "2"])
    if mode == "1":
        return Game()
    level = ask_for_choice("1) Easy   2) Hard: ", ["1", "2"])
    ai = EasyAI() if level == "1" else HardAI()
    return Game(ai)

# run one game until someone wins or it is a draw
def play(game):
    print(game.get_board())
    while not game.is_over():
        if game.is_computer_turn():
            row, col = game.play_computer_turn()
            print(f"\nComputer plays {row + 1} {col + 1}")
        else:
            row, col = ask_for_move(game.current_player())
            if not game.play(row, col):
                print("That cell is taken or off the board. Try again.")
                continue
            print()
        print(game.get_board())
    show_result(game)

def main():
    print("=" * 80)
    print(" **************************  Welcome to Tic-Tac-Toe!  ************************** ")
    print("=" * 80)
    play(choose_game())


if __name__ == "__main__":
    main()
