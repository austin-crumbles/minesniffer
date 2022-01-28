from curses import window
import time
import random
from . import grid

ANIMATION_TIME = 1

def animate_on(tiles, tk_root, grid_dims, animation='linear'):
    w, h = grid_dims
    gridsize = w * h

    # animation = None
    if animation == 'linear':
        animation = linear_grid(w, h)
    elif animation == 'random':
        animation = random_grid(w, h)
    elif animation == 'snake':
        animation = snake_grid(w, h)

    for row, col in animation:
        tile = tiles[row][col]
        tile.master.grid(row=row, column=col)
        tile.grid(row=0, column=0, sticky='NSEW')

        tk_root.update()
        time.sleep(ANIMATION_TIME / gridsize)

def linear_grid(width, height):
    for cell in get_flat_grid(width, height):
        row, col = cell
        yield row, col

def random_grid(width, height):
    ungridded = get_flat_grid(width, height)

    random.shuffle(ungridded)

    for cell in ungridded:
        row, col = cell
        yield row, col

def snake_grid(width, height):
    ungridded = get_flat_grid(width, height)
    current_cell = [0, 0]
    possible_operations = ((0, 1), (1, 0), (0, -1), (-1, 0))
    current_operation = possible_operations[0]

    while len(ungridded) > 0:
        row, col = current_cell
        try:
            if row < 0 or col < 0:
                raise IndexError
            if (row, col) not in ungridded:
                raise IndexError
            ungridded.remove((row, col))
            yield row, col

        except IndexError:
            current_cell[0] -= current_operation[0]
            current_cell[1] -= current_operation[1]

            next_op = possible_operations.index(current_operation) + 1
            next_op = next_op if next_op < len(possible_operations) else 0
            current_operation = possible_operations[next_op]

        current_cell[0] += current_operation[0]
        current_cell[1] += current_operation[1]

def get_flat_grid(width, height):
    """
    Returns a 1-dimensional list of all the cell coords in the grid.
    """
    grid = []
    for row in range(width):
        for col in range(height):
            grid.append((row, col))

    return grid