CLUE_COORDS = [
    [-1, -1], [-1, 0], [-1, 1],
    [0, -1], [0, 1],
    [1, -1], [1, 0], [1, 1]
]


def flatten_list(two_dim_list):
    """
    Get inner items of a 2D list
    """
    for row in two_dim_list:
        for item in row:
            yield item


def get_neighbor_cells(gameboard, row, col):
    cell = gameboard[row][col]
    neighbors = []
    for coords in CLUE_COORDS:
        neighbor_row = coords[0] + cell["coords"][0]
        neighbor_col = coords[1] + cell["coords"][1]

        if neighbor_row < 0 or neighbor_col < 0:
            continue

        try:
            neighbor_cell = gameboard[neighbor_row][neighbor_col]
        except IndexError:
            continue

        neighbors.append(neighbor_cell)

    return neighbors