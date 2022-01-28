from tkinter import ttk
from threading import Thread
from . import animate

def make_container(root, cell_size, coords) -> ttk.Frame:
    """
    Create the tile container, which contains both the button tile and the
    mine clue underneath.

    Note: Might not use this container if I can get the tile and clue to grid
    without it
    """
    row, col = coords
    container = ttk.Frame(root)
    container.configure(
        width=cell_size,
        height=cell_size,
        borderwidth=0,
        relief='solid'
    )
    # container.grid(row=row, column=col)
    container.grid_propagate(0)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(0, weight=1)

    return container


def make_tile(root) -> ttk.Label:
    """
    Gameboard cells which are clickable, and reveal the number of adjacent mines
    """
    tile = ttk.Label(root)
    tile.configure(
        anchor='center',
        text='',
        style='secret.tile.TLabel'
    )

    return tile


def tile_bindings(tile, controller, coords):
    # Bind both single and double click to the quick_reveal function, so that
    # the user can change quick reveal settings during a game in progress
    row, col = coords

    def click_func(event):
        is_revealed = controller.is_revealed(row, col)
        if event == '<Button-1>':
            if is_revealed:
                controller.quick_reveal(row, col, 1)
            else:
                controller.reveal(row, col)
        elif event == '<Double-Button-1>' and is_revealed:
            controller.quick_reveal(row, col, 2)
        elif event == '<Button-2>' and not is_revealed:
            controller.flag(row, col)

    def hover_func(event):
        if controller.is_revealed(row, col):
            return
        if event == '<Enter>':
            tile.configure(style='hover.secret.tile.TLabel')
        elif event == '<Leave>':
            tile.configure(style='secret.tile.TLabel')

    tile.bind(
        '<Button-1>',
        (lambda e: click_func('<Button-1>'))
    )
    tile.bind(
        '<Double-Button-1>',
        (lambda e: click_func('<Double-Button-1>'))
    )
    tile.bind(
        '<Button-2>',
        (lambda e: click_func('<Button-2>'))
    )
    tile.bind(
        '<Enter>',
        (lambda e: hover_func('<Enter>'))
    )
    tile.bind(
        '<Leave>',
        (lambda e: hover_func('<Leave>'))
    )


def make_gameboard(root, gameboard_data, cell_size, controller, animation):
    main = ttk.Frame(
        root,
        borderwidth=3,
        relief='sunken'
    )
    # Keeping track of all the widgets on the board
    tiles_list = []

    for row in gameboard_data:
        # Creating a mirror gameboard, but for widget data
        tiles_list_row = []
        tile_row_frame = ttk.Frame(main)
        for cell in row:
            coords = cell['coords']

            # Container makes the width consistent
            container = make_container(tile_row_frame, cell_size, coords)
            tile = make_tile(container)

            # Callbacks to main.py for interaction events
            tile_bindings(tile, controller, coords)

            # If there is no animation, grid everything here. Otherwise,
            # it'll be gridded when the function returns
            if animation == 'none':
                # Animate will take care of gridding these later
                tile.grid(row=0, column=0, sticky='NSEW')

            container.grid(row=0, column=cell['coords'][1])
            tile_row_frame.grid(row=cell['coords'][0], column=0)

            tiles_list_row.append(tile)
        tiles_list.append(tiles_list_row)

    main.grid(
        column=0,
        row=1,
        padx=20,
        pady=(0, 20)
    )

    if animation != 'none':
        animate.animate_on(tiles_list, root, animation)

    # # If there is no animation, grid everything here. Otherwise,
    # # it'll be gridded when the function returns
    # if animation == 'none':
    #     # Container grids to the coords, while the inner elems grid to 0, 0
    #     Gridder().run(widgets, controller)

    return main, tiles_list


def update_grid(gameboard, widgets, minesprite, flagsprite):
    for cell in flatten_grid(gameboard):
        coord_row = cell['coords'][0]
        cood_col = cell['coords'][1]
        tile = widgets[coord_row][cood_col]

        if 'revealed' in tile.configure('style'):
            continue
        if cell['is_flagged'] is True:
            tile.configure(image=flagsprite)
        else:
            tile.configure(image='')
        if cell['is_revealed'] is False:
            continue

        # Reveal the tile
        hint = cell['hint'] or ''
        tile.configure(text=hint)

        if hint == 'M':
            tile.configure(image=minesprite)
            tile.configure(style='revealed.tile.TLabel')
        elif hint == '':
            tile.configure(style='revealed.tile.TLabel')
        else:
            tile.configure(style=f'{hint}.revealed.tile.TLabel')


def flatten_grid(two_dim_list):
    """
    Get inner items of a 2D list
    """
    for row in two_dim_list:
        for item in row:
            yield item

def get_coords_list(width, height):
    """
    Returns a 1-dimensional list of all the cell coords in the grid.
    """
    grid = []
    for row in range(width):
        for col in range(height):
            grid.append((row, col))

    return grid


class Gridder(Thread):
    def __init__(self):
        super().__init__()

    def run(self, widgets, controller):
        rows = len(widgets)
        cols = len(widgets[0])
        tiles = list(flatten_grid(widgets))
        coords = get_coords_list(width=cols, height=rows)

        for n, t in enumerate(tiles):
            container = t.master
            row = container.master
            t.grid(row=0, column=0, sticky='NSEW')
            container.grid(row=0, column=coords[n][1])
            row.grid(row=coords[n][0], column=0)
            # controller.view.root.update()
            # time.sleep(.01)
        # for c in coords:
        #     container = tiles[0].master
        #     container.grid(row=c[0], column=c[1])
        #     tiles[0].grid(row=0, column=0, sticky='NSEW')
