import timeit # used for timing how long it takes to solve a board
import json # reading in data
import matplotlib.pyplot as plt # graphing the test results
# import statistics
import numpy as np

"""Use this for importing solver functions"""
import sys
import os
import time
import signal
import copy
sys.path.append('../Solvers')

from backtracking import solve, solve_NO_inference
from inference import inference_at_start
# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
# print("current is: {}, parent is: {}".format(current_dir, parent_dir))
# Add the parent directory to the beginning of sys.path
sys.path.insert(1, parent_dir) # 1 instead of 0 so it checks parent dir after current dir
# Now you can import modules from within "Code" directory

from Board_Generators.DatabaseMaker import draw_progress_bar
# from ..Board_Generators.DatabaseMaker import get_database_data

MAX_NUM_TILES = 150
MAX_TIME = 1 # 1 second max for a board to solve

def read_in_test_database() -> dict | None:
    """
    Reads in the database
    input: None
    output: Database as a dict or None
    """
    try:
        path_to_db = "test_db.json"
        if os.path.exists(path_to_db):
            print("Reading in the test database of boards...")
            with open(path_to_db) as db_file:
                data = json.load(db_file)
            db_file.close()
            return data
        else:
            print("Error: Path to database does not exist {}".format(path_to_db))
            return dict({})
    except Exception as e:
        print("Error: {}: From Reading in database.".format(e))
        return None
    
def read_in_database() -> dict | None:
    """
    Reads in the database
    input: None
    output: Database as a dict or None
    """
    try:
        path_to_db = "../Board_Generators/board_database.json"
        if os.path.exists(path_to_db):
            print("Reading in the database of boards...")
            with open(path_to_db) as db_file:
                data = json.load(db_file)
            db_file.close()
            return data
        else:
            print("Error: Path to database does not exist {}".format(path_to_db))
            return dict({})
    except Exception as e:
        print("Error: {}: From Reading in database.".format(e))
        return None

def get_number_of_boards(data: dict) -> int:
    """
    input: boards in the same format as the database of boards
    output: int of how many boards there are in the data
    """
    # using try/except bc the data could be large and maybe error
    try:
        num = 0
        for board_size in data:
            num += len(data.get(board_size).keys())
        return num
    except Exception as e:
        print("Error: Could not find how many boards there are; {}".format(e))
        return 0

def get_number_of_tiles(board_size:str) -> int:
    """
    input: the board size, i.e. "5x5" or "25x17"
    output: integer of how many tiles there are in a board of the given size
    """
    split_str = board_size.split("x")
    # print(split_str)
    return int(split_str[0]) * int(split_str[1])

def make_graph(file_name:str, title:str, x_label:str, y_label:str, x_values:list , y_values:list) -> None:
    """
    Makes a graph based on the input
    Make sure lists are same length
    """
    plt.plot(x_values, y_values)
    # Add labels an
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    # plt.show()
    plt.savefig("{}.png".format(file_name))
    plt.close()

def make_bar_graph(file_name:str, title:str, x_label:str, y_label:str, x_values:list , y_values:list) -> None:
    """
    Makes a graph based on the input
    Make sure lists are same length
    """
    plt.bar(x_values, y_values)
    # Add labels an
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    # plt.show()
    plt.savefig("{}.png".format(file_name))
    plt.close()

