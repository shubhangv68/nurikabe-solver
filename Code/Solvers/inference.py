def is_minus_one(x, y, rows, cols, board):
    """
    Utility function for basic_9
    """
    return 0 <= x < rows and 0 <= y < cols and board[x][y] == -1

def inference_at_start(board:list[list[int]], coordinates: list[list[int,int,int]]):
    """
    Some of the inference techniques are run once when starting to solve the board,
        this function combines all of them

    input:
        - board
        - coordinates
    output:
        - ???
    """
    black_tiles = set()
    black_tiles.update( starting_1(board, coordinates)  )
    black_tiles.update( starting_2(board, coordinates) )
    black_tiles.update( starting_3(board, coordinates) )
    black_tiles.update( basic_9(board) )

    return black_tiles

def check_in_board(board, point):
    """
    Checks if the given point is within the bounds of the board.

    Params: 
        - board: Takes in a Nurikabe board state of x by y shape
        - point: Coordinates of a point

    Returns:
        - True: If the point is within the bounds of the board
        - False: If the point is not within the bounds of the board 
    """
    if point[0] >= 0 and point[1] >= 0 and point[0] < len(board) and point[1] < len(board[0]):
        return True
    return False

def get_diagonal_neighbors(board:list[list[int]], point_row:int, point_col:int) -> list[tuple[int,int]]:
    """
    Obtains the 4 DIAGONAL neighbors surrounding the given point's coordinates
    input:
        - point_row: Row of the point
        - point_col: Column of the point
    output:
        - list of tuples of coords
    """
    in_board = []
    points_to_test = [
        (point_row+1, point_col+1),
        (point_row+1, point_col-1),
        (point_row-1, point_col+1),
        (point_row-1, point_col-1)
    ]
    for p in points_to_test:
        if check_in_board(board, p):
            in_board.append(p)
    return in_board

def get_neighbors(board, point_row, point_col):
    """
    Obtains the 4 neighbors surrounding the given point's coordinates
    Only up, down, left, right neighbors. Diagonals not included.

    Params:
        - point_row: Row of the point
        - point_col: Column of the point

    Returns:
        - Array: Returns the coordinates of the 4 surrounding neighbors 
                 as tuples in an array
    """
    potential_neighbors = [(point_row, point_col+1), (point_row+1, point_col), (point_row, point_col-1), (point_row-1, point_col)]
    neighbors = []
    for each in potential_neighbors:
        if check_in_board(board, each):
            neighbors.append(each)
    return neighbors

def starting_1(board, coordinates):
    """
    island of 1 -> all tiles around it are black
    returns a lit of tuples (col , row) of the coords of black tiles
    """
    black_tiles = []

    for coord in coordinates:
        if coord[2] == 1:
            neighbors = get_neighbors(board, coord[0], coord[1])
            for neighbor in neighbors:
                if (neighbor[0], neighbor[1], -1) not in black_tiles:
                    black_tiles.append((neighbor[0], neighbor[1], -1))
                    
    return black_tiles

def starting_2(board : list[list[int]], coordinates: list[list[int,int,int]]) -> list[tuple[int, int]]:
    """
    Clues separated by one square -> inbetween them has to be a black tile
    returns a list of tuples (col, row) of the coord of black tiles
    """
    black_tiles = set({})
    for coord in coordinates:
        in_board = []
        # check if up two, down two, left two, or right two are numbers
        original_point = (coord[1], coord[0])
        up_two_coord = (coord[1]+2, coord[0])
        down_two_coord = (coord[1]-2, coord[0])
        left_two_coord = (coord[1], coord[0]+2)
        right_two_coord = (coord[1], coord[0]-2)
        if check_in_board(board, up_two_coord):
            in_board.append(up_two_coord)
        if check_in_board(board, down_two_coord):
            in_board.append(down_two_coord)
        if check_in_board(board, left_two_coord):
            in_board.append(left_two_coord)
        if check_in_board(board, right_two_coord):
            in_board.append(right_two_coord)
        for coords_again in coordinates:
            coord_point = (coords_again[1], coords_again[0])
            for in_b in in_board:
                if in_b == coord_point:
                    col_dif = original_point[0] - coord_point[0]
                    row_dif = original_point[1] - coord_point[1]
                    if col_dif == 0:
                        row_dif = int(row_dif / 2)
                    else:
                        col_dif = int(col_dif / 2)
                    inbetween_point = (coord_point[1]+row_dif, coord_point[0]+col_dif )
                    black_tiles.add((inbetween_point[0], inbetween_point[1], -1))
                    break

    return list(black_tiles)
        
