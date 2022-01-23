from tkinter import Tk, HORIZONTAL
from tkinter import ttk
from . import grid, menus, modals, sprite, style

QUICK_REVEAL_LABELS = ["Off", "Single-Click", "Double-Click"]

class GameWin():
    """
    Creates the main TK window for the game
    """
    def __init__(self, controller):
        self.controller = controller
        self.root = Tk()
        self.root.title("BombSniffer")
        self.root.protocol('WM_DELETE_WINDOW', self.controller.quit_game)

        # The board is created separately so that it can be refreshed between games
        self.board = None
        self.board_widgets = None
        self.info_grid = None
        self.info_reveal = None
        self.menus = None
        self.reset_button = None
        self.timer = None

        self.style = None

    def make_window(self):
        self.make_style()
        self.make_menus()
        self.make_topbar()
        self.make_deco()
        self.make_infobar()

        self.update_infobar()

        self.root.resizable(False, False)

        # Some keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.controller.new_game())
        self.root.bind('<Control-g>', lambda e: self.show_gridsize_modal())
        
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

    def update_infobar(self):
        self.info_grid.config(text='Grid size: {0} x {1}'.format(*self.controller.get_grid_dims()))
        quick_reveal_label = QUICK_REVEAL_LABELS[self.controller.get_setting('quick_reveal')]
        self.info_reveal.config(text=f'Quick Reveal: {quick_reveal_label}')
    
    def update_grid(self):
        grid.update_grid(self.controller.get_gameboard(), self.board_widgets)

    def update_timer(self, timestr):
        self.timer.configure(text = timestr)

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
        timer = ttk.Label(top_bar)

        reset.grid(column=1, row=0)
        top_bar.grid(column=0, row=0, pady=20, padx=20, sticky='NSEW')
        timer.grid(column=1, row=1)

        top_bar.columnconfigure(1, weight=1)
        top_bar.rowconfigure(0, weight=1)
        top_bar.bind('<3>', lambda e: self.post_options_menu(e))

        timer.configure(style='timer.TLabel')

        self.reset_button = reset
        self.timer = timer

    def make_gameboard(self):
        """
        Create the board ui
        """
        if self.board is not None and type(self.board) is ttk.Frame:
            self.board.destroy()

        mine_sprite = sprite.get_sprite(self.controller.get_setting("cell_size"))
        board_frame, board_widgets = grid.make_gameboard(
            self.controller.get_gameboard(),
            self,
            mine_sprite
        )
        # Set the parent so the board has some place to go
        board_frame.grid(
            column=0, 
            row=1, 
            padx=20, 
            pady=(0, 20) 
            # sticky='NSEW'
        )

        self.board = board_frame
        self.board_widgets = board_widgets

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

    def post_options_menu(self, e):
        self.menus["top"].post(e.x_root, e.y_root)

    def post_quick_reveal_menu(self, e):
        self.menus["quick_reveal"].post(e.x_root, e.y_root)
    
    def show_gameover_alert(self, text):
        self.reset_button.configure(text=text)

    def hide_gameover_alert(self):
        self.reset_button.configure(text="BombSniffer")

    def show_gridsize_modal(self):
        modals.make_gridsize_modal(self.root, self.controller)

    def stylize(self, theme):
        style.stylize(self.style, theme)
