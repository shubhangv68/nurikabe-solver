import subprocess # for creating executable
import os # for creating the executable
import sys # for progress bar
import json # creates output file
import jsbeautifier # makes it pretty
import copy

MIN_BOARD_SIZE = 5
MAX_BOARD_SIZE = 25
BOARDS_PER_SIZE = 30
COMPILE_COMMAND = ["g++", "-w", "getPuzzle.cpp", "generator.cpp", "-o", "puzzle_generator"]
REMOVE_COMMAND = ["rm", "puzzle_generator"]
DATABASE_NAME = "board_database.json"

class error_handler():
    """
    will run for a while, want to make sure errors are logged
    if any occur instead of them crashing program
    """
    def __init__(self) -> None:
        if os.path.exists("errors.txt"):
            subprocess.run(["rm", "errors.txt"], capture_output=True, text=True)
        self.messages = []

    def log(self, msg:str) -> None:
        self.messages.append(msg)

    def to_file(self) -> None:
        if len(self.messages) == 0:
            print("\n\nNo errors recorded.\n")
        else:
            print("Recording errors in 'errors.txt'")
            with open("errors.txt", "w") as err_file:
                for msg in self.messages:
                    err_file.write(f"{msg}\n")
            err_file.close()

# good to be proactive w/ errors
global_logger = error_handler()

def confirm_with_user() -> bool:
    """
    Confirms with user that they are
    okay with running this program
    """
    print("\nWARNING:")
    print("Will take a WHILE to run, please confirm you want to run this")
    user_input = input("Please Confirm with y or n: ")
    return user_input == "y"

def draw_progress_bar(msg:str, percent:float, bar_len = 20) -> None:
    """
    makes a progress bar (fun!)
    Source for only this method: https://stackoverflow.com/questions/3002085/how-to-print-out-status-bar-and-percentage
    """
    sys.stdout.write("\r")
    sys.stdout.write("{} [{:<{}}] {:.0f}%".format(msg, "#" * int(bar_len * percent), bar_len, percent * 100))
    sys.stdout.flush()

def create_board_generator_executable() -> int:
    """
    Creates the board generator program

    input: None
    output: 
        - 0 or 1 with 0 representing successful compilation
        - changes the directory to be within "generator" if successful compilation

    generator has been modified from: https://github.com/Malorn44/NurikabeMaker
    """
    # Compile the C++ code
    """
    this works for me on a mac/linux based, idk if it works for windows ?
    """
    try:
        os.chdir("generator")
        compile_result = subprocess.run(COMPILE_COMMAND, capture_output=True, text=True)
    except FileNotFoundError:
        global_logger.log(FileNotFoundError)
        return 1
    except Exception as e:
        global_logger.log(e)
        os.chdir("..")
        return 1
    
    if compile_result.returncode == 0:
        return 0
    else:
        global_logger.log(compile_result.stderr)
        os.chdir("..")
        return 1

def delete_board_generator_executable() -> int:
    """
    Creates the board generator program

    input: None
    output: 
        - 0 or 1 with 0 representing successful deletion
        - changes the directory to be parent dir of "generator"
    """
    is_one = False
    try:
        compile_result = subprocess.run(REMOVE_COMMAND, capture_output=True, text=True)
    except Exception as e:
        global_logger.log(e)
        is_one = True

    try: 
        os.chdir("..")
    except Exception as e:
        global_logger.log(e)
        is_one = True

    if compile_result.returncode == 0:
        return 0 if not is_one else 1
    else:
        global_logger.log(compile_result.stderr)
        return 1

def get_database_data() -> dict:
    """
    gets and returns the current database data from: board_database.json
    """
    try:
        if os.path.exists(DATABASE_NAME):
            with open(DATABASE_NAME) as db_file:
                data = json.load(db_file)
            db_file.close()
            return data
        else:
            return dict({})
    except Exception as e:
        global_logger.log("Reading in current database, {}".format(e))
        return dict({})

def get_coordinates(board : list) -> list:
    """
    input: a single board (a 2d list)
    output: a 2d list of the form [[(x, y), num] , ... , [(x, y), num] ]
    """
    coords = []
    for y, x_list in enumerate(board):
        for x, val in enumerate(x_list):
            if int(val) > 0:
                coords.append( tuple((x, y, board[y][x] ) ) )
    return coords

