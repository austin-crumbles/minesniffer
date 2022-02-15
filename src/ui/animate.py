from curses import window
import time
import random
from . import grid

ANIMATION_TIME = 1

def animate_on(tiles, root, animation="linear"):
    rows = len(tiles)
    cols = len(tiles[0])
    area = rows * cols
    coords = grid.get_coords_list(cols, rows)

    # animation = None
    if animation == "linear":
        animation_gen = linear_grid(coords)
    elif animation == "random":
        animation_gen = random_grid(coords)
    elif animation == "snake":
        animation_gen = snake_grid(coords)

    for row, col in animation_gen:
        t = tiles[row][col]
        t.grid(row=0, column=0, sticky="NSEW")
        root.update()
        time.sleep(ANIMATION_TIME / area)

def linear_grid(coords_list):
    for cell in coords_list:
        row, col = cell
        yield row, col

def random_grid(coords_list):
    random.shuffle(coords_list)

    for cell in coords_list:
        row, col = cell
        yield row, col

def snake_grid(coords_list):
    current_cell = [0, 0]
    possible_operations = ((0, 1), (1, 0), (0, -1), (-1, 0))
    current_operation = possible_operations[0]

    while len(coords_list) > 0:
        row, col = current_cell
        try:
            if row < 0 or col < 0:
                raise IndexError
            if (row, col) not in coords_list:
                raise IndexError
            coords_list.remove((row, col))
            yield row, col

        except IndexError:
            current_cell[0] -= current_operation[0]
            current_cell[1] -= current_operation[1]

            next_op = possible_operations.index(current_operation) + 1
            next_op = next_op if next_op < len(possible_operations) else 0
            current_operation = possible_operations[next_op]

        current_cell[0] += current_operation[0]
        current_cell[1] += current_operation[1]
