"""
Tools used by other game components to manipulate the game board
and its data.
"""

CLUE_COORDS = [
    [-1, -1], [-1, 0], [-1, 1],
    [0, -1], [0, 1],
    [1, -1], [1, 0], [1, 1]
]


def flatten_list(two_dim_list):
    """
    Flatten a nested 2D list into a single list of elements.
    """
    for row in two_dim_list:
        for item in row:
            yield item


def get_neighbor_cells(gameboard, row, col) -> list:
    """
    Get a list of the cells that surround the cell located at `(row, col)`.
    """
    cell = gameboard[row][col]
    neighbors = []

    # Check each neighboring coordinate
    for coords in CLUE_COORDS:
        neighbor_row = coords[0] + cell["coords"][0]
        neighbor_col = coords[1] + cell["coords"][1]

        # If the coorinates are out of range on the lower side,
        # continue, otherwise the game will try to pull from the
        # end of the list, rather than throwing an error.
        #
        # If the coordinates are out of range on the higher side,
        # just catch the error and move along with your merry day.
        if neighbor_row < 0 or neighbor_col < 0:
            continue
        try:
            neighbor_cell = gameboard[neighbor_row][neighbor_col]
        except IndexError:
            continue

        neighbors.append(neighbor_cell)

    return neighbors


def get_coords_list(width, height):
    """
    Returns a 1-dimensional list of all the cell coords in the grid.
    """
    grid = []
    for row in range(width):
        for col in range(height):
            grid.append((row, col))

    return grid
