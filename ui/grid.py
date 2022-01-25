from tkinter import ttk
from .colors import COLORS
from . import sprite


def make_container(root, controller, coords) -> ttk.Frame:
    """
    Create the tile container, which contains both the button tile and the
    mine clue underneath.

    Note: Might not use this container if I can get the tile and clue to grid
    without it
    """
    row, col = coords
    container = ttk.Frame(root)
    container.configure(
        width=controller.get_setting('cell_size'), 
        height=controller.get_setting('cell_size'), 
        borderwidth=0, 
        relief='solid'
        # background=COLORS[controller.get_setting('game_theme')]['color3']
    )
    container.grid(row=row, column=col)
    container.grid_propagate(0)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(0, weight=1)

    return container

# def make_tile(root, controller, coords) -> ttk.Button:
#     """
#     The tiles on the grid that hide the clues, and can be marked by a flag
#     """
#     row, col = coords
#     tile = ttk.Button(root)
#     tile.configure(
#         # width=controller.get_setting('cell_size'), 
#         # height=controller.get_setting('cell_size'),
#         style='tile.TButton', 
#         command=(lambda lamb_row=row, lamb_col=col: controller.reveal(lamb_row, lamb_col))
#     )
#     # Grid commented out -- it'll get gridded later
#     # grid_tile.grid(row=0, column=0, sticky='NSEW')

#     tile.bind(
#         '<Button-2>', 
#         (lambda e, lamb_row=row, lamb_col=col: controller.flag(lamb_row, lamb_col))
#     )
    
#     return tile

def make_tile(root, controller, coords) -> ttk.Label:
    """
    Gameboard cells which are clickable, and reveal the number of adjacent mines
    """
    row, col = coords
    tile = ttk.Label(root)
    tile.configure(
        anchor='center', 
        text='',
        style='secret.tile.TLabel'
    )
    # Grid commented out -- it'll get gridded later
    # grid_clue.grid(row=0, column=0, sticky='NSEW')

    # Bind both single and double click to the quick_reveal function, so that
    # the user can change quick reveal settings during a game in progress

    # 
    tile.bind(
        '<Button-1>', 
        (lambda e: tile_func(tile, controller, row, col))
    )
    tile.bind(
        '<Double-Button-1>', 
        (lambda e: controller.quick_reveal(row, col, 2) if controller.is_revealed(row, col) else None)
    )
    tile.bind(
        '<Button-2>', 
        (lambda e: controller.flag(row, col) if not controller.is_revealed(row, col) else None)
    )
    tile.bind(
        '<Enter>',
        (lambda e: tile.configure(style='hover.secret.tile.TLabel') if not controller.is_revealed(row, col) else None)
    )
    tile.bind(
        '<Leave>',
        (lambda e: tile.configure(style='secret.tile.TLabel') if not controller.is_revealed(row, col) else None)
    )

    return tile

def tile_func(tile, controller, row, col):
    if controller.is_revealed(row, col):
        controller.quick_reveal(row, col, 1)
    else:
        controller.reveal(row, col)

def make_gameboard(gameboard_data, parent):
    main = ttk.Frame(
        borderwidth=3,
        relief='sunken'
    )
    controller = parent.controller
    widgets = []    # Keeping track of all the widgets on the board

    for row in gameboard_data:
        widget_container = []
        for cell in row:
            container = make_container(main, controller, cell['coords'])
            tile = make_tile(container, controller, cell['coords'])
            
            container.grid(row=cell['coords'][0], column=cell['coords'][1])     # Container grids to the coords, while
            tile.grid(row=0, column=0, sticky='NSEW')                           # the inner elems grid to 0, 0
            widget_container.append(tile)      # Bool used to keep track of if the tile has been removed

        widgets.append(widget_container)

    for i in range(len(gameboard_data[0])):
        main.rowconfigure(i, weight=1)
    for i in range(len(gameboard_data[1])):
        main.columnconfigure(i, weight=1)

    return main, widgets

def update_grid(gameboard, widgets, sprite):
    for cell in get_two_dim_items(gameboard):
        coord_row = cell['coords'][0]
        cood_col = cell['coords'][1]
        tile = widgets[coord_row][cood_col]

        if 'revealed' in tile.configure('style'):
            continue
        if cell['is_flagged'] is True:
            tile.configure(text='F')
        if cell['is_revealed'] is False:
            continue

        # Reveal the tile
        hint = cell['hint'] or ''
        tile.configure(text=hint)
        
        if hint == 'M':
            tile.configure(image=sprite)
            tile.configure(style='revealed.tile.TLabel')
        elif hint == '':
            tile.configure(style='revealed.tile.TLabel')
        else:
            tile.configure(style=f'{hint}.revealed.tile.TLabel')        


def get_two_dim_items(two_dim_list):
    """
    Get inner items of a 2D list
    """
    for row in two_dim_list:
        for item in row:
            yield item
