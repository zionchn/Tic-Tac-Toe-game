def create_board():
    return [""] * 9 # creates 9 empty strings



def display_board(board):
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("---+---+---")


def check_winner(board):
    winning_combinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],

    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],

    [0, 4, 8],
    [2, 4, 6]
    ]

    for combo in winning_combinations:
        a, b, c = combo
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
        
    return None


def check_draw(board):
    return "" not in board and check_winner(board) is None


def is_valid_move(board, position):
    return 0 <= position < 9 and board[position] == ""

def make_move(board, position, player):
    if is_valid_move(board, position):
        board[position] = player
        return True
    return False

def switch_player(current_player):
    if current_player == "X":
        return "O"
    return "X"


# This function plays the game, will call at the end to run it
def play_game():
    while True:
        board = create_board()

        current_player = "X"

        while True:
            display_board(board)
            print(f"\nPlayer {current_player}'s turn")
            try:
                position = int(input("Choose a position (0-8): "))
            except ValueError:
                print("Please enter a valid number!")
                continue
            if make_move(board, position, current_player):
                print("Move successful")
            else:
                print("Invalid move. Try again.")
                continue

            winner = check_winner(board)
            if winner:
                display_board(board)
                print(f"Player {winner} wins!")
                break

            if check_draw(board):
                display_board(board)
                print("It's a draw!")
                break

            current_player = switch_player(current_player)

        replay = input("\nPlay again? (yes/no): ").lower()
        if replay != "yes":
            print("Thanks for playing!")
            break


# Run the game
if __name__ == "__main__":
    play_game()
