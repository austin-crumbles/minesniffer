from tkinter import Tk
from tkinter import ttk
from . import grid, menus
from .colors import COLORS

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
        self.info_grid = None
        self.info_reveal = None
        self.options_menu = None

        self.make_style()
        self.make_menus()
        self.make_topbar()
        self.make_gameboard()
        self.make_deco()
        self.make_infobar()
        self.update_infobar()

        self.root.resizable(False, False)

        # Some keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.controller.reset_game())
        self.root.bind('<Control-g>', lambda e: self.controller.change_grid_size())
        
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

    def update_infobar(self):
        self.info_grid.config(text='Grid size: {0} x {1}'.format(*self.controller.get_grid_dims()))
        quick_reveal_label = QUICK_REVEAL_LABELS[self.controller.get_setting('quick_reveal')]
        self.info_reveal.config(text=f'Quick Reveal: {quick_reveal_label}')
    
    def make_style(self):
        """
        Initialize the ttke style for the app
        """
        style = ttk.Style(self.root)
        style.theme_use('default')

    def make_menus(self):
        self.options_menu = menus.make_options_menu(self.root, self.controller)

    def make_topbar(self):
        top_bar = ttk.Frame(self.root)
        reset = ttk.Button(
            top_bar,
            text="BombSniffer",
            command=self.controller.reset_game
        )
        timer = ttk.Label(top_bar)

        reset.grid(column=1, row=0)
        top_bar.grid(column=0, row=0, pady=20, padx=20, sticky='NSEW')
        timer.grid(column=1, row=1)

        top_bar.columnconfigure(1, weight=1)
        top_bar.rowconfigure(0, weight=1)
        top_bar.bind('<3>', lambda e: self.controller.show_options_menu(e))

        timer['text'] = "00:00"

        timer.configure(style='timer.TLabel')

    def make_gameboard(self):
        """
        Create the board ui
        """
        if self.board is not None and type(self.board) is ttk.Frame:
            self.board.destroy()

        board_frame, board_widgets = grid.make_gameboard(
            self.controller.get_gameboard_data(), 
            self.controller.get_grid_dims(), 
            self.controller.get_num_mines()
        )
        # Set the parent so the board has some place to go
        board_frame.configure(parent=self.root)
        board_frame.grid(
            column=0, 
            row=1, 
            padx=20, 
            pady=(0, 20), 
            sticky='NSEW'
        )

        self.board = board_widgets

    def make_deco(self):
        """
        Create the line separator between the board and the infobar
        """
        sep = ttk.Separator(self.root, orient='HORIZONTAL')
        sep.grid(column=0, row=2, sticky='EW')

    def make_infobar(self):
        """
        The infobar displays certain pieces of information to the player
        """
        info = ttk.Frame(self.root)
        info_grid = ttk.Label(info)
        info_reveal = ttk.Label(info)

        info.grid(column=0, row=3, sticky='EW')
        info_grid.grid(column=0, row=0, sticky='W', padx=(20, 0))
        info_reveal.grid(column=1, row=0, sticky='E', padx=(0, 20))

        info.columnconfigure(1, weight=1)

        # Ability to click on the info text to change the settings related
        # to the text labels
        info_grid.bind('<1>', lambda e: self.controller.change_grid_size())
        info_reveal.bind('<1>', lambda e: self.controller.options_auto_flag.post(e.x_root, e.y_root))
        info_reveal.bind('<3>', lambda e: self.controller.options_auto_flag.post(e.x_root, e.y_root))

        info.configure(style='info.TLabel')
        info_grid.configure(style='info.TLabel')
        info_reveal.configure(style='info.TLabel')

        self.info_grid = info_grid
        self.info_reveal = info_reveal

    def stylize(self, style):
        """
        Change the game's colors
        """
        style.configure(
            'TFrame', 
            background=COLORS[style]['color2']
        )
        style.configure(
            'TLabel', 
            background=COLORS[style]['color3'],
            foreground=COLORS[style]['text1']
        )
        style.configure(
            'timer.TLabel', 
            background=COLORS[style]['color2'],
            foreground=COLORS[style]['text2'], 
            font='Courier'
        )
        style.configure('TButton',
            background=COLORS[style]['color1'],
            foreground=COLORS[style]['text1']
        )
        style.configure('info.TLabel', 
            background=COLORS[style]['color2'],
            foreground=COLORS[style]['text2']
        )

        self.root.configure(background=COLORS[style]['color2'])
        self.root.update()

    def post_options_menu(self, e):
        self.options_menu.post(e.x_root, e.y_root)