def starting_3(board : list[list[int]], coordinates: list[list[int,int,int]]) -> list[tuple[int, int]]:
    """
    when two clues are diagonally adjacent then each of the squares touching both clues must be part of a wall.
    """
    black_tiles = set({})
    for coord in coordinates:
        original_point = (coord[1], coord[0])
        in_board = get_diagonal_neighbors(board, coord[1], coord[0])
        for coords_again in coordinates:
            coord_point = (coords_again[1], coords_again[0])
            for in_b in in_board:
                if in_b == coord_point:
                    og_coord_neighbors = set(get_neighbors(board, coord[0], coord[1]))
                    curr_coord_neighbors = set(get_neighbors(board, coord_point[1], coord_point[0]))
                    black_tiles.update( og_coord_neighbors.intersection(curr_coord_neighbors) )
                    break
    new_black_tiles = []
    for tile in black_tiles:
        new_black_tiles.append((tile[0], tile[1], -1))
    return list(new_black_tiles)

def basic_1(board):
    """
    When a white tile is surrounded by walls or black tiles and has no nearby island to connect to, it must be black.
    Params: 
        - board: Takes in a Nurikabe board state of x by y shape
    Returns:
        - black_tiles: A list of tuples for guaranteed black tiles due to the inference
    """
    black_tiles = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                neighbors = get_neighbors(board, i, j)
                sum = 0
                for neighbor in neighbors:
                    sum += board[neighbor[0]][neighbor[1]]
                if len(neighbors) == (-1*sum):
                    black_tiles.append((j, i, -1))
    return black_tiles

def basic_9(board):
    """
    Inferencing technique: avoiding wall area of 2x2
    Returns list of cells that cannot be black
    """
    rows = len(board)
    cols = len(board[0])
    invalid_0_locations = set()

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 0:
                if (is_minus_one(i + 1, j, rows, cols, board) and is_minus_one(i, j + 1, rows, cols, board)
                        and is_minus_one(i + 1, j + 1, rows, cols, board)):

                    invalid_0_locations.add((j, i, 0))

                if (is_minus_one(i + 1, j, rows, cols, board) and is_minus_one(i, j - 1, rows, cols, board)
                        and is_minus_one(i + 1, j - 1, rows, cols, board)):
                    invalid_0_locations.add((j, i, 0))

                if (is_minus_one(i - 1, j, rows, cols, board) and is_minus_one(i, j + 1, rows, cols, board)
                        and is_minus_one(i - 1, j + 1, rows, cols, board)):
                    invalid_0_locations.add((j, i, 0))

                if (is_minus_one(i - 1, j, rows, cols, board) and is_minus_one(i, j - 1, rows, cols, board)
                        and is_minus_one(i - 1, j - 1, rows, cols, board)):
                    invalid_0_locations.add((j, i, 0))

    return sorted(list(invalid_0_locations), key=lambda pos: (pos[0], pos[1]))

"""
# For testing purposes

for row in test_board:
    to_print = ""
    for val in row:
        to_print += str(val).rjust(3)
    print(to_print)
print("coords of the board is",test_locations)
print("Island of 1 inferences: ",starting_1(test_board, test_locations))
print("inbetween 2 numbers inferences: ",starting_2(test_board, test_locations))
print("nums are diag -> touching sides are black tiles:", starting_3(test_board, test_locations))
print("Invalid positions for black tiles", basic_9(basic_9_test_board))
"""

"""
https://www.conceptispuzzles.com/index.aspx?uri=puzzle/nurikabe/techniques

3 starting - Erin (all)

10 basic - Erin (1,2,3), Harry (4,5,6,7), Shubhang (8,9,10)

5 advanced - Harry (1,2), Shubhang (3,4,5)
-> try to attempt, but if it doesn't work that's okay, state why this inference is difficult
"""