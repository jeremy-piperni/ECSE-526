import numpy as np

board = np.array([['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x'],
                  ['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x'],['x','x','x','x','x','x','x','x']])
is_white = True
depth = 3
game_won = False

def get_valid_moves():
    valid_moves = []
    for col in range(8):
        if valid_row(col) != 0:
            valid_moves.append("D " + str(col + 1))
    if is_white:
        runsOfThree = runs_of_three("white")
        runsOfTwo = runs_of_two("white")
    else:
        runsOfThree = runs_of_three("black")
        runsOfTwo = runs_of_two("black")
    if runsOfThree:
        check_shifts(runsOfThree, valid_moves)
    if runsOfTwo:
        check_shifts(runsOfTwo, valid_moves)
    return valid_moves

def valid_row(col):
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

def print_board():
        for row in board:
            for val in row:
                print(val, end = ",")
            print() 

def drop_piece(col):
    col = int(col)
    row = valid_row(col)
    if is_white:
        board[row - 1][col] = '0'
    else:
        board[row - 1][col] = '1'

def read_move(string):
    valid_moves = get_valid_moves()
    if string in valid_moves:    
        split = string.split(" ")
        split[1] = str(int(split[1]) - 1)
        if split[0] == 'D':
            drop_piece(split[1])
        elif split[0] == 'L':
            split[2] = str(int(split[2]) - 1)
            shift_left(split[1], split[2])
        elif split[0] == 'R':
            split[2] = str(int(split[2]) - 1)
            shift_right(split[1], split[2])
    else:
        print("Move is not valid")

def is_winning_move(color):
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

def runs_of_three(color):
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

def runs_of_two(color):
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

def check_shifts(runs, valid_moves):
    for run in runs:
        if run[0][0] != 1:
            if is_white:
                if board[run[0][1] - 1][run[0][0] - 2] == '1':
                    if run[0][0] == 2 or board[run[0][1] - 1][run[0][0] - 3] == 'x':
                        valid_moves.append("L " + str(run[1][0]) + " " + str(run[1][1]))
            else:
                if board[run[0][1] - 1][run[0][0] - 2] == '0':
                    if run[0][0] == 2 or board[run[0][1] - 1][run[0][0] - 3] == 'x':
                        valid_moves.append("L " + str(run[1][0]) + " " + str(run[1][1]))
        if run[1][0] != 8:
            if is_white:
                if board[run[1][1] - 1][run[1][0]] == '1':
                    if run[1][0] == 7 or board[run[1][1] - 1][run[1][0] + 1] == 'x':
                        valid_moves.append("R " + str(run[0][0]) + " " + str(run[0][1]))
            else:
                if board[run[1][1] - 1][run[1][0]] == '0':
                    if run[1][0] == 7 or board[run[1][1] - 1][run[1][0] + 1] == 'x':
                        valid_moves.append("R " + str(run[0][0]) + " " + str(run[0][1]))
    return valid_moves

def fill_column(row, col):
    if board[row][col] == 'x':
        cur_row = row
        while cur_row > 0:
            board[cur_row][col] = board[cur_row - 1][col]
            cur_row = cur_row - 1
        if valid_row(col) < row:
            fill_column(row, col)


def shift_left(col, row):
    col = int(col)
    row = int(row)
    if is_white:
        color = '0'
        opp_color = '1'
    else:
        color = '1'
        opp_color = '0'

    if col - 2 >= 0:
        bot_row2 = valid_row(col - 3) - 1
    if col - 3 >= 0:
        bot_row3 = valid_row(col - 4) - 1
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
                fill_column(bot_row2, col - 3)
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
                fill_column(bot_row3, col - 4)
    fill_column(row, col)

def shift_right(col, row):
    col = int(col)
    row = int(row)
    if is_white:
        color = '0'
        opp_color = '1'
    else:
        color = '1'
        opp_color = '0'

    if col + 2 <= 7:
        bot_row2 = valid_row(col + 2) - 1
    if col + 3 <= 7:
        bot_row3 = valid_row(col + 3) - 1
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
                fill_column(bot_row2, col + 3)
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
                fill_column(bot_row3, col + 4)
    fill_column(row, col)

while (game_won == False):
    print(get_valid_moves())
    user_input = input("Enter move: ")
    read_move(user_input)
    print_board()
    if is_white:
        color = "white"
    else:
        color = "black"
    winning_runs = is_winning_move(color)
    runsOfThree = runs_of_three(color)
    runsOfTwo = runs_of_two(color)
    if winning_runs:
        print(winning_runs)
        game_won = True
    else:
        is_white = not is_white
    