def make_double_bar_graph(diff_results: dict) -> None:
    """
    Makes a graph based on the input
    Make sure lists are same length
    """
    file_name = "num_of_difficulty_solved"
    title = "Number of Given Difficulty Solved vs. Timeout"
    x_label = "Diffulty Level"
    y_label = "Count"

    x_values = [
        sum(diff_results[0]),
        sum(diff_results[1]),
        sum(diff_results[2])
    ]
    y_values = [
        len(diff_results[0]) - sum(diff_results[0]),
        len(diff_results[1]) - sum(diff_results[1]),
        len(diff_results[2]) - sum(diff_results[2]),

    ]

    N = 3  # Number of bars
    ind = np.arange(N)  
    width = 0.35  # Width of each bar

    fig, ax = plt.subplots()
    bar1 = ax.bar(ind + width/2, y_values, width, color='r', label='Timeout')
    bar2 = ax.bar(ind - width/2, x_values, width, color='b', label='Solved')

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(('Easy', 'Medium', 'Hard'))
    ax.legend()

    # Save and close the plot
    plt.savefig("{}.png".format(file_name))
    plt.close()

    # N = 3
    # ind = np.arange(N)  
    # width = 0.35
    
    # bar1 = plt.bar(ind, x_values, width, color = 'r') 
    
    # bar3 = plt.bar(ind+width*2, y_values, width, color = 'b') 

    # plt.xlabel(x_label)
    # plt.ylabel(y_label)
    # plt.title(title)
    
    # plt.xticks(ind+width,['Easy', 'Medium', 'Hard']) 
    # plt.legend( (bar1, bar3), ('Timeout', 'Solved') ) 

    # plt.bar(x_values, y_values)
    # # Add labels an
    
    # # plt.show()
    # plt.savefig("{}.png".format(file_name))
    # plt.close()



def make_graph_with_best_fit_line(file_name:str, title:str, x_label:str, y_label:str, x_values:list , y_values:list) -> None:
    """
    Makes a graph based on the input WITH A LINE OF BEST FIT
    Make sure lists are same length
    """
    plt.plot(x_values, y_values)
    m, b = np.polyfit(x_values, y_values, 1)#n
    x_fit = np.linspace(min(x_values), max(x_values), 100)  # Generate x values for the regression line
    y_fit = m * x_fit + b # Calculate y values for the regression line
    plt.plot(x_fit, y_fit, color='red') # add the line of best fit
    # Add labels and title
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    # Save the graph
    plt.savefig("{}.png".format(file_name))
    plt.close()

# H update this
def test_boards(data : dict) -> None:
    return
    """
    tests all boards from the given data
    input: boards to test in the same format as the database of boards
    output: None but does create various graphs
    """
    results = dict({})
    num_tiles_results = dict({})

    current_board_num = 0
    total_num_boards = get_number_of_boards(data)
    print("About to test {} board(s)\n\n".format(total_num_boards))

    for board_size in data:

        number_of_tiles = get_number_of_tiles(board_size)


        if num_tiles_results.get(number_of_tiles) == None:
            num_tiles_results.update({number_of_tiles : list([])})

        b_size_data = data.get(board_size)

        for board_num in b_size_data:
            current_board_num += 1
            draw_progress_bar("Testing {} of size {}x{}, total {}/{}".format(
                    str(board_num).ljust(8), 
                    str(board_size.split("x")[0]).rjust(2),
                    str(board_size.split("x")[1]).rjust(2),
                    str(current_board_num).ljust(5),total_num_boards
                    ), 
                current_board_num / total_num_boards
            )
            
            # update with the actual solver
            time_to_solve = timeit.timeit('"-".join(map(str, range(10_000)))', number=1)
            times = list(num_tiles_results.get(number_of_tiles))
            times.append(time_to_solve)
            num_tiles_results.update({ number_of_tiles : times })
    print("")
    graph_number_of_tiles_results(num_tiles_results)


def get_difficulty_level(coords : list[list] , number_of_tiles:int ) -> int:
    """
    input:
        - coords
        - num tiles
    output:
        - difficulty level (0 for easy, 1 for medium, 2 for hard)
    """
    # print(coords, number_of_tiles)
    difficulty_level = 0

    num_white_tiles = 0
    num_islands = 0
    unique_islands = set({})
    for c in coords:
        num_islands+=1
        unique_islands.add(c[2])
        num_white_tiles += c[2]

    num_black_tiles = number_of_tiles - num_white_tiles
    tile_diff = abs(num_black_tiles - num_white_tiles)

    difficulty_level += number_of_tiles / MAX_NUM_TILES

    if tile_diff < 1/3 :
        difficulty_level += len( unique_islands) / num_islands
    
    difficulty_level += (1 - (tile_diff / number_of_tiles))

    return int(difficulty_level)

