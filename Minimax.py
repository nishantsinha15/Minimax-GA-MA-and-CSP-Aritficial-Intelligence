import copy
import time


def isWinner(ch, board):
    if (board[0][0] == ch and board[0][1] == ch and board[0][2] == ch) \
            or (board[1][0] == ch and board[1][1] == ch and board[1][2] == ch) \
            or (board[2][0] == ch and board[2][1] == ch and board[2][2] == ch):
        return True

    if (board[0][0] == ch and board[1][0] == ch and board[2][0] == ch) \
            or (board[0][1] == ch and board[1][1] == ch and board[2][1] == ch) \
            or (board[0][2] == ch and board[1][2] == ch and board[2][2] == ch):
        return True

    if (board[0][0] == ch and board[1][1] == ch and board[2][2] == ch) \
            or board[0][2] == board[1][1] == board[2][0] == ch:
        return True

    return False


# returns 0, 1, -1 accordingly.
# returns 2 for non terminal state
def utility(board):
    if isWinner('X', board):
        return -1
    elif isWinner('O', board):
        return 1
    elif '*' not in board[0] and '*' not in board[1] and '*' not in board[2]:
        return 0
    else:
        return 2


def check_terminal(board):
    x = utility(board)
    if x == 2:
        return -1
    if x == 1:
        print("Computer wins")
    elif x == -1:
        print("You win")
    elif x == 0:
        print("Game Draw")
    return 1


def minimax(board, flag):
    actions = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    x = utility(board)
    if x != 2:
        return board, x
    if flag == 'min':
        min_val = 100
        for a in actions:
            next_state = make_move(copy.deepcopy(board), a, 'X')
            if next_state is None:
                continue
            garbage, temp = minimax(copy.deepcopy(next_state), 'max')
            if temp < min_val:
                min_val = temp
                state = next_state
        return state, min_val
    else:
        max_val = -100
        for a in actions:
            next_state = make_move(copy.deepcopy(board), a, 'O')
            if next_state is None:
                continue
            garbage, temp = minimax(copy.deepcopy(next_state), 'min')
            if temp > max_val:
                max_val = temp
                state = next_state
        return state, max_val


def make_move(board, action, ch):
    a, b = action[0], action[1]
    if board[a][b] != '*':
        return None
    board[a][b] = ch
    return board


def print_board(board):
    for i in range(3):
        for j in range(3):
            print(board[i][j], end = "\t")
        print()


def user_move(board):
    a, b = map(int,input().split())
    return make_move(board, (a,b), 'O')


def main():
    board = [['*' for i in range(3)] for j in range(3)]
    while check_terminal(board) == -1:
        print_board(board)
        print("Your turn")
        board = user_move(board)
        print_board(board)
        if check_terminal(board) != -1:
            print("Game over")
            break
        print("Computer's turn")
        start_time = time.time()
        board, val = minimax(board, 'min')
        end_time = time.time()
        print("Computer took ", end_time-start_time, " seconds")
    print_board(board)


main()