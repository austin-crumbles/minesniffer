from .colors import COLORS

def stylize(style):
    game_theme.set(style)
    s.configure('TFrame', background=COLORS[style]['color2'])
    s.configure('TLabel', background=COLORS[style]['color3'],
                foreground=COLORS[style]['text1'])
    s.configure('timer.TLabel', background=COLORS[style]['color2'],
                foreground=COLORS[style]['text2'], font='Courier')
    s.configure('TButton', background=COLORS[style]['color1'],
                foreground=COLORS[style]['text1'])
    s.configure('info.TLabel', background=COLORS[style]['color2'],
                foreground=COLORS[style]['text2'])
    root.configure(background=COLORS[style]['color2'])
    info.configure(style='info.TLabel')
    info_timer.configure(style='timer.TLabel')
    info_grid.configure(style='info.TLabel')
    info_reveal.configure(style='info.TLabel')
    root.update()

game_theme = StringVar()
game_theme.set('dark')
stylize(game_theme.get())