def timeout_handler(sig, frame):
    raise TimeoutError

def graphs_1(data : dict) -> None:
    """
    Function creates the data that'll be used to graph
    num tiles vs. avg time to solve
    """
    results = dict({}) # of the form {num_tiles : [time_to_solve, time_to_solve, ... ]}
    total_num_boards = get_number_of_boards(data)
    current_board_num = 0
    difficulty_results = { 0 : [] , 1 : [] , 2 : [] }
    for board_size in data:
        number_of_tiles = get_number_of_tiles(board_size)
        # just to double check
        # if current_board_num > 100:
        #     break
        if number_of_tiles <= MAX_NUM_TILES:
            # iterate over all boards of this size
            for board_number in data.get(board_size):
                current_board_num += 1
                # fun progress bar
                draw_progress_bar("Testing {} of size {}x{}, total {}/{}".format(
                        str(board_number).ljust(8), 
                        str(board_size.split("x")[0]).rjust(2),
                        str(board_size.split("x")[1]).rjust(2),
                        str(current_board_num).ljust(5),total_num_boards
                        ), 
                    current_board_num / total_num_boards
                )
                # time to solve it
                curr_board_data = data.get(board_size).get(board_number)
                difficulty = get_difficulty_level(curr_board_data.get("coordinates") , number_of_tiles )
                # Set a timeout of 5 seconds
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(MAX_TIME)  # Trigger timeout_handler after 5 seconds
                try:
                    unused_var = solve(curr_board_data)
                    difficulty_results.update({difficulty : difficulty_results[difficulty] + [1] })
                    """
                    # Get start time
                    start_time = time.perf_counter()  # Use perf_counter for high-resolution
                    # Call the function
                    unused_var = solve(curr_board_data)
                    # Get end time
                    end_time = time.perf_counter()
                    
                    # Calculate execution time
                    time_to_solve = end_time - start_time
                    # time_to_solve = timeit.timeit( backtracking.solve(curr_board_data) , number=1 )
                    if results.get(number_of_tiles) != None:
                        new_list = results.get(number_of_tiles) + [time_to_solve]
                    else:
                        new_list = [time_to_solve]
                    results.update({ number_of_tiles : new_list})
                    """
                except TimeoutError:
                    difficulty_results.update({difficulty : difficulty_results[difficulty] + [0] })
                    pass # go to next iteration
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(MAX_TIME*1_000_000)
    print("\n", difficulty_results)
    try:
        p_easy = sum( difficulty_results[0] ) / len(difficulty_results[0])
    except:
        p_easy = 0
    try:
        p_medium = sum(difficulty_results[1]) / len(difficulty_results[1])
    except:
        p_medium = 0
    try:
        p_hard = sum(difficulty_results[2]) / len(difficulty_results[2])
    except:
        p_hard = 0
    print("\nPrecents of easy, medium, hard:",p_easy, p_medium, p_hard)
    make_bar_graph(
        "perc_of_difficulty_solved" ,
        "Percent Of Difficulty Solved" ,
        "Difficulty Rating",
        "Percent Solved",
        ["Easy" , "Medium" , "Hard"] ,
        [p_easy, p_medium, p_hard]
    )

    make_double_bar_graph(
        difficulty_results
    )
    """
    print("")
    x_axis_data = sorted(list(results.keys()))
    y_axis_data = []
    for num_tiles in x_axis_data:
        times_list = results.get(num_tiles)
        y_value = sum(times_list) / len(times_list)
        y_axis_data.append(y_value)
    make_graph(
        "num_tiles_vs_avg_solve_time" ,
        "Number of Tiles vs. Average Time to Solve", 
        "Number Of Tiles",
        "Average Time To Solve",
        x_axis_data,
        y_axis_data
    )
    """

