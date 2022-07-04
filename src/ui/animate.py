"""
Animations for creatively gridding the tiles to the screen.
"""

import time
import random
from logic import gridtools

# How long the animation takes to complete. SHOULD be 1 second.
ANIMATION_TIME = 1

def animate_on(tiles, root, animation="linear"):
    """
    Grid the tiles to the root using the given animation.

    Possible animations are:
    - linear: cascades from left to right, top to bottom
    - random: randomly grid each tile
    - snake: loop tiles around until they reach the center
    """
    rows = len(tiles)
    cols = len(tiles[0])
    area = rows * cols
    coords = gridtools.get_coords_list(cols, rows)

    # A generator that yields each block in the pattern.
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

        # Sleep so the animation doesn't go by faster than perceivable
        time.sleep(ANIMATION_TIME / area)

def linear_grid(coords_list):
    """
    Cascade-grid tiles from left to right, top to bottom.
    """
    for cell in coords_list:
        row, col = cell
        yield row, col

def random_grid(coords_list):
    """
    Randomly grid each tile.
    """
    random.shuffle(coords_list)

    for cell in coords_list:
        row, col = cell
        yield row, col

def snake_grid(coords_list):
    """
    Loop tiles around until they reach the center.
    """
    current_cell = [0, 0]
    possible_operations = ((0, 1), (1, 0), (0, -1), (-1, 0))
    current_operation = possible_operations[0]

    # `coords_list` decreases with each while loop iteration, so eventually
    # the loop will exit.
    while len(coords_list) > 0:
        row, col = current_cell
        try:
            # Using IndexError here to signal that it's time to change the
            # operation.
            if row < 0 or col < 0:
                raise IndexError
            if (row, col) not in coords_list:
                raise IndexError
            coords_list.remove((row, col))

            # Yielding within the try block because we only want to return
            # tiles that actually exist.
            yield row, col

        except IndexError:
            # If an IndexError has occured, then it is time to change the operation.
            # First, reverse the previous step by one...
            current_cell[0] -= current_operation[0]
            current_cell[1] -= current_operation[1]

            # Then get the next operation.
            next_op = possible_operations.index(current_operation) + 1
            next_op = next_op if next_op < len(possible_operations) else 0
            current_operation = possible_operations[next_op]

        # Perform current operation
        current_cell[0] += current_operation[0]
        current_cell[1] += current_operation[1]
