import subprocess # for creating executable
import os # for creating the executable
import sys # for progress bar
import json # creates output file

MIN_BOARD_SIZE = 5
MAX_BOARD_SIZE = 50

MAX_NUM_BOARDS = 1_000

def getBoardSizes() -> list:
    """
    gets the size(s) of the board(s) to make
    from user input, returns a list of them
    """
    # prompt user
    print("\nWhat size boards do you want to make? Please enter either a single size or a range. For example enter: '15' or '7-12'")
    count = 1 # failsafe count
    while True:
        error_code = -1
        sizes = []
        try: # get board size(s)
            user_input = input("Please enter board size(s): ")
            parsed_input = user_input.split("-")

            if len(parsed_input) > 2:
                error_code = 1 # too many input
                cause_error = int('h') # brings us to except

            for elem in parsed_input: # get sizes
                error_code = 2 # set just in case
                sizes.append(int(elem)) # might throw error

            for val in sizes: # valid board sizes
                if val < MIN_BOARD_SIZE:
                    error_code = 3
                    cause_error = int('h')
                if val > MAX_BOARD_SIZE:
                    error_code = 4
                    cause_error = int('h')

            if len(sizes) > 1: # make sure valid range
                if sizes[0] >= sizes[1]:
                    error_code = 5
                    cause_error = int("h")

            break # break out of while if good

        except: # error in board sizes
            if 1 == error_code: # too many input
                error_msg = "Please enter either a single integer or two seperated by a \'-\', e.g. 14, 7, 8, 5-9, 12-17, or 8-13"
            elif 2 == error_code: # input not int
                error_msg = "Please enter a valid integer(s)"
            elif 3 == error_code: # input too small
                error_msg = "Please enter larger board sizes, minimum board size is {}".format(MIN_BOARD_SIZE)
            elif 4 == error_code: # input too large
                error_msg = "Please enter smaller board sizes, maximum board size is {}".format(MAX_BOARD_SIZE)
            elif 5 == error_code: # input not valid range
                error_msg = "Please enter a valid range, smaller board size must come first"
            else:
                error_msg = "Error getting board size"

            print("Error: {}".format(error_msg)) # print error message

        finally: # 5 chances to get it
            if count >= 5:
                print("Failed to get board size(s)...")
                print("Exiting program...")
                exit() # failsafe
            count += 1

    # now have either like [15] or [7, 12]
    if len(sizes) == 1:
        return sizes
    else:
        # turn [7, 12] into [7, 8, 9, 10, 11, 12]
        return list(range(sizes[0], sizes[1] + 1))

def getNumberOfBoards() -> int:
    """
    gets how many of each size board to make
    from user input
    """
    """
    Bug where the generator makes multiple boards, this forces it to be only 1 board
    """
    return 1
    
    # prompt user
    print("\nHow many board(s) of each size do you want to make")
    # get input, quite if failed 5 times
    count = 1
    while True:
        error_code = 1
        try:
            user_input = input("Please enter an integer: ")
            num_boards = int(user_input) # attempt to convert to int, this is where error can happen
            if num_boards < 1:
                error_code = 2
            if num_boards > MAX_NUM_BOARDS:
                error_code = 3
            break # break out of loop if good
        except:
            if 1 == error_code:
                error_msg = "Please enter a valid integer."
            elif 2 == error_code:
                error_msg = "Please enter a positive integer"
            elif 3 == error_code:
                error_msg = "Please enter a SMALLER number of boards, the max number of boards is {}".format(MAX_NUM_BOARDS)
            else:
                error_msg = "Error getting number of boards"
            print("Error: {}".format(error_msg))
        finally:
            # check to see if still under 5 times, this is just a safety net
            if count >= 5:
                print("Failed to get how many boards to make...")
                print("Exiting program...")
                exit() # failsafe
            count += 1

    return num_boards

def drawProgressBar(msg:str, percent:float, barLen = 20) -> None:
    """
    makes a progress bar (fun!)
    Source for only this method: https://stackoverflow.com/questions/3002085/how-to-print-out-status-bar-and-percentage
    """
    sys.stdout.write("\r")
    sys.stdout.write("{} [{:<{}}] {:.0f}%".format(msg, "#" * int(barLen * percent), barLen, percent * 100))
    sys.stdout.flush()

def makeBoardGeneratorExecutable() -> None:
    """
    Creates the board generator program
    """
    print("Compiling generator executable")
    os.chdir('generator') # Change directory to 'generator'
    
    # Compile the C++ code
    """
    this works for me on a mac/linux based, idk if it works for windows ?
    """
    compile_command = ["g++", "-w", "getPuzzle.cpp", "generator.cpp", "-o", "puzzle_generator"]
    compile_result = subprocess.run(compile_command, capture_output=True, text=True)
    if compile_result.returncode == 0:
        print("Compilation successful.")
    else:
        print("Error compiling the code:")
        print(compile_result.stderr)
        exit() # uh oh
    os.chdir("..") # change back to og directory
    
def createAllBoards(board_sizes: list, num_boards: int) -> None:
    """
    Brains of creating the boards, for each size of board the function
    creates num_boards number of those

    Input: board sizes in a list, number of boards
    Output: None, but does create a file of the boards created
    """
    print("\nCreating {} board(s) of size(s) {}".format(num_boards, board_sizes))

    makeBoardGeneratorExecutable()

    os.chdir("generator")

    all_boards = dict({})

    for size in board_sizes:
        board_size = "{}x{}".format(size, size)
        print("\nCreating {} boards...".format(board_size))
        generated_boards = []
        for i in range(1, num_boards + 1):
            msg = "Creating board number {}".format(i)
            drawProgressBar(msg, i / (num_boards))

            # create the board
            run_command = ["./puzzle_generator", "{}".format(size), "{}".format(size)]
            run_result = subprocess.run(run_command, capture_output=True, text=True)
            if run_result.returncode == 0:
                # good
                # print("Program executed successfully.")
                board = run_result.stdout.split(" ")
                board_with_spaces = []
                print("\n", board, "\n") # add spaces
                for row in board:
                    new_row = []
                    # print(row.split(","))
                    for num_str in row.split(","):
                        if num_str != "":
                            new_row.append(int(num_str))
                    # print(new_row)
                    # print("Here")
                    if new_row != []:
                        # print("added")
                        board_with_spaces.append(new_row)
                # print("Output:")
                # print(run_result.stdout)
                generated_boards.append(board_with_spaces)
            else:
                # bad bad bad bad bad bad
                print("error creating board {} of {} for size {}x{}".format(i, num_boards, size, size))
                print("Error executing the program:")
                print(run_result.stderr)
                print("aborting program...")
                exit()
        temp = {}
        for num, board in enumerate(generated_boards):
            temp.update({"board_{}".format(num+1) : board})
        all_boards.update({board_size : temp})
        print("") # new line
    
    # remove executable
    run_command = ["rm", "puzzle_generator"]
    # run_result = subprocess.run(run_command, capture_output=True, text=True)
    if run_result.returncode == 0:
        # good
        pass
    else:
        # bad
        print("Feel free to remove the executable in the generator directory (\"rm puzzle_generator\")")

    os.chdir("..")
    print("\n\nWriting to file...")

    with open('boards.json', 'w') as board_file: 
        board_file.write(json.dumps(all_boards, indent=3))



if __name__== "__main__":
    
    # get puzzle sizes
    puzzle_sizes = getBoardSizes()
    # get how many of each size to me
    num_puzzles = getNumberOfBoards()

    # print(puzzle_sizes, num_puzzles)
    # create puzzles of those sizes
    createAllBoards(puzzle_sizes, num_puzzles)