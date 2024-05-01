# Basic backtracking algorithm for solving Nurikabe as a CSP problem
import util
import checkAnswer
import copy
import inference
import sys
import re

# NOTE: 0 = white, -1 = black
# NOTE: coordinates are stored in (column, row) order

def solve_NO_inference(data: dict) -> list[list[int]] | int:
    """
    Solves with NO inference
        for testing purposes
    """
    board = util.strings_to_ints(data["board"])
    board = util.replace_int_with_int_in_arr(board, 0, -1) # set all besides seeds to be black initially
    coordinates = util.strings_to_ints(data["coordinates"])
    
    fixed_cells = []
    return backtracking_search(board, coordinates, get_initial_islands(coordinates), get_initial_neighborhoods(board, coordinates), fixed_cells)

def solve(data: dict) -> list[list[int]] | int:
    """
    Solves the input nurikabe puzzle
    data["board"] contains the board
    data["coordinates"] contains the coordinates of all seed cells along with their numbers
    """
    board = util.strings_to_ints(data["board"])
    board = util.replace_int_with_int_in_arr(board, 0, -1) # set all besides seeds to be black initially
    coordinates = util.strings_to_ints(data["coordinates"])
    
    board, fixed_cells = pre_inference(board, coordinates)
    return backtracking_search(board, coordinates, get_initial_islands(coordinates), get_initial_neighborhoods(board, coordinates), fixed_cells)

def backtracking_search(board: list[list[int]], coordinates: list[int, int, int], islands: dict[tuple[int, int, int], list[tuple[int, int]]], neighborhoods: dict[tuple[int, int], list[tuple[int, int]]], fixed_cells: list[tuple[int, int]]) -> list | int:
    """
    Basic backtracking algorithm. Variables are islands and the domain of an island is its neighborhood of unassigned cells.

    islands: key -- tuple of coordinates of the seed along with its number, value -- list of coordinates of cells that are currently part of the island (includes the seed cell itself)
    neighborhoods: key -- tuples of coordinates of the seed, value -- lisdt of coordinates of cells that are currently part of the neighborhood

    Returns either a solution (board) or -1 for failure
    """
    if checkAnswer.check_board(board, coordinates): # meets all the constraints and is a complete assignment
        return board
    selected_island = select_next_island(islands) # select an island to expand
    if selected_island is None:
        return -1 # no more islands to expand, but it was not correct (as checked earlier), so this configuration is a failure

    island_col = selected_island[0]
    island_row = selected_island[1]
    
    # check each value assignment (cell from its neighborhood) for the selected island
    for cell in order_cells_in_domain(island_col, island_row, neighborhoods[(island_col, island_row)]):
        if cell not in fixed_cells:
            cell_col = cell[0]
            cell_row = cell[1]
            board_copy = util.copy_2Darr(board)
            neighborhoods_copy = copy.deepcopy(neighborhoods)
            islands_copy = copy.deepcopy(islands)
            if not constraints_violated(board, cell_col, cell_row, islands, selected_island): # check if cell assignment is consistent with assignment so far
                board[cell_row][cell_col] = 0 # add grid cell to the assignment
                islands[selected_island].append(cell)
                neighborhoods[(selected_island[0], selected_island[1])] = update_neighborhood(board, cell, neighborhoods[(selected_island[0], selected_island[1])])

                result = backtracking_search(board, coordinates, islands, neighborhoods, fixed_cells)
                if result != -1:
                    return result
            board = board_copy # revert board
            islands = islands_copy # revert islands
            neighborhoods = neighborhoods_copy # revert neighborhoods
    return -1 # failure

def select_next_island(islands: dict[tuple[int, int, int], list[tuple[int, int]]]) -> tuple[int, int, int] | None:
    """
    Selects the next island to assign a value to.
    Returns the chosen island's coordinates and number of the seed, or None if no more to assign
    """
    # most constrained variable: get island with least number of grid cells left to complete the island ( so "fewest legal values left")
    min_keys = [] # candidate tuples for islands with min cells left to fill in
    min_cells_to_assign = float("inf") # keep track of current min amt (not zero)
    for key, val in islands.items():
        cells_left = key[2] - len(val)
        if cells_left < min_cells_to_assign and cells_left > 0:
            min_keys = [key]
            min_cells_to_assign = cells_left
        elif cells_left == min_cells_to_assign and cells_left > 0:
            min_keys.append(key)
    
    chosen_island = min_keys[0] if len(min_keys) > 0 else None # for now
    return chosen_island

