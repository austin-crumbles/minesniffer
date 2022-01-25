from tkinter import Tk, HORIZONTAL
from tkinter import ttk
import time

from numpy import tile
from . import grid, menus, modals, style, sprite, animate

QUICK_REVEAL_LABELS = ["Off", "Single-Click", "Double-Click"]


class GameWin():
    """
    Creates the main TK window for the game
    """
    def __init__(self, controller, root):
        self.controller = controller
        self.root = root
        self.root.title("BombSniffer")
        self.root.protocol('WM_DELETE_WINDOW', self.controller.quit_game)
        # self.root.minsize(400, 500)

        # The board is created separately so that it can be refreshed between games
        self.grid_frame = None
        self.grid_tiles = None

        self.info_grid = None
        self.info_reveal = None
        self.menus = None
        self.topbar_reset = None
        self.topbar_minecount = None
        self.topbar_tilecount = None
        self.topbar_timer = None
        self.gridsize_modal = None

        self.interrupt_timer = False

        self.style = None
        self.mine_sprite = sprite.get_mine_sprite(self.controller.get_setting('cell_size'))
        self.flag_sprite = sprite.get_flag_sprite(self.controller.get_setting('cell_size'))

        self.make_window()
        self.stylize(self.controller.get_setting('game_theme'))

    def make_window(self):
        self.make_style()
        self.make_menus()
        self.make_topbar()
        # self.make_deco()
        # self.make_infobar()

        # self.update_infobar()

        self.root.resizable(False, False)

        # Some keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.controller.new_game())
        self.root.bind('<Control-g>', lambda e: self.show_gridsize_modal())
        
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

    def make_style(self):
        self.style = style.make_style(self.root)

    def make_menus(self):
        self.menus = menus.make_options_menus(self)

    def make_topbar(self):
        top_bar = ttk.Frame(self.root)
        reset = ttk.Button(
            top_bar,
            text="BombSniffer",
            command=self.controller.new_game
        )
        minecount = ttk.Label(
            top_bar,
            text=0,
            style='stats.TLabel',
            anchor='center'
        )
        tilecount = ttk.Label(
            top_bar,
            text=0,
            style='stats.TLabel',
            anchor='center'
        )
        timer = ttk.Label(top_bar)

        minecount.grid(row=0, column=0, ipadx=4, ipady=4, sticky='E')
        reset.grid(row=0, column=1)
        tilecount.grid(row=0, column=2, ipadx=4, ipady=4, sticky='W')
        timer.grid(row=1, column=1, pady=(10, 0))
        top_bar.grid(row=0, column=0, pady=20, padx=20, sticky='NSEW')
        
        top_bar.columnconfigure(0, weight=1)
        top_bar.columnconfigure(1, weight=1)
        top_bar.columnconfigure(2, weight=1)
        top_bar.rowconfigure(0, weight=1)
        top_bar.bind('<3>', lambda e: self.post_options_menu(e))

        timer.configure(style='timer.TLabel')

        self.topbar_reset = reset
        self.topbar_minecount = minecount
        self.topbar_tilecount = tilecount
        self.topbar_timer = timer

    def make_gameboard(self):
        """
        Create the board ui
        """
        gameboard = self.controller.get_gameboard()
        if self.grid_frame is not None and type(self.grid_frame) is ttk.Frame:
            self.grid_frame.destroy()

        grid_frame, grid_tiles = grid.make_gameboard(
            gameboard,
            self.controller
        )
        # Set the parent so the board has some place to go
        grid_frame.grid(
            column=0, 
            row=1, 
            padx=20, 
            pady=(0, 20) 
            # sticky='NSEW'
        )

        self.grid_frame = grid_frame
        self.grid_tiles = grid_tiles

        self.update_minecount()
        self.update_tilecount()

        animate.animate_on(gameboard, grid_tiles, self.root, self.controller)

    def make_deco(self):
        """
        Create the line separator between the board and the infobar
        """
        sep = ttk.Separator(self.root, orient=HORIZONTAL)
        sep.grid(column=0, row=2, sticky='EW')

    def make_infobar(self):
        """
        The infobar displays certain pieces of information to the player
        """
        info = ttk.Frame(self.root)
        info_grid = ttk.Label(info)
        info_reveal = ttk.Label(info)

        info.grid(column=0, row=3, sticky='EW')
        info_grid.grid(column=0, row=0, sticky='W', padx=(20, 10))
        info_reveal.grid(column=1, row=0, sticky='E', padx=(10, 20))

        info.columnconfigure(1, weight=1)

        # Ability to click on the info text to change the settings related
        # to the text labels
        info_grid.bind('<1>', lambda e: self.show_gridsize_modal())
        info_reveal.bind('<1>', lambda e: self.post_quick_reveal_menu(e))
        info_reveal.bind('<3>', lambda e: self.post_quick_reveal_menu(e))

        info.configure(style='info.TLabel')
        info_grid.configure(style='info.TLabel')
        info_reveal.configure(style='info.TLabel')

        self.info_grid = info_grid
        self.info_reveal = info_reveal

    def update_infobar(self):
        if self.info_grid is None and self.info_reveal is None:
            return

        self.info_grid.config(text='Grid size: {0} x {1}'.format(*self.controller.get_grid_dims()))
        quick_reveal_label = QUICK_REVEAL_LABELS[self.controller.get_setting('quick_reveal')]
        self.info_reveal.config(text=f'Quick Reveal: {quick_reveal_label}')
    
    def update_grid(self):
        grid.update_grid(
            self.controller.get_gameboard(), 
            self.grid_tiles,
            self.mine_sprite,
            self.flag_sprite
        )
        self.update_tilecount()

    def update_timer(self, timestr):
        if self.interrupt_timer is True:
            return
        self.topbar_timer.configure(text = timestr)

    def update_tilecount(self):
        tilecount = self.controller.get_num_remaining_cells()
        self.topbar_tilecount.configure(text=tilecount)

    def update_minecount(self):
        minecount = self.controller.get_num_mines()
        self.topbar_minecount.configure(text=minecount)

    def get_gridsize_modal(self):
        if self.gridsize_modal is not None:
            return self.gridsize_modal

        modal = modals.make_gridsize_modal(self, self.controller)
        self.gridsize_modal = modal
        return self.gridsize_modal

    def post_options_menu(self, e):
        self.menus['top'].post(e.x_root, e.y_root)

    def post_quick_reveal_menu(self, e):
        self.menus['quick_reveal'].post(e.x_root, e.y_root)
    
    def show_gameover_alert(self, text):
        self.topbar_reset.configure(text=text)

    def hide_gameover_alert(self):
        self.topbar_reset.configure(text="BombSniffer")

    def show_gridsize_modal(self):
        self.controller.pause_timer()
        self.interrupt_timer = True
        modal = self.get_gridsize_modal()
        self.grid_frame.grid_remove()
        modal.grid(
            row=1,
            column=0,
            padx=20, 
            pady=(0, 10),
            ipadx=5,
            ipady=10,
            sticky='NSEW'
        )
    
    def hide_gridsize_modal(self):
        self.controller.resume_timer()
        self.interrupt_timer = False
        self.gridsize_modal.grid_remove()
        self.grid_frame.grid()

    def stylize(self, theme):
        style.stylize(self.style, theme)
