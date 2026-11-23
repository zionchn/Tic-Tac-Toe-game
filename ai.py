import random

def get_random_move(board):
    available_moves = []

    for position in range(len(board)):
        if board[position] == "":
            available_moves.append(position)

    if not available_moves:
        return None
    
    return random.choice(available_moves)


# Some test stuff, not important
# if __name__ == "__main__":

#     test_board = [
#         "X", "", "O",
#         "", "X", "",
#         "", "", "O"
#     ]

#     move = get_random_move(test_board)

#     print("Computer chooses position:", move)


def check_winner(board, player):
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

        if board[a] == board[b] == board[c] == player:
            return True

    return False


def find_winning_move(board, player):
    for position in range(9):
        if board[position] == "":
            board[position] = player

            if check_winner(board, player):
                board[position] = ""
                return position

            board[position] = ""

    return None


# Upgrading my AI. This function teaches the computer to Check if it can win, if not,
# then it checks if the player's move can be blocked, else it plays a random move
def get_medium_move(board):
    winning_move = find_winning_move(board, "O")

    if winning_move is not None:
        return winning_move

    blocking_move = find_winning_move(board, "X")

    if blocking_move is not None:
        return blocking_move

    return get_random_move(board)


# adding the minimax function for final boss difficulty. This function plays a move, checks for possible outcomes,
# Then unplays the move, plays another one, and checks for the possible outcomes. It chooses the best result.
def minimax(board, is_maximizing):

    if check_winner(board, "O"):
        return 10

    if check_winner(board, "X"):
        return -10

    if "" not in board:
        return 0

    if is_maximizing:
        best_score = float("-inf")

        for position in range(9):
            if board[position] == "":
                board[position] = "O"

                score = minimax(board, False)

                board[position] = ""

                best_score = max(score, best_score)

        return best_score

    else:
        best_score = float("inf")

        for position in range(9):
            if board[position] == "":
                board[position] = "X"

                score = minimax(board, True)

                board[position] = ""

                best_score = min(score, best_score)

        return best_score
    

# This takes the result from minimax and picks a position based off it
def get_best_move(board):
    best_score = float("-inf")
    best_move = None

    for position in range(9):
        if board[position] == "":
            board[position] = "O"

            score = minimax(board, False)

            board[position] = ""

            if score > best_score:
                best_score = score
                best_move = position

    return best_move
