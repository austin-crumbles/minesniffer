from tkinter import ttk
from .colors import COLORS


def make_style(root):
    """
    Initialize the ttke style for the app
    """
    style = ttk.Style(root)
    style.theme_use('default')

    stylize(style, 'dark')
    return style


def stylize(style, theme):
    """
    Change the game's colors
    """
    style.configure(
        'TFrame', 
        background=COLORS[theme]['color2'],
    )
    style.configure(
        'modal.TFrame',
        background=COLORS[theme]['color3']
    )
    style.configure(
        'TLabel', 
        background=COLORS[theme]['color3'],
        foreground=COLORS[theme]['text1']
    )
    style.configure(
        'stats.TLabel',
        relief="raised",
        width="3"
    )
    style.configure(
        'timer.TLabel', 
        background=COLORS[theme]['color2'],
        foreground=COLORS[theme]['text2'], 
        font='Courier'
    )
    style.configure('TButton',
        background=COLORS[theme]['color1'],
        foreground=COLORS[theme]['text1']
    )
    style.configure('info.TLabel', 
        background=COLORS[theme]['color2'],
        foreground=COLORS[theme]['text2']
    )
    style.configure('tile.TLabel',
        background=COLORS[theme]['color3']
    )
    style.configure('secret.tile.TLabel',
        relief='raised',
        background=COLORS[theme]['color1']
    )
    style.configure('hover.secret.tile.TLabel',
        background=COLORS[theme]['color4']
    )
    style.configure('revealed.tile.TLabel',
            relief='none'
    )

    numset = f'numset_{COLORS[theme]["numset"]}'    # Get dark or light numset
    style.configure('1.revealed.tile.TLabel',
        foreground=COLORS[numset]['1']
    )
    style.configure('2.revealed.tile.TLabel',
        foreground=COLORS[numset]['2']
    )
    style.configure('3.revealed.tile.TLabel',
        foreground=COLORS[numset]['3']
    )
    style.configure('4.revealed.tile.TLabel',
        foreground=COLORS[numset]['4']
    )
    style.configure('5.revealed.tile.TLabel',
        foreground=COLORS[numset]['5']
    )
    style.configure('6.revealed.tile.TLabel',
        foreground=COLORS[numset]['6']
    )
    style.configure('7.revealed.tile.TLabel',
        foreground=COLORS[numset]['7']
    )
    style.configure('8.revealed.tile.TLabel',
        foreground=COLORS[numset]['8']
    )

    style.master.configure(background=COLORS[theme]['color2'])
    style.master.update()