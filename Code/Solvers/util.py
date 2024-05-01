# Useful functions for solving Nurikabe
import json
import math

def replace_int_with_int_in_arr(arr: list[list[int]], prev: int, after: int) -> list[list[int]]:
    """
    Replace all ints in a 2D array with another int
    """
    new_arr = []
    for row in arr:
        new_row = [x if x != prev else after for x in row]
        new_arr.append(new_row)
    return new_arr

def strings_to_ints(arr: list[list[str]]) -> list[list[int]]:
    """
    Given a 2d array of strings, converts strings (numbers) to ints and returns new array
    """
    int_arr = []
    for row in arr:
        int_arr.append([int(number) for number in row])
    return int_arr

def load_board_from_json(board_num: int) -> list[list[str]]:
    """
    Laads the specified boardfrom the database of boards
    """
    with open("../Board-Generators/board_database.json") as f:
        data_set = json.load(f)

    outer_key = list(data_set.keys())[board_num]
    inner_key = list(data_set[outer_key].keys())[board_num]

    return data_set[outer_key][inner_key]

def load_board_from_examples(board_num: int) -> list[list[str]]:
    """
    Laads the specified boardfrom the database of boards
    """
    with open("../Board_Generators/example_boards.json") as f:
        data_set = json.load(f)

    return data_set["examples"][board_num]

def euclidean_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    """
    Returns the euclidean distance between two coords (x1, y1) and (x2, y2)
    """
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))

def valid_cell(arr: list[list[int]], row: int, col: int) -> bool:
    """
    Returns whether arr[row][col] is a valid index
    """
    return row >= 0 and row < len(arr) and col >= 0 and col < len(arr[0])

def print_2darr_nice(arr: list[list]) -> None:
    """
    Prints 2d arr in nicer format
    """
    for sub_arr in arr:
        print(sub_arr)

def copy_2Darr(arr: list[list]) -> list[list]:
    """
    Returns a copy of inputted 2D array
    """
    return [row[:] for row in arr]