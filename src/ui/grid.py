from tkinter import ttk
from threading import Thread
from logic import gridtools
from . import animate
from .attributes import FuncAttributes


def make_gameboard(root, gameboard_data, cell_size, animation, functions: FuncAttributes):
    """
    Create the visual gameboard using the `gameboard_data` supplied by the controller.
    """
    # The main housing for the grid
    main = ttk.Frame(
        root,
        borderwidth=3,
        relief="sunken"
    )
    # Keeping track of all the tiles on the board, so that we can update them later.
    # Essentially a mirror gameboard, but for tile references instead of cell data.
    tiles_list = []

    for row in gameboard_data:
        tiles_list_row = []

        # Break down the main widget into separate rows so that TKinter can have an
        # easier time keeping track of all the widgets going into the grid. Without it,
        # larger grid sizes significantly slow down the program.
        main_row = ttk.Frame(main)
        for cell in row:
            coords = cell["coords"]

            # Container makes the width of the tiles consistent
            container = make_container(main_row, cell_size)
            tile = make_tile(container)

            # Callbacks to the controller for interaction events
            tile_bindings(tile, functions, coords)

            # If there is no animation, grid everything here. Otherwise,
            # the animate module will take care of the gridding.
            if animation == "none":
                tile.grid(row=0, column=0, sticky="NSEW")

            # Each `main_row` takes care of remembering its own respective
            # columns (containers, which in turn each contain a single tile).
            container.grid(row=0, column=cell["coords"][1])
            main_row.grid(row=cell["coords"][0], column=0)

            tiles_list_row.append(tile)
        tiles_list.append(tiles_list_row)

    main.grid(
        column=0,
        row=1,
        padx=20,
        pady=(0, 20)
    )

    # If the tiles were not gridded above, grid them now... fancier.
    if animation != "none":
        animate.animate_on(tiles_list, root, animation)

    return main, tiles_list


def make_container(root, cell_size) -> ttk.Frame:
    """
    Create the tile container, which contains acts as a fence for the tile.
    """
    container = ttk.Frame(root)
    container.configure(
        width=cell_size,
        height=cell_size,
        borderwidth=0
    )
    container.grid_propagate(0)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(0, weight=1)

    return container


def make_tile(root) -> ttk.Label:
    """
    Gameboard tiles which are clickable, flaggable, and reveal the number of 
    adjacent mines or an active mine.
    """
    return GridTile(root)


def tile_bindings(tile, functions, coords):
    """
    Bind callback functions to the grid tiles.
    """
    
    row, col = coords

    def click_func(event):
        """
        Defines the context for which function to call on a tile click
        """
        # Bind both single and double click to the quick_reveal function, so that
        # the user can change quick reveal settings during a game in progress
        if event == "<Button-1>":
            if tile.is_revealed is False:
                functions.exec("reveal", row, col)
            else:
                functions.exec("quick_reveal", row, col, 1)
        elif event == "<Double-Button-1>" and tile.is_revealed is True:
            functions.exec("quick_reveal", row, col, 2)
        elif event == "<Button-2>" and tile.is_revealed is False:
            functions.exec("flag", row, col)

    def hover_func(event):
        """
        Defines the context for which style to change to if a tile is hovered over.
        """
        if tile.is_revealed is True:
            return
        if event == "<Enter>":
            tile.configure(style="hover.secret.tile.TLabel")
        elif event == "<Leave>":
            tile.configure(style="secret.tile.TLabel")

    tile.bind(
        "<Button-1>",
        (lambda e: click_func("<Button-1>"))
    )
    tile.bind(
        "<Double-Button-1>",
        (lambda e: click_func("<Double-Button-1>"))
    )
    tile.bind(
        "<Button-2>",
        (lambda e: click_func("<Button-2>"))
    )
    tile.bind(
        "<Enter>",
        (lambda e: hover_func("<Enter>"))
    )
    tile.bind(
        "<Leave>",
        (lambda e: hover_func("<Leave>"))
    )


def update_grid(tile_updates, widgets, minesprite, flagsprite):
    """
    Main grid updater. `tile_updates` should be a minimized list containing only
    cell references that have been updated since the last execution of this function.
    """
    for data_cell in tile_updates:
        coord_row = data_cell["coords"][0]
        cood_col = data_cell["coords"][1]
        tile = widgets[coord_row][cood_col]

        if tile.is_revealed is True:
            continue

        # Toggle the flag icon
        if data_cell["is_flagged"] is True:
            tile.configure(image=flagsprite)
        else:
            tile.configure(image="")
        
        # Nothing else to do if the cell has not been marked as revealed
        if data_cell["is_revealed"] is False:
            continue

        # Reveal the tile
        # If the hint is `None`, then pass it along as an empty string instead.
        hint = data_cell["hint"] or ""
        tile.configure(text=hint)
        tile.is_revealed = True

        if hint == "M":
            tile.configure(image=minesprite)
            tile.configure(style="revealed.tile.TLabel")
        elif hint == "":
            tile.configure(style="revealed.tile.TLabel")
        else:
            # Assign the style corresponding the the numeric hint. Each numeric
            # hint has a separate color.
            tile.configure(style=f"{hint}.revealed.tile.TLabel")

    # Clear out tile updates when all is said and done.
    tile_updates = []


class GridTile(ttk.Label):
    """
    Small subclass of ttk.Label that adds the ability to track
    if it has been revealed. Avoids a function call back to the 
    controller.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_revealed = False
        self.configure(
            anchor="center",
            text="",
            style="secret.tile.TLabel"
        )
