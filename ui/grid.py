from tkinter import ttk
from .colors import COLORS

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

def make_tile(root, controller, coords) -> ttk.Button:
    """
    The tiles on the grid that hide the clues, and can be marked by a flag
    """
    row, col = coords
    tile = ttk.Button(root)
    tile.configure(
        # width=controller.get_setting('cell_size'), 
        # height=controller.get_setting('cell_size'),
        style='tile.TButton', 
        command=(lambda lamb_row=row, lamb_col=col: controller.reveal(lamb_row, lamb_col))
    )
    # Grid commented out -- it'll get gridded later
    # grid_tile.grid(row=0, column=0, sticky="NSEW")

    tile.bind(
        '<Button-2>', 
        (lambda e, lamb_row=row, lamb_col=col: controller.flag(lamb_row, lamb_col))
    )
    
    return tile

def make_clue(root, controller, coords) -> ttk.Label:
    """
    The clues underneath the grid tiles
    """
    row, col = coords
    clue = ttk.Label(root)
    clue.configure(
        anchor='center', 
        text="",
        style='clue.TLabel'
        # width=controller.get_setting('cell_size'), 
        # height=controller.get_setting('cell_size')
    )
    # Grid commented out -- it'll get gridded later
    # grid_clue.grid(row=0, column=0, sticky='NSEW')

    # Bind both single and double click to the quick_reveal function, so that
    # the user can change quick reveal settings during a game in progress
    clue.bind(
        '<Button-1>', 
        (lambda e, lamb_row=row, lamb_col=col: controller.quick_reveal(lamb_row, lamb_col, 1))
    )
    clue.bind(
        '<Double-Button-1>', 
        (lambda e, lamb_row=row, lamb_col=col: controller.quick_reveal(lamb_row, lamb_col, 2))
    )

    return clue

def make_gameboard(gameboard_data, parent, sprite):
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
            clue = make_clue(container, controller, cell['coords'])
            if cell['clue'] != 'mine':
                clue.configure(text=cell['clue'])
            elif cell['clue'] == 'mine':
                clue.configure(text="M")
                clue.configure(image=sprite)
            
            container.grid(row=cell['coords'][0], column=cell['coords'][1])     # Container grids to the coords, while
            tile.grid(row=0, column=0, sticky="NSEW")                           # the inner elems grid to 0, 0
            widget_container.append([tile, clue, False])      # Bool used to keep track of if the tile has been removed

        widgets.append(widget_container)

    for i in range(len(gameboard_data[0])):
        main.rowconfigure(i, weight=1)
    for i in range(len(gameboard_data[1])):
        main.columnconfigure(i, weight=1)

    return main, widgets
