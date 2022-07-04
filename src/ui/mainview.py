from logic import gridtools
from logic.timer import TimerState
from tkinter import ttk
from . import grid, menus, modals, style, sprite
from .attributes import FuncAttributes


class GameView():
    """
    Creates the main TK window for the game
    """

    def __init__(self, functions, settings, root):
        self.functions = functions
        self.settings = settings
        self.root = root
        self.root.title("MineSniffer")
        self.root.protocol(
            "WM_DELETE_WINDOW", 
            self.functions.get_func_obj("quit_game")
        )

        # Tk widgets to make. Note that the gmae board is created separately so that
        # it can be refreshed between games
        self.grid_frame = None
        self.topbar_reset = None
        self.topbar_minecount = None
        self.topbar_tilecount = None
        self.topbar_timer_display = None
        self.gridsize_modal = None

        self.style = None
        self.cell_size = self.settings.get_value("cell_size")
        self.mine_sprite = sprite.get_mine_sprite(self.cell_size)
        self.flag_sprite = sprite.get_flag_sprite(self.cell_size)
        self.grid_tiles = None
        self.interrupt_timer_update = False

        self.make_window()
        self.stylize()

    def make_window(self):
        """
        Create each main UI element.
        """
        self.make_style()
        self.make_menus()
        self.make_topbar()

        self.root.resizable(False, False)

        # Some keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.functions.exec("new_game"))
        self.root.bind("<Control-g>", lambda e: self.show_gridsize_modal())
        self.root.bind("<Control-=>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

    def make_style(self):
        """
        Init the ttk Style element.
        """
        self.style = style.make_style(self.root)

    def make_menus(self):
        """
        Create the menubar.
        """
        funcs = self.get_menu_funcs()
        menus.make_options_menus(self.root, self.settings, funcs)

    def make_topbar(self):
        """
        Create the elements for the top bar.
        """
        top_bar = ttk.Frame(self.root)
        reset = ttk.Button(
            top_bar,
            text="BombSniffer",
            command=self.functions.get_func_obj("new_game")
        )
        minecount = ttk.Label(
            top_bar,
            text=0,
            style="stats.TLabel",
            anchor="center"
        )
        tilecount = ttk.Label(
            top_bar,
            text=0,
            style="stats.TLabel",
            anchor="center"
        )
        timer = ttk.Label(top_bar)

        minecount.grid(row=0, column=0, ipadx=4, ipady=4, sticky="E")
        reset.grid(row=0, column=1)
        tilecount.grid(row=0, column=2, ipadx=4, ipady=4, sticky="W")
        timer.grid(row=1, column=1, pady=(10, 0))
        top_bar.grid(row=0, column=0, pady=20, padx=20, sticky="NSEW")

        top_bar.columnconfigure(0, weight=1)
        top_bar.columnconfigure(1, weight=1)
        top_bar.columnconfigure(2, weight=1)
        top_bar.rowconfigure(0, weight=1)

        timer.configure(style="timer.TLabel")

        self.topbar_reset = reset
        self.topbar_minecount = minecount
        self.topbar_tilecount = tilecount
        self.topbar_timer_display = timer
    
    def make_gridsize_modal(self):
        """
        Create the modal used to change the grid size.
        """
        widthvar = self.settings.get_var_obj("grid_width")
        heightvar = self.settings.get_var_obj("grid_height")
        validation_func = self.functions.get_func_obj("validate_dims")
        modal = modals.make_gridsize_modal(self, widthvar, heightvar, validation_func)
        self.gridsize_modal = modal

    def make_gameboard(self):
        """
        Create the board ui
        """
        gameboard = self.functions.exec("get_gameboard")

        # Reset the game board container whenever we make a new one.
        if self.grid_frame is not None and type(self.grid_frame) is ttk.Frame:
            self.grid_frame.destroy()

        animation = self.settings.get_value("grid_animation")
        grid_frame, grid_tiles = grid.make_gameboard(
            self.root,
            gameboard,
            self.cell_size,
            animation,
            self.functions
        )

        self.grid_frame = grid_frame
        self.grid_tiles = grid_tiles

        self.update_minecount()
        self.update_tilecount()
        self.root.update()

    def get_menu_funcs(self) -> FuncAttributes:
        """
        Return the functions use to build the menus.
        """
        funcs = {
            "new_game": self.functions.get_func_obj("new_game"),
            "show_gridsize_modal": self.show_gridsize_modal,
            "zoom_in": self.zoom_in,
            "zoom_out": self.zoom_out,
            "stylize": self.stylize
        }
        return FuncAttributes(funcs)

    def update_grid(self, tile_updates):
        """
        Main grid updater. `tile_updates` should be a minimized list containing only
        cell references that have been updated since the last execution of this function.
        """
        grid.update_grid(
            tile_updates,
            self.grid_tiles,
            self.mine_sprite,
            self.flag_sprite
        )
        self.update_tilecount()

    def update_timer_display(self, timestr):
        """
        Update the timer display with a string. Typically a time string, but can also
        be used to display text (e.g. "Paused").
        """

        # Interrupt the timer to keep the timer from updating after the game is already
        # over, of if a modal has appeared, for instance.
        if self.interrupt_timer_update is True:
            return
        self.topbar_timer_display.configure(text=timestr)

    def update_tilecount(self):
        """
        Update the tile counter badge with the number of non-revealed tiles left.
        """
        tilecount = self.functions.exec("get_num_remaining_cells") 
        self.topbar_tilecount.configure(text=tilecount)

    def update_minecount(self):
        """
        Update the mine counter badge with the number of mines in the field.
        """
        minecount = self.functions.exec("get_num_mines")
        self.topbar_minecount.configure(text=minecount)

    def show_gameover_alert(self, text):
        self.topbar_reset.configure(text=text)

    def hide_gameover_alert(self):
        self.topbar_reset.configure(text="BombSniffer")

    def show_gridsize_modal(self):
        """
        Display the modal used to change the grid size, and pause the timer.
        """
        paused = self.functions.exec("pause_timer")
        if paused is TimerState.PAUSED:
            self.topbar_timer_display.configure(text="Paused")
        self.interrupt_timer_update = True

        if self.gridsize_modal is None:
            self.make_gridsize_modal()

        self.grid_frame.grid_remove()
        self.gridsize_modal.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20),
            ipadx=10,
            ipady=10,
            sticky="NSEW"
        )

    def hide_gridsize_modal(self):
        """
        Remove the gridsize modal and resume the timer.
        """
        if self.gridsize_modal is None:
            return
        self.functions.exec("resume_timer")
        self.interrupt_timer_update = False
        self.gridsize_modal.grid_remove()
        self.grid_frame.grid()

    def stylize(self):
        """
        Change the game theme.
        """
        theme = self.settings.get_value("game_theme")
        style.stylize(self.style, theme)

    def zoom_in(self):
        """
        Make the tiles bigger.
        """
        if self.cell_size >= 50:
            self.cell_size = 50
            return
        self.cell_size += 10
        self.update_zoom()

    def zoom_out(self):
        """
        Make the tiles smaller.
        """
        if self.cell_size <= 20:
            self.cell_size = 20
            return
        self.cell_size -= 10
        self.update_zoom()

    def update_zoom(self):
        """
        Change the size of each tiles' container based on the current cell_size.
        """
        for tile in gridtools.flatten_list(self.grid_tiles):
            tile.master.configure(
                width=self.cell_size,
                height=self.cell_size
            )
        self.settings.set_value("cell_size", self.cell_size)
