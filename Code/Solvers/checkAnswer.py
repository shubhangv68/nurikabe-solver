# test_board = [
#         [1,0,0,0,0,0,0],
#         [0,0,2,0,1,0,1],
#         [1,0,0,0,0,0,0],
#         [0,0,0,2,0,0,1],
#         [0,2,0,0,0,0,0],
#         [0,0,0,1,0,1,0],
#         [0,0,0,0,0,0,0]
# ]
# test_board_sol = [
#         [1,-1,-1,-1,-1,-1,-1],
#         [-1,-1,2,-1,1,-1,1],
#         [1,-1,0,-1,-1,-1,-1],
#         [-1,-1,-1,2,0,-1,1],
#         [-1,2,-1,-1,-1,-1,-1],
#         [-1,0,-1,1,-1,1,-1],
#         [-1,-1,-1,-1,-1,-1,-1]
# ]

# test_board_sol = [
#         [0, 24, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, -1, 0]
#     ]

# test_board_sol = [
#     [3,0,0,-1]
# ]

# test_board = [
#     [20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,24],
#     [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [ 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
#     [ 0, 0, 0, 0, 7, 0, 0, 0, 9, 0, 0, 0],
#     [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
# ]

# test_board = [
#     [0, 0, 0, 0, 0],
#     [0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0],
#     [0, 2, 0, 0, 2],
#     [0, 0, 0, 0, 0]
# ]

test_board_sol = [
        [-1, -1, -1, -1, -1], 
        [-1, 1, -1, 1, -1], 
        [-1, -1, -1, -1, -1], 
        [-1, 2, -1, 0, 2], 
        [-1, 0, -1, -1, -1]
]

test_locations = []
test_white = 0
test_black = 0
test_sum = 0

# for i in range(
# len(test_board)):
#     for j in range(len(test_board[0])):
#         if test_board[i][j] > 0:
#             test_locations.append([(i,j), test_board[i][j]])
#             test_sum += test_board[i][j]
#         if test_board[i][j] == 0:
#             test_white += 1
#         if test_board[i][j] == -1:
#             test_black += 1

for i in range(len(test_board_sol)):
    for j in range(len(test_board_sol[0])):
        if test_board_sol[i][j] > 0:
            test_locations.append([j, i, test_board_sol[i][j]])
            test_sum += test_board_sol[i][j]
        if test_board_sol[i][j] == 0:
            test_white += 1
        if test_board_sol[i][j] == -1:
            test_black += 1

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

def check_connected(board):
    """
    Checks if the black tiles on the given board are fully connected or not.
    Params:
        - board: Takes in a Nurikabe board state of x by y shape
    Returns: 
        - True: If the black tiles are all connected
        - False: If some portion is disconnected
    """
    frontier = []
    visited = []
    found_start = False

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == -1 and found_start == False:
                frontier.append(tuple((i, j)))
                found_start = True
                break
        if found_start == True:
            break

    while len(frontier) != 0:
        curr = frontier.pop(0)
        visited.append(curr)
        neighbors = get_neighbors(board, curr[0], curr[1])

        for neighbor in neighbors:
            if check_in_board(board, neighbor) and (neighbor not in visited) and (neighbor not in frontier) and board[neighbor[0]][neighbor[1]] == -1:
                frontier.append(neighbor)

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == -1 and (i, j) not in visited:
                return False

    return True

def check_areas(board, coords):
    """
    Checks if the white tile areas surrounding a numbered tile
    are of the right size. 
    Params:
        - board: Takes in a Nurikabe board state of x by y shape
        - coords: Coordinates of all numbers (non white and black tiles)
    Returns:
        - True: If the white tiles surrounding a number are of the
                correct value
        - False: If the white tiles surrounding a number are not of
                 the correct value
    """
    total_visited = []
    for coord in coords:
        neighbors = get_neighbors(board, coord[1], coord[0])
        visited = []
        total_visited.append(coord)
        count = coord[2] - 1
        while len(neighbors) > 0:
            curr = neighbors.pop(0)

            if check_in_board(board, curr):
                visited.append(curr)
                # breakpoint()
                if board[curr[0]][curr[1]] == 0 and curr not in total_visited:
                    count -= 1
                    total_visited.append(curr)
                    new_neighbors = get_neighbors(board, curr[0], curr[1])
                    for each_new in new_neighbors:
                        if each_new not in visited: 
                            neighbors.append(each_new)

                if board[curr[0]][curr[1]] == -1:
                    visited.append(curr)
                    if curr not in total_visited:
                        total_visited.append(curr)
                if count < 0:
                    return False
        if count != 0:
            return False

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0 and (i, j) not in total_visited:
                return False

    return True

def check_no_2x2(board):
    """
    Checks if there are any 2x2 black tile sections
    Note that the constraint is violated if there are larger 
    black tile sections, however, any larger x by x section
    must contain a 2x2 section as well and thus we do not 
    need to check for larger areas.
    Params:
        - board: Takes in a Nurikabe board state of x by y shape
    Returns:
        - True: If there are no black clusters
        - False: If there is at least one black cluster
    """

    for i in range(len(board) - 1):
        for j in range(len(board[0]) - 1):
            if (board[i][j] + board[i+1][j] + board[i][j+1] + board[i+1][j+1]) == -4:
                return False

    return True

def check_board(board, coordinates):
    """
    Checks all 3 constraints for any board state.
    Params:
        - board: Takes in a Nurikabe board state of x by y shape
    Returns:
        - True: If all constraints are met
        - False: If any constraint fails
    """
    connected = check_connected(board)
    areas = check_areas(board, coordinates)
    check_2x2 = check_no_2x2(board)

    if connected and areas and check_2x2:
        return True

    return False