def graphs_2(data : dict) -> None:
    """
    Function creates the data that'll be used to graph
    num tiles vs. avg tiles from inference
    """
    results = dict({}) # of the form {num_tiles : [time_to_solve, time_to_solve, ... ]}
    current_board_num = 0
    total_num_boards = get_number_of_boards(data)
    for board_size in data:
        number_of_tiles = get_number_of_tiles(board_size)
        if number_of_tiles <= MAX_NUM_TILES:
            for board_num in data.get(board_size):
                current_board_num += 1
                # fun progress bar
                draw_progress_bar("Testing {} of size {}x{}, total {}/{}".format(
                        str(board_num).ljust(8), 
                        str(board_size.split("x")[0]).rjust(2),
                        str(board_size.split("x")[1]).rjust(2),
                        str(current_board_num).ljust(5),total_num_boards
                        ), 
                    current_board_num / total_num_boards
                )
                curr_board_data = data.get(board_size).get(board_num)
                curr_board = curr_board_data.get("board")
                curr_coords = curr_board_data.get("coordinates")
                num_tiles_from_inference =len( inference_at_start(curr_board, curr_coords) )
                if results.get(number_of_tiles) != None:
                    new_list = results.get(number_of_tiles) + [num_tiles_from_inference]
                else:
                    new_list = [num_tiles_from_inference]
                results.update({ number_of_tiles : new_list}) 
    print("")
    x_axis_data = sorted(list(results.keys()))
    y_axis_data = []
    for num_tiles in x_axis_data:
        times_list = results.get(num_tiles)
        y_value = sum(times_list) / len(times_list)
        y_axis_data.append(y_value)

    make_graph_with_best_fit_line(
        "num_tiles_vs_avg_tiles_from_inference" ,
        "Number of Tiles vs. Average Tiles Gained By Inference", 
        "Number Of Tiles",
        "Average Number Of Tiles",
        x_axis_data,
        y_axis_data
    )

def graphs_3(data):
    cell_count_list = []  # Array to store dimension strings
    average_differences = []  # Array to store average differences across all boards for each dimension

    # Iterate through each dimension in the JSON data (like "5x5", "5x6", etc.)
    for dimension in data:
        boards = data[dimension]
        board_count = len(boards)

        count_data = dimension.split('x')
        cell_count = int(count_data[0]) * int(count_data[1])

        cell_count_list.append(cell_count)

        total_difference = 0

        for board_name, board_info in boards.items():
            start_time_solve = time.time()
            solve(copy.deepcopy(board_info))
            end_time_solve = time.time()
            solve_runtime = end_time_solve - start_time_solve

            start_time_solve_NO_inference = time.time()
            solve_NO_inference(copy.deepcopy(board_info))
            end_time_solve_NO_inference = time.time()
            solve_NO_inference_runtime = end_time_solve_NO_inference - start_time_solve_NO_inference

            difference = solve_runtime - solve_NO_inference_runtime
            total_difference += difference

        average_difference = total_difference / board_count
        average_differences.append(average_difference)
        print(f'Average difference for dimension {dimension}: {round(average_difference, 5)} seconds')

    print("Cell count list:", cell_count_list)
    print("Average differences across all boards for each dimension:", average_differences)

    return cell_count_list, average_differences

if __name__ == '__main__':
    print("Let the testing commence!")
    # data = read_in_database()
    data = read_in_test_database()
    
    total_num_boards = get_number_of_boards(data)
    print("About to test {} board(s)".format(total_num_boards))
    # test_boards(data)
    """Comment and uncomment the following as needed"""
    graphs_1(data)
    # data = read_in_test_database()
    # graphs_2(data)

    # cell_count_list, average_differences = graphs_3(data)




"""
TO DO

H 1
finalize num tiles vs. avg time to solve
    - x axis is num tiles
    - y axis is avg time to solve
    - add timeouts / restrict board size

H 2
make num tiles vs tiles from inference
    - x axis is num tiles
    - y axis is avg times from inference

S 3
backtracking vs backtracking with inference
    - x axis is num tiles
    - y axis is
        - avg time difference

S 4
Keep a count of:
    - timeouts for no inference
    - timeouts with inference
    - print these

    try to combine 3 and 4
"""