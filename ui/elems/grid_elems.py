from .base import *
from ..colors import COLORS

class Grid_Frame(Frame):
    def __init__(self, parent, row, col):
        Frame.__init__(self, parent)
        self.configure(width=cell_size, height=cell_size,
                       borderwidth=0, relief='solid',
                       background=COLORS[game_theme.get()]['color3'])
        self.grid(row=row, column=col)
        self.grid_propagate(0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class Grid_Label(ttk.Label):
    def __init__(self, parent, row, col):
        ttk.Label.__init__(self, parent)
        self.configure(anchor='center', text="")
        self.grid(row=0, column=0, sticky='NSEW')
        self.bind('<Button-1>', (lambda e, lamb_row=row,
                                 lamb_col=col:
                                 auto_reveal(e, lamb_row,
                                             lamb_col, 1)))
        self.bind('<Double-Button-1>', (lambda e, lamb_row=row,
                                        lamb_col=col:
                                        auto_reveal(e, lamb_row,
                                                    lamb_col, 2)))


class Grid_Button(ttk.Button):
    def __init__(self, parent, row, col):
        ttk.Button.__init__(self, parent)
        self.configure(style='grid.TButton',
                       command=(lambda lamb_row=row, lamb_col=col:
                                reveal(lamb_row, lamb_col)))
        self.grid(row=0, column=0, sticky=(N, S, E, W))
        self.bind('<Button-3>', (lambda e, lamb_row=row, lamb_col=col:
                                 flag(lamb_row, lamb_col)))
        self.bind('<Button-1>', (lambda e: start_timer()))

self.g_over_alert.grid_remove()
info_timer['text'] = "00:00"