def order_cells_in_domain(col: int, row: int, neighborhood: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Returns an ordering of cells from the island's current neighborhood

    col: column of island's seed cell
    row: row of island's seed cell
    neighborhood: a list of coordinates of the cells in the island's neighborhood
    """
    # least constraining value
    # in this context, it means cells that are closer to the numbered cell in the island (and therefore farther from other islands)

    return sorted(neighborhood, key=lambda tup: util.euclidean_distance(tup[0], tup[1], col, row)) # in increasing euclidean distance (so try nearest cells in the neighborhood first)

def constraints_violated(board: list[list[int]], col: int, row: int, islands: dict[tuple[int, int, int], list[tuple[int, int]]], selected_island: tuple[int, int, int]) -> bool:
    """
    Returns whether any constraint is violated by making the specified cell at (col, row) part of the island assignment
    """
    # rule: each island contains only one number and a contiguous area of white cells (the new cell does not connect two different islands)
    connects_islands_constraint = connects_islands(board, col, row, islands, selected_island) # we want this to be false
    # rule: stream cannot be broken
    stream_not_broken = checkAnswer.check_connected(board)
    return connects_islands_constraint or (not stream_not_broken)

def connects_islands(board: list[list[int]], col: int, row: int, islands: dict[tuple[int, int, int], list[tuple[int, int]]], selected_island: tuple[int, int, int]) -> bool:
    """
    Returns whether the addition of the new cell would connect two separate islands together (which we don't want)
    """
    islands_copy = copy.deepcopy(islands)
    islands_copy[selected_island].append((col, row))

    # checking for: two different islands across from each other
    is_island_top = is_valid_island_cell(board, row - 1, col) # there's an island above the newly added cell; same goes for the rest except in different directions
    is_island_bottom = is_valid_island_cell(board, row + 1, col)
    is_island_left = is_valid_island_cell(board, row, col - 1)
    is_island_right = is_valid_island_cell(board, row, col + 1)
    if (is_island_top and is_island_bottom and not (is_island_left or is_island_right)) or (is_island_left and is_island_right and not (is_island_top or is_island_bottom)):
        return True

    # checking for: no "diagonal connections" between two different islands
    connection_top_left = is_valid_island_cell(board, row - 1, col) and is_valid_island_cell(board, row, col - 1) and get_island_of_cell(islands_copy, row - 1, col) != get_island_of_cell(islands_copy, row, col - 1)
    connection_left_bottom = is_valid_island_cell(board, row, col - 1) and is_valid_island_cell(board, row + 1, col) and get_island_of_cell(islands_copy, row, col - 1) != get_island_of_cell(islands_copy, row + 1, col)
    connection_bottom_right = is_valid_island_cell(board, row + 1, col) and is_valid_island_cell(board, row, col + 1) and get_island_of_cell(islands_copy, row + 1, col) != get_island_of_cell(islands_copy, row, col + 1)
    connection_right_top = is_valid_island_cell(board, row, col + 1) and is_valid_island_cell(board, row - 1, col) and get_island_of_cell(islands_copy, row, col + 1) != get_island_of_cell(islands_copy, row - 1, col)

    if connection_top_left or connection_left_bottom or connection_bottom_right or connection_right_top:
        return True

    return False # if either are true, the constraint is violated

def is_valid_island_cell(board: list[list[int]], row: int, col: int) -> bool:
    """
    Returns whether board[row][col] is an island (white) cell that is in range
    """
    return util.valid_cell(board, row, col) and board[row][col] >= 0

def get_island_of_cell(islands: dict[tuple[int, int, int], list[tuple[int, int]]], row: int, col: int) -> tuple[int, int, int]:
    """
    Returns the seed coordinates tuple for islands data structure of the given cell at (row, col)
    """
    index_of_island = [index for index, tups in enumerate(islands.values()) if (col, row) in tups][0]
    return list(islands.keys())[index_of_island]

def update_neighborhood(board: list[list[int]], new_cell: tuple[int, int], neighborhood: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Returns the new neighborhood of the island given that new_cell is added to it
    """
    neighborhood_addition = get_adjacent_cells(board, new_cell[0], new_cell[1]) # cells that need to be added to the neighborhood (may overlap with cells already in neighborhood)
    union_set = list(set(neighborhood).union(set(neighborhood_addition))) # union set
    union_set.remove(new_cell)
    return union_set

def get_adjacent_cells(board: list[list[int]], col: int, row: int) -> list[tuple[int, int]]:
    """
    Returns the adjacent cells (array of tuples) originating from specified coordinate, but only the currently unspecified ones (the "stream")
    """
    adjacent = []
    if util.valid_cell(board, row - 1, col) and board[row - 1][col] == -1: # up
        adjacent.append((col, row - 1))
    if util.valid_cell(board, row + 1, col) and board[row + 1][col] == -1: # down
        adjacent.append((col, row + 1))
    if util.valid_cell(board, row, col - 1) and board[row][col - 1] == -1: # left
        adjacent.append((col - 1, row))
    if util.valid_cell(board, row, col + 1) and board[row][col + 1] == -1: # right
        adjacent.append((col + 1, row))
    return adjacent # in col, row format

def get_initial_neighborhoods(board: list[list[int]], num_coords: list[tuple[int, int, int]]) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """
    Returns initial neighborhoods dict for a board: dict (col, row) of seed: [array of tuples]
    num_coords is from coordinates in the board_database.json file
    """
    neighborhoods_dict = {}
    for coords in num_coords:
        neighborhoods_dict[(coords[0], coords[1])] = get_adjacent_cells(board, coords[0], coords[1])  # col, row
    return neighborhoods_dict

def get_initial_islands(num_coords: list[tuple[int, int, int]]) -> dict[tuple[int, int, int], list[tuple[int, int]]]:
    """
    Returns the initial islands dict where key is the tuple coord of a numbered cell + number in the cell, and value is [tuple coords of cells in the island so far]
    """
    islands = {}
    for tup in num_coords:
        islands[(tup[0], tup[1], tup[2])] = [(tup[0], tup[1])] # col, row
    return islands

def pre_inference(board: list[list[int]], coordinates: list[int, int, int]) -> (list[list[int]], list[tuple[int, int]]):
    """
    Performs inference that can be done prior to backtracking search
    Returns the board, and list of fixed cells
    """
    fixed_cells = inference.inference_at_start(board, coordinates)
    board = add_fixed_cells(board, fixed_cells)
    return (board, fixed_cells)

def add_fixed_cells(board: list[list[int]], fixed_cells: list[tuple[int, int]]) -> list[list[int]]:
    """
    Returns the same board but with the updated cells based on the fixed_cells list
    Fixed cells don't change throughout backtracking, they already have their final values
    """
    for cell in fixed_cells:
        if cell[2] == 0:
            board[cell[1]][cell[0]] = 0
    return board

def get_coordinates(board: list[list[int]]) -> list[tuple[int, int]]:
    """
    """
    coordinates = []
    for i in range(len(board)): # row
        for j in range(len(board[0])): # col
            if board[i][j] > 0: # if the cell is a seed cell with a number in it
                coordinates.append([j, i, board[i][j]]) # col, row
    return coordinates

if __name__== "__main__":
    print("Run with: python backtracking.py [board_num] [inference_option]")
    print("board_num is number of example board [1-5], inclusive")
    print("inference_option is either yesInference or noInference to choose whether backtracking uses pre-inferencing step")
    argv_len = len(sys.argv)
    board_num = int(sys.argv[1])
    inference_option = sys.argv[2]
    # handle error with input
    if board_num not in [1, 2, 3, 4, 5]:
        print("Wrong board_num input. Should be from [1-5], inclusive")
    if inference_option not in ["yesInference", "noInference"]:
        print("Wrong inference_option. inference_option is either yesInference or noInference to choose whether backtracking uses pre-inferencing step")
    print("--------------------------------------------------------------------------------------------------------------")

    # load the board
    data = None
    match board_num:
        case 1:
            data = util.load_board_from_examples(0)
        case 2:
            data = util.load_board_from_examples(1)
        case 3:
            data = util.load_board_from_examples(2)
        case 4:
            data = util.load_board_from_examples(3)
        case 5:
            data = util.load_board_from_examples(4)
    util.print_2darr_nice(data["board"])

    solution = None
    if inference_option == "yesInference":
        solution = solve(data)
    else:
        solution = solve_NO_inference(data)

    if solution == -1:
        print("FAILURE")
    else:
        print("SOLUTION:")
        util.print_2darr_nice(solution)