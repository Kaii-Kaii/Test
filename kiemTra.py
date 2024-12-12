import copy
import math
import random
import numpy

X = "X"
O = "O"
EMPTY = None
user = None
ai = None


##################################################
#! câu 1
def display_board(board):
    # tạo bàn cờ có dạng 
    #    |   |
    # ---------
    #    |   |
    # ---------
    #    |   |
    print("\n")
    for row in board:
        print(" | ".join([" " if cell is None else cell for cell in row]))
        print("-" * 9)
    


def initial_state(n):
    """
    Returns starting state of the board.
    """
    board = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(EMPTY)
        board.append(row)
    return board

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for i in board:
        for j in i:
            if j:
                count += 1
    if count % 2 != 0:
        return ai
    return user

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()
    board_len = len(board)
    for i in range(board_len):
        for j in range(board_len):
            if board[i][j] == EMPTY:
                res.add((i, j))
    return res

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    curr_player = player(board)
    result_board = copy.deepcopy(board)
    (i, j) = action
    result_board[i][j] = curr_player
    return result_board

def get_horizontal_winner(board):
    # check horizontally
    winner_val = None
    board_len = len(board)
    for i in range(board_len):
        winner_val = board[i][0]
        for j in range(board_len):
            if board[i][j] != winner_val:
                winner_val = None
        if winner_val:
            return winner_val
    return winner_val

def get_vertical_winner(board):
    # check vertically
    winner_val = None
    board_len = len(board)
    for i in range(board_len):
        winner_val = board[0][i]
        for j in range(board_len):
            if board[j][i] != winner_val:
                winner_val = None
        if winner_val:
            return winner_val
    return winner_val

def get_diagonal_winner(board):
    # check diagonally
    winner_val = None
    board_len = len(board)
    winner_val = board[0][0]
    for i in range(board_len):
        if board[i][i] != winner_val:
            winner_val = None
    if winner_val:
        return winner_val
    winner_val = board[0][board_len - 1]
    for i in range(board_len):
        j = board_len - 1 - i
        if board[i][j] != winner_val:
            winner_val = None
    return winner_val

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner_val = get_horizontal_winner(board) or get_vertical_winner(board) or get_diagonal_winner(board) or None
    return winner_val

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_val = winner(board)
    if winner_val == X:
        return 1
    elif winner_val == O:
        return -1
    return 0

def maxValue(state):
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        v = max(v, minValue(result(state, action)))
    return v

def minValue(state):
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        v = min(v, maxValue(result(state, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    if current_player == X:
        min = -math.inf
        for action in actions(board):
            check = minValue(result(board, action))  # FIXED
            if check > min:
                min = check
                move = action
    else:
        max = math.inf
        for action in actions(board):
            check = maxValue(result(board, action))  # FIXED
            if check < max:
                max = check
                move = action
    return move
if __name__ == "__main__":
    #! câu 5
    # Tạo một danh sách move_history để lưu lại từng nước đi dưới dạng (player, (row, col)).
    move_history = []
    #! câu 2
    n = int(input("Enter the size of the board: "))
    board = initial_state(n)
    x = int(input("Chọn chế độ chơi: 1. Người VS Máy, 2. Người VS Người: "))
    if x == 1:
        ai_turn = False
        print("Choose a player")
        user = input()
        if user == "X":
            ai = "O"
        else:
            ai = "X"
        while True:
            game_over = terminal(board)
            playr = player(board)
            if game_over:
                # chỉnh ở đây
                winner_val = winner(board)
                if winner_val is None:
                    print("Game Over: Tie.")
                else:
                    print(f"Game Over: {winner_val} wins.")
                break;

            else:
                if user != playr and not game_over:
                    if ai_turn:
                        move = minimax(board)
                        board = result(board, move)
                        ai_turn = False
                        #! Câu 1
                        display_board(board)
                        #! ####################
                elif user == playr and not game_over:
                    ai_turn = True
                    print("Enter the position to move (row,col)")
                    i = int(input("Row:"))
                    j = int(input("Col:"))
                    move_history.append((user, (i, j)))
                    if board[i][j] == EMPTY:
                        board = result(board, (i, j))
                        #! câu 1
                        display_board(board)
                        #! ####################
    #! câu 3
    else:
        user = X
        ai = O
        while True:
            game_over = terminal(board)
            playr = player(board)
            if game_over:
                # chỉnh ở đây
                if game_over:
                    winner_val = winner(board)
                    if winner_val is None:
                        print("Game Over: Tie.")
                    else:
                        print(f"Game Over: {winner_val} wins.")
                    break;

            else:
                print(f"Player {playr} turn")
                print("Enter the position to move (row,col)")
                i = int(input("Row:"))
                j = int(input("Col:"))
                move_history.append((playr, (i, j)))
                if board[i][j] == EMPTY:
                    board = result(board, (i, j))
                    #! câu 1
                    display_board(board)
                    #! ####################
    #! ####################
    print("Move history:")
    for move in move_history:
        print(f"Player {move[0]} moved at {move[1]}")
    #! câu 4
    d = int(input("Bạn có muốn chơi tiếp không? 1. Có, 2. Không: "))
    while(d == 1):
        #! câu 5
        move_history = []
        n = int(input("Enter the size of the board: "))
        board = initial_state(n)
        x = int(input("Chọn chế độ chơi: 1. Người VS Máy, 2. Người VS Người: "))
        if x == 1:
            ai_turn = False
            print("Choose a player")
            user = input()
            if user == "X":
                ai = "O"
            else:
                ai = "X"
            while True:
                game_over = terminal(board)
                playr = player(board)
                if game_over:
                    # chỉnh ở đây
                    winner_val = winner(board)
                    if winner_val is None:
                        print("Game Over: Tie.")
                    else:
                        print(f"Game Over: {winner_val} wins.")
                    break;
                else:
                    if user != playr and not game_over:
                        if ai_turn:
                            move = minimax(board)
                            board = result(board, move)
                            ai_turn = False
                            #! Câu 1
                            display_board(board)
                            #! ####################
                    elif user == playr and not game_over:
                        ai_turn = True
                        print("Enter the position to move (row,col)")
                        i = int(input("Row:"))
                        j = int(input("Col:"))
                        move_history.append((user, (i, j)))
                        if board[i][j] == EMPTY:
                            board = result(board, (i, j))
                            #! câu 1
                            display_board(board)
                            #! ####################
        #! câu 3
        else:
            user = X
            ai = O
            while True:
                game_over = terminal(board)
                playr = player(board)
                if game_over:
                    # chỉnh ở đây
                    winner_val = winner(board)
                    if winner_val is None:
                        print("Game Over: Tie.")
                    else:
                        print(f"Game Over: {winner_val} wins.")
                    break;
                else:
                    print(f"Player {playr} turn")
                    print("Enter the position to move (row,col)")
                    i = int(input("Row:"))
                    j = int(input("Col:"))
                    move_history.append((playr, (i, j)))
                    if board[i][j] == EMPTY:
                        board = result(board, (i, j))
                        #! câu 1
                        display_board(board)
                        #! ####################
        #! ####################
        print("Move history:")
        for move in move_history:
            print(f"Player {move[0]} moved at {move[1]}")
        d = int(input("Bạn có muốn chơi tiếp không? 1. Có, 2. Không: "))