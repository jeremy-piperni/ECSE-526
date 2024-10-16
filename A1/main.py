import numpy as np
import socket

# Variables that can be changed by the user
connect_to_server = True
game_id = "12345"
playing_color = "white"
TCP_IP = "156trlinux-1.ece.mcgill.ca"
TCP_PORT = 12345
AI_vs_AI = True
depth = 5

# Variables that should not be changed by the user
playing_board = np.array([['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x'],
                  ['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x']])
is_white = True
game_won = False
BUFFER_SIZE = 1024

# get the valid moves on the board for a given color
def get_valid_moves(board, color):
    valid_moves = []
    drop_order = [3,4,2,5,1,6,0,7]
    if color == "white":
        runsOfThree = runs_of_three_hor(board, "white")
        runsOfTwo = runs_of_two_hor(board, "white")
    else:
        runsOfThree = runs_of_three_hor(board, "black")
        runsOfTwo = runs_of_two_hor(board, "black")
    if runsOfThree:
        check_shifts(board, runsOfThree, valid_moves, color)
    if runsOfTwo:
        check_shifts(board, runsOfTwo, valid_moves, color)
    for col in drop_order:
        if valid_row(board, col) != 0:
            valid_moves.append("D " + str(col + 1))
    return valid_moves

# find what row is empty in a given col
def valid_row(board, col):
    if board[7][col] == "x":
        return 8
    elif board[6][col] == "x":
        return 7
    elif board[5][col] == "x":
        return 6
    elif board[4][col] == "x":
        return 5
    elif board[3][col] == "x":
        return 4
    elif board[2][col] == "x":
        return 3
    elif board[1][col] == "x":
        return 2
    elif board[0][col] == "x":
        return 1
    else:
        return 0

# check if cells above a certain col,row is empty
def is_above_empty(board, row, col):
    is_empty = True
    for i in range(row):
        if board[i][col] != "x":
            is_empty = False
    return is_empty

# print out the playing board
def print_board(board):
        for row in board:
            for val in row:
                print(val, end = ",")
            print() 

# drop a piece in the given column
def drop_piece(board, col, color):
    col = int(col)
    row = valid_row(board, col)
    if color == "white":
        board[row - 1][col] = '0'
    else:
        board[row - 1][col] = '1'

# reads the move that was given by the AI, player, or server
def read_move(board, string, color):
    valid_moves = get_valid_moves(board, color)
    if string in valid_moves:    
        split = string.split(" ")
        split[1] = str(int(split[1]) - 1)
        if split[0] == 'D':
            drop_piece(board, split[1], color)
        elif split[0] == 'L':
            split[2] = str(int(split[2]) - 1)
            shift_left(board, split[1], split[2], color)
        elif split[0] == 'R':
            split[2] = str(int(split[2]) - 1)
            shift_right(board, split[1], split[2], color)
    else:
        print("Move is not valid")

# check if there are any winning moves for a given color
def is_winning_move(board, color):
    winning_runs = []
    if color == "white":
        piece = '0'
    else:
        piece = '1'
    # Check horizontal winning runs
    for col in range(5):
        for row in range(8):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][col + 3] == piece:
                winning_runs.append([[col + 1, row + 1], [col + 4, row + 1]])
    # Check vertical winning runs            
    for col in range(8):
        for row in range(5):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + 3][col] == piece:
                winning_runs.append([[col + 1, row + 1], [col + 1, row + 4]])
    # Check positive diagonal winning runs
    for col in range(5):
        for row in range(5):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece:
                winning_runs.append([[col + 1, row + 1], [col + 4, row + 4]])
    # Check negative diagonal winning runs
    for col in range(5):
        for row in range(3, 8):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece:
                winning_runs.append([[col + 1, row + 1], [col + 4, row - 2]])

    return winning_runs

# check horizontal runs of threes for a given color
def runs_of_three_hor(board, color):
    runs_of_three = []
    if color == "white":
        piece = '0'
    else:
        piece = '1'
    # Check horizontal runs
    for col in range(6):
        for row in range(8):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece:
                runs_of_three.append([[col + 1, row + 1], [col + 3, row + 1]])
                
    return runs_of_three

