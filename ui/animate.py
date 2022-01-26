import time
import random
from . import grid

ANIMATION_TIME = 1

def animate_on(gameboard_data, tiles, tk_root, grid_dims, animation='linear'):
    w, h = grid_dims
    gridsize = w * h

    anim = None
    if animation == 'linear':
        animation = linear_grid(gameboard_data, tiles)
    if animation == 'random':
        animation = random_grid()

    for tile, row, col in animation:
        tile.master.grid(row=row, column=col)
        tile.grid(row=0, column=0, sticky='NSEW')

        tk_root.update()
        time.sleep(ANIMATION_TIME / gridsize)

def linear_grid(gameboard, grid_tiles):
    for cell in grid.get_two_dim_items(gameboard):
        row = cell['coords'][0]
        col = cell['coords'][1]
        tile = grid_tiles[row][col]
        yield tile, row, col

def random_grid(gameboard, grid_tiles):
    while len(gameboard) > 0:
        cell = random.choice(random.choice(gameboard))

    for cell in grid.get_two_dim_items(gameboard):
        row = cell['coords'][0]
        col = cell['coords'][1]
        tile = grid_tiles[row][col]
        yield tile, row, col