def update_database_data(current_db_data:dict, generated_boards:dict, board_num : int) -> json:
    """
    input: current data in database, new boards, board_num is which board num is it
    output: combined of the above two
    """
    try:
        if not current_db_data:
            # only if first time (its empty)
            for key in generated_boards:
                new_board = generated_boards.get(key)
                current_db_data.update({
                    key : { 
                        "board_{}".format(board_num) : {
                            "board" : new_board ,
                            "coordinates" : get_coordinates(new_board)
                        }
                    } 
                })
        else:
            for key in generated_boards:
                curr_boards = current_db_data.get(key)
                new_board = generated_boards.get(key) 
                curr_boards.update({
                    "board_{}".format(board_num) : {
                        "board" : new_board ,
                        "coordinates" : get_coordinates(new_board)
                        }
                    })
                current_db_data.update({key : curr_boards})

        return current_db_data
    
    except Exception as e:
        global_logger.log("Error combining {}".format(e))
        return current_db_data

def save_updated_database( database_data : dict) -> None:
    """
    input: updated database
    output: None but does save to a json file
    """
    with open(DATABASE_NAME, "w") as db_file:
        options = jsbeautifier.default_options()
        options.indent_size = 3
        db_file.write( jsbeautifier.beautify( json.dumps(database_data), options ) )

def create_database() -> None:
    """
    Creates the database in the form of a json
        called "board_database.json"

    At each board size updates database json to
        help with data protection in case of crash
    """
    print("\nStartings database creation; {} boards each for size {}x{} to {}x{}".format(BOARDS_PER_SIZE, MIN_BOARD_SIZE, MIN_BOARD_SIZE, MAX_BOARD_SIZE, MAX_BOARD_SIZE))
    total_num_boards = (((MAX_BOARD_SIZE - MIN_BOARD_SIZE)+1) ** 2) * BOARDS_PER_SIZE
    created_boards = 0
    all_boards = dict({})
    for b_num in range(1, BOARDS_PER_SIZE + 1):

        # make generator and changes dir into generator
        code = create_board_generator_executable()
        if code != 0:
            global_logger.log("error with board number {}, skipping".format(b_num))
            continue # skip to next iteration

        generated_boards = dict({})

        for x in range(MIN_BOARD_SIZE, MAX_BOARD_SIZE + 1):
            for y in range(MIN_BOARD_SIZE, MAX_BOARD_SIZE + 1):
                created_boards += 1
                draw_progress_bar(
                    "Creating {}x{} board number {}/{}, total board: {}/{}".format(
                        str(x).rjust(2), str(y).ljust(2), str(b_num).rjust(2), BOARDS_PER_SIZE, 
                        str(created_boards).rjust(len(str(total_num_boards))), total_num_boards
                    ), created_boards / total_num_boards
                )
                
                try:
                    run_command = ["./puzzle_generator", str(x), str(y)]
                    run_result = subprocess.run(run_command, capture_output=True, text=True)
                except Exception as e:
                    global_logger.log("error with {}x{} board number {}, {},skipping".format(
                        x, y, b_num, e
                    ))
                    continue

                if run_result.returncode == 0:
                    board = []
                    for og_row in run_result.stdout.split(" "):
                        row = []
                        for idx in og_row.split(","):
                            if idx != "":
                                row.append( int(idx) )
                        if row != []:
                            board.append(row)

                    generated_boards.update({ "{}x{}".format(x, y) : board })
                else:
                    global_logger.log("error with {}x{} board number {}, {},skipping".format(
                        x, y, b_num, run_result.stderr
                    ))

        # remove generator and back into parent directory
        delete_board_generator_executable()

        # current_db_data = get_database_data()
        # updated_db_data = update_database_data(current_db_data, generated_boards, b_num)
        # save_updated_database(updated_db_data)
        if b_num == 1:
            current_db_data = {}
        else:
            current_db_data = all_boards
        all_boards = update_database_data(current_db_data, generated_boards, b_num)
    save_updated_database(all_boards)
    print("\n\nDatabase Creation Successful.\n")

if __name__ == "__main__":
    # confirm they want to run
    confirmation = confirm_with_user()
    if not confirmation:
        print("Exiting...")
        exit(0)
    
    # good to go
    create_database()

    # make sure errors are recorded
    global_logger.to_file()