# check runs of threes for a given color
def runs_of_three(board, color):
    runs_of_three = []
    if color == "white":
        piece = '0'
    else:
        piece = '1'
    # Check horizontal runs of three
    for col in range(6):
        for row in range(8):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece:
                runs_of_three.append([[col + 1, row + 1], [col + 3, row + 1]])
    # Check vertical runs of three            
    for col in range(8):
        for row in range(6):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece:
                runs_of_three.append([[col + 1, row + 1], [col + 1, row + 3]])
    # Check positive diagonal runs of three
    for col in range(6):
        for row in range(6):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece:
                runs_of_three.append([[col + 1, row + 1], [col + 3, row + 3]])
    # Check negative diagonal runs of three
    for col in range(6):
        for row in range(2, 8):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece:
                runs_of_three.append([[col + 1, row + 1], [col + 3, row - 1]])

    return runs_of_three

# check horizontal runs of twos for a given color
def runs_of_two_hor(board, color):
    runs_of_two = []
    if color == "white":
        piece = '0'
    else:
        piece = '1'
    # Check horizontal runs
    for col in range(7):
        for row in range(8):
            if board[row][col] == piece and board[row][col + 1] == piece:
                runs_of_two.append([[col + 1, row + 1], [col + 2, row + 1]])
                
    return runs_of_two

# check runs of twos for a given color
def runs_of_two(board, color):
    runs_of_two = []
    if color == "white":
        piece = '0'
    else:
        piece = '1'
    # Check horizontal runs of two
    for col in range(7):
        for row in range(8):
            if board[row][col] == piece and board[row][col + 1] == piece:
                runs_of_two.append([[col + 1, row + 1], [col + 2, row + 1]])
    # Check vertical runs of two           
    for col in range(8):
        for row in range(7):
            if board[row][col] == piece and board[row + 1][col] == piece:
                runs_of_two.append([[col + 1, row + 1], [col + 1, row + 2]])
    # Check positive diagonal runs of two
    for col in range(7):
        for row in range(7):
            if board[row][col] == piece and board[row + 1][col + 1] == piece:
                runs_of_two.append([[col + 1, row + 1], [col + 2, row + 2]])
    # Check negative diagonal runs of two
    for col in range(7):
        for row in range(1, 8):
            if board[row][col] == piece and board[row - 1][col + 1] == piece:
                runs_of_two.append([[col + 1, row + 1], [col + 2, row]])

    return runs_of_two

# check what shifts are possible for a given color
def check_shifts(board, runs, valid_moves, color):
    for run in runs:
        if run[0][0] != 1:
            if color == "white":
                if board[run[0][1] - 1][run[0][0] - 2] == '1':
                    if run[0][0] == 2 or board[run[0][1] - 1][run[0][0] - 3] == 'x':
                        valid_moves.append("L " + str(run[1][0]) + " " + str(run[1][1]))
            else:
                if board[run[0][1] - 1][run[0][0] - 2] == '0':
                    if run[0][0] == 2 or board[run[0][1] - 1][run[0][0] - 3] == 'x':
                        valid_moves.append("L " + str(run[1][0]) + " " + str(run[1][1]))
        if run[1][0] != 8:
            if color == "white":
                if board[run[1][1] - 1][run[1][0]] == '1':
                    if run[1][0] == 7 or board[run[1][1] - 1][run[1][0] + 1] == 'x':
                        valid_moves.append("R " + str(run[0][0]) + " " + str(run[0][1]))
            else:
                if board[run[1][1] - 1][run[1][0]] == '0':
                    if run[1][0] == 7 or board[run[1][1] - 1][run[1][0] + 1] == 'x':
                        valid_moves.append("R " + str(run[0][0]) + " " + str(run[0][1]))
    return valid_moves

# fill the current column, when a shift occured
def fill_column(board, row, col):
    if board[row][col] == 'x':
        cur_row = row
        while cur_row > 0:
            board[cur_row][col] = board[cur_row - 1][col]
            cur_row = cur_row - 1
        if not is_above_empty(board, row, col):
            fill_column(board, row, col)

# Shift a run left
def shift_left(board, col, row, main_color):
    col = int(col)
    row = int(row)
    if main_color == "white":
        color = '0'
        opp_color = '1'
    else:
        color = '1'
        opp_color = '0'

    if col - 2 >= 0:
        bot_row2 = valid_row(board, col - 3) - 1
    if col - 3 >= 0:
        bot_row3 = valid_row(board, col - 4) - 1
    if board[row][col - 2] == opp_color:
        if col - 2 == 0:
            board[row][col - 2] = color
            board[row][col - 1] = color
            board[row][col] = 'x'
        else:
            board[row][col - 3] = opp_color
            board[row][col - 2] = color
            board[row][col - 1] = color
            board[row][col] = 'x'
            if row != 7:
                fill_column(board, bot_row2, col - 3)
    else:
        if col - 3 == 0:
            board[row][col - 3] = color
            board[row][col - 2] = color
            board[row][col - 1] = color
            board[row][col] = 'x'
        else:
            board[row][col - 4] = opp_color
            board[row][col - 3] = color
            board[row][col - 2] = color
            board[row][col - 1] = color
            board[row][col] = 'x'
            if row != 7:
                fill_column(board, bot_row3, col - 4)
    fill_column(board, row, col)

