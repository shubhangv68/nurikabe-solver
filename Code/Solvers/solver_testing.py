from backtracking import solve
import json
import copy
import checkAnswer

def print_board(curr_board, bool_flag):
    """
    Prints curr_board nicely
    """
    if bool_flag:
        for row in curr_board.get("board"):
            msg = "["
            for val in row:
                msg += str(val).rjust(3)
            msg+="]"
            print(msg)
    else:
        for row in curr_board:
            msg = "["
            for val in row:
                msg += str(val).rjust(3)
            msg+="]"
            print(msg)

def testing_backtracking():
    """
    Function for running tests on backtracking
    """
    with open("../Board-Generators/board_database.json") as f:
        data_set = json.load(f)
    f.close()
    for board_size in data_set:
        for board_num in data_set[board_size]:

            if board_num == "board_28" or True:
                curr_board = data_set[board_size][board_num]
                print("\nTesting {} {}".format(board_size, board_num))
                print_board(curr_board, True)
                solved_board = solve(copy.deepcopy(curr_board))
                if solved_board != -1:
                    print("\nSolved!")
                    print_board(solved_board, False)
                else:
                    print("\nA failure occured.")
                    
                # print_2darr_nice(solved_board) if solved_board != -1 else print("failure")
            else:
                pass
        break # only do 5x5 rn for testing

def get_coordinates(board):
    """
    Get the coordinates of numbered cells in the board (seed cells) along with their number
    """
    coordinates = []
    for i in range(len(board)): # row
        for j in range(len(board[0])): # col
            if board[i][j] > 0:
                coordinates.append([j, i, board[i][j]])
    return coordinates

def testing_check_answer():
    """
    Function for testing check_answer
    """
    board_good = [
        [0, 24, 0, 0, 0],
        [0, 0, 0, 0, -1],
        [0, 0, 0, 0, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1]
    ]
    print_board(board_good, False)
    print("(checking connected) Should be {}, is {}".format(True, checkAnswer.check_connected(board_good) ) )

    print("")

    board_bad   = [
        [0, 24, 0, 0, 0],
        [0, 0, 0, 0, -1],
        [0, 0, 0, 0, 0],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1]
    ]
    print_board(board_bad, False)
    print("(checking connected) Should be {}, is {}\n".format(False, checkAnswer.check_connected(board_bad) ) )


    uh_oh_board = [
        [0, 24, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, -1, 0]
    ]
    print(get_coordinates(uh_oh_board))
    print_board(uh_oh_board, False)
    print( checkAnswer.check_board(uh_oh_board, get_coordinates(uh_oh_board)) )

    print("")
    board_2 = [ [3, 0, 0, -1] ]
    print(get_coordinates(board_2))
    print_board(board_2, False)
    print(checkAnswer.check_board(board_2, get_coordinates(board_2)))

def print_board_coords():
    """
    Prints board coordinates in a nice format
    """
    for i in range(5):
        row = ""
        for j in range(5):
            row += "{},{}   ".format( j, i)
        print(row)

if __name__== "__main__": # current state is just for testing purposes
    print("\nThis was a file we used for testing various methods of the solver or constraints")
    print("Feel free to uncomment the following lines of code in main to see, but really they don't do anything exciting\n")
    # testing_backtracking()
    # print("")
    # testing_check_answer()
    # print("")
    # print_board_coords()
