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


# Some test stuff again, not important
# if __name__ == "__main__":

#     board1 = [
#         "O", "O", "",
#         "X", "X", "",
#         "", "", ""
#     ]

#     print("Test 1:", get_medium_move(board1))


#     board2 = [
#         "X", "X", "",
#         "O", "", "",
#         "", "O", ""
#     ]

#     print("Test 2:", get_medium_move(board2))
            