# Shift a run right
def shift_right(board, col, row, main_color):
    col = int(col)
    row = int(row)
    if main_color == "white":
        color = '0'
        opp_color = '1'
    else:
        color = '1'
        opp_color = '0'

    if col + 2 < 7:
        bot_row2 = valid_row(board, col + 3) - 1
    if col + 3 < 7:
        bot_row3 = valid_row(board, col + 4) - 1
    if board[row][col + 2] == opp_color:
        if col + 2 == 7:
            board[row][col + 2] = color
            board[row][col + 1] = color
            board[row][col] = 'x'
        else:
            board[row][col + 3] = opp_color
            board[row][col + 2] = color
            board[row][col + 1] = color
            board[row][col] = 'x'
            if row != 7:
                fill_column(board, bot_row2, col + 3)
    else:
        if col + 3 == 7:
            board[row][col + 3] = color
            board[row][col + 2] = color
            board[row][col + 1] = color
            board[row][col] = 'x'
        else:
            board[row][col + 4] = opp_color
            board[row][col + 3] = color
            board[row][col + 2] = color
            board[row][col + 1] = color
            board[row][col] = 'x'
            if row != 7:
                fill_column(board, bot_row3, col + 4)
    fill_column(board, row, col)

# score a non terminal node for minimax
def score_function(board, color, type):
    if type == "old":
        white = len(runs_of_three(board,"white")) + len(runs_of_two(board,"white"))
        black = len(runs_of_three(board,"black")) + len(runs_of_two(board,"black"))
        if color == "white":
            score = white - black
        else:
            score = black - white
        return score
    else:
        if color == "white":
            white3s = len(runs_of_three(board,"white"))
            white2s = len(runs_of_two(board,"white"))
            white2shor = len(runs_of_two_hor(board, "white"))
            score = (3 * white3s) + white2shor + white2s
        else:
            black3s = len(runs_of_three(board,"black"))
            black2s = len(runs_of_two(board,"black"))
            black2shor = len(runs_of_two_hor(board, "black"))
            white3s = len(runs_of_three(board,"white"))
            score = (3 * black3s) + black2shor + black2s - (3 * white3s)
        return score

# Minimax algorithm
def minimax(board, cur_depth, max_depth, max_player, type):
    if is_white:
        color = "white"
        opp_color = "black"
    else:
        color = "black"
        opp_color = "white"
    white_win_moves = is_winning_move(board, "white")
    black_win_moves = is_winning_move(board, "black")
    if is_white and not max_player:
        winRatio = len(white_win_moves) - len(black_win_moves)
    elif not is_white and not max_player:
        winRatio = len(black_win_moves) - len(white_win_moves)
    elif is_white and max_player:
        winRatio = len(white_win_moves) - len(black_win_moves)
    elif not is_white and max_player:
        winRatio = len(black_win_moves) - len(white_win_moves)
    if winRatio > 0:
        return (None, 999999)
    if winRatio < 0:
        return (None, -999999)

    if cur_depth == max_depth:
        if is_white and not max_player:
            return (None, score_function(board, "white", type))
        elif is_white and max_player:
            return (None, score_function(board, "black", type))
        elif not is_white and not max_player:
            return (None, score_function(board, "black", type))
        elif not is_white and max_player:
            return (None, score_function(board, "white", type))

    if max_player:
        value = -999999
        validMoves = get_valid_moves(board, color)
        maxMove = validMoves[0]
        for move in validMoves:
            board_copy = board.copy()
            read_move(board_copy, move, color)
            new_score = minimax(board_copy, cur_depth + 1, max_depth, False, type)[1]
            if new_score > value:
                value = new_score
                maxMove = move
        return (maxMove, value)
    else:
        value = 999999
        validMoves = get_valid_moves(board, opp_color)
        minMove = validMoves[0]
        for move in validMoves:
            board_copy = board.copy()
            read_move(board_copy, move, opp_color)
            new_score = minimax(board_copy, cur_depth + 1, max_depth, True, type)[1]
            if new_score < value:
                value = new_score
                minMove = move
        return (minMove, value)

# minimax algorithm with alpha-beta pruning
def minimax_alpha_beta(board, cur_depth, max_depth, max_player, alpha, beta, type):
    if is_white:
        color = "white"
        opp_color = "black"
    else:
        color = "black"
        opp_color = "white"
    white_win_moves = is_winning_move(board, "white")
    black_win_moves = is_winning_move(board, "black")
    if is_white and not max_player:
        winRatio = len(white_win_moves) - len(black_win_moves)
    elif not is_white and not max_player:
        winRatio = len(black_win_moves) - len(white_win_moves)
    elif is_white and max_player:
        winRatio = len(white_win_moves) - len(black_win_moves)
    elif not is_white and max_player:
        winRatio = len(black_win_moves) - len(white_win_moves)
    if winRatio > 0:
        return (None, 999999)
    if winRatio < 0:
        return (None, -999999)

    if cur_depth == max_depth:
        if is_white and not max_player:
            return (None, score_function(board, "white", type))
        elif is_white and max_player:
            return (None, score_function(board, "black", type))
        elif not is_white and not max_player:
            return (None, score_function(board, "black", type))
        elif not is_white and max_player:
            return (None, score_function(board, "white", type))

    if max_player:
        value = -999998
        validMoves = get_valid_moves(board, color)
        maxMove = validMoves[0]
        for move in validMoves:
            board_copy = board.copy()
            read_move(board_copy, move, color)
            new_score = minimax_alpha_beta(board_copy, cur_depth + 1, max_depth, False, alpha, beta, type)[1]
            if new_score > value:
                value = new_score
                maxMove = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (maxMove, value)
    else:
        value = 999998
        validMoves = get_valid_moves(board, opp_color)
        minMove = validMoves[0]
        for move in validMoves:
            board_copy = board.copy()
            read_move(board_copy, move, opp_color)
            new_score = minimax_alpha_beta(board_copy, cur_depth + 1, max_depth, True, alpha, beta, type)[1]
            if new_score < value:
                value = new_score
                minMove = move
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (minMove, value)

# main function
if connect_to_server:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Connected")
    except Exception as e:
        print("something wrong")
    s.send((game_id + " " + playing_color).encode())

    while (game_won == False):
        if playing_color == "white":
            minimax_result = minimax_alpha_beta(playing_board, 0, depth, True, -999999, 999999, "new")
            user_output = minimax_result[0]
            print(user_output)
            s.send(user_output.encode())
            read_move(playing_board, user_output, "white")
            print_board(playing_board)
            is_white = False
            data = s.recv(BUFFER_SIZE).decode()
            read_move(playing_board, data, "black")
            is_white = True
            print_board(playing_board)
        else:
            data = s.recv(BUFFER_SIZE).decode()
            read_move(playing_board, data, "white")
            print_board(playing_board)
            is_white = False
            minimax_result = minimax_alpha_beta(playing_board, 0, depth, True, -999999, 999999, "new")
            user_output = minimax_result[0]
            s.send(user_output.encode())
            read_move(playing_board, user_output, "black")
            print_board(playing_board)
            is_white = True
    
    s.close()
else:
    while (game_won == False):
        if playing_color == "white":
            if is_white:
                minimax_result = minimax_alpha_beta(playing_board, 0, depth, True, -999998, 999998, "new")
                user_input = minimax_result[0]
            else:
                if AI_vs_AI:
                    minimax_result = minimax_alpha_beta(playing_board, 0, depth, True, -999998, 999998, "new")
                    user_input = minimax_result[0]
                else:
                    user_input = input("Enter move: ")
                
        else:
            if is_white:
                if AI_vs_AI:
                    minimax_result = minimax_alpha_beta(playing_board, 0, depth, True, -999998, 999998, "new")
                    user_input = minimax_result[0]
                else:
                    user_input = input("Enter move: ")
            else:
                minimax_result = minimax_alpha_beta(playing_board, 0, depth, True, -999998, 999998, "new")
                user_input = minimax_result[0]

        print(user_input)
        if is_white:
            read_move(playing_board, user_input, "white")
        else:
            read_move(playing_board, user_input, "black")
        print_board(playing_board)
        if is_white:
            color = "white"
        else:
            color = "black"
        winning_runs = is_winning_move(playing_board, color)

        if winning_runs:
            game_won = True
            if color == "white" and len(winning_runs) > 0:
                print("White wins!")
            elif color == "white" and len(winning_runs) < 0:
                print("Black wins!")
            elif color == "black" and len(winning_runs) > 0:
                print("Black wins!")
            elif color == "black" and len(winning_runs) < 0:
                print("White wins!")
            else:
                print("Draw!")
        else:
            is_white = not is_white


