from tkinter import ttk


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
    container.grid(row=row, column=col)
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


def make_gameboard(gameboard_data, cell_size, controller, animation=False):
    main = ttk.Frame(
        borderwidth=3,
        relief='sunken'
    )
    widgets = []  # Keeping track of all the widgets on the board

    for row in gameboard_data:
        widgets_row = []  # Creating a mirror gameboard, but for widget data
        for cell in row:
            coords = cell['coords']
            container = make_container(main, cell_size, coords)  # Container makes the width consistent
            tile = make_tile(container)
            tile_bindings(tile, controller, coords)                      # Callbacks to main.py for interaction events
            
            # If there is no animation, grid everything here. Otherwise,
            # it'll be gridded when the function returns
            if animation == 'none':
                container.grid(row=coords[0], column=coords[1])  # Container grids to the coords, while
                tile.grid(row=0, column=0, sticky='NSEW')        # the inner elems grid to 0, 0
            widgets_row.append(tile)

        widgets.append(widgets_row)

    # # Make the colums of the gameboard flexible
    # for i in range(len(gameboard_data[0])):
    #     main.rowconfigure(i, weight=1)
    # for i in range(len(gameboard_data[1])):
    #     main.columnconfigure(i, weight=1)

    return main, widgets


def update_grid(gameboard, widgets, minesprite, flagsprite):
    for cell in get_two_dim_items(gameboard):
        coord_row = cell['coords'][0]
        cood_col = cell['coords'][1]
        tile = widgets[coord_row][cood_col]

        if 'revealed' in tile.configure('style'):
            continue
        if cell['is_flagged'] is True:
            tile.configure(image=flagsprite)
            # tile.configure(text='F')
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


def get_two_dim_items(two_dim_list):
    """
    Get inner items of a 2D list
    """
    for row in two_dim_list:
        for item in row:
            yield item
