# =============
# To Learn List:
#   1. Theme
#   2. Package
#   3. Optimize?
# =============

from tkinter import *
from tkinter import ttk
from time import time, sleep
from PIL import Image, ImageTk
from random import randint
from math import *
import threading

# s = ttk.Style()


def reveal(row, col, num=None):
    global boxes_left
    global game_over
    global g_over
    global num_bombs
    if g_over == 1:
        return
    r_button = grid_data[row][col][0]
    try:
        if r_button['text'] != "X":
            r_button.grid_remove()
            grid_data[row][col][0] = 0
            r_button.destroy()
            r_lbl = grid_data[row][col][1]
            boxes_left -= 1
            if r_lbl['text'] == "":
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        remove_row = row + x
                        remove_col = col + y
                        try:
                            if(remove_row < 0 or remove_col < 0 or
                               remove_row >= grid_size[0] or
                               remove_col >= grid_size[1]
                               ):
                                pass
                            else:
                                reveal(remove_row, remove_col)
                        except IndexError:
                            print("Could not remove box at: {0},{1}"
                                  .format(remove_row, remove_col))
                            continue
            elif r_lbl['text'] == "X":
                g_over = 1
                for x in range(0, grid_size[0]):
                    for y in range(0, grid_size[1]):
                        if grid_data[x][y][0] != 0:
                            grid_data[x][y][0].destroy()
                print("Game over!")
                game_over['text'] = "Game Over!"
                game_over.grid(column=0, row=1)
                return
    except TypeError:
        pass
    if boxes_left == num_bombs:
        game_over['text'] = "Chicken Dinner!"
        game_over.grid(column=0, row=1)
        g_over = 1
        print('Game won!')
    return 0


def auto_reveal(e, row, col, num_clicks):
    if num_clicks != int(auto_reveal_variable.get()):
        return
    label_ar = e.widget
    num_flags = 0
    if label_ar['text'] == "":
        return
    if label_ar['text'] != "" and label_ar['text'] != "X":
        for x in range(-1, 2):
            for y in range(-1, 2):
                remove_row = row + x
                remove_col = col + y
                try:
                    if(remove_row < 0 or remove_col < 0 or
                            remove_row >= grid_size[0] or
                            remove_col >= grid_size[1]):
                        continue
                    elif grid_data[remove_row][remove_col][0]['text'] == "X":
                        num_flags += 1
                except (AttributeError, TypeError):
                    grid_data[remove_row][remove_col][0]
                    continue
    if num_flags == int(label_ar['text']):
        for x in range(-1, 2):
            for y in range(-1, 2):
                remove_row = row + x
                remove_col = col + y
                try:
                    flag_b = grid_data[remove_row][remove_col][0]
                    if(remove_row < 0 or remove_col < 0 or
                            remove_row >= grid_size[0] or
                            remove_col >= grid_size[1]):
                        continue
                    elif flag_b['text'] == "":
                        re = reveal(remove_row, remove_col, num=num_flags)
                        if re == 1:
                            return
                except (TypeError, AttributeError, IndexError) as err:
                    continue


def flag(row, col):
    global g_over
    if g_over == 1:
        return
    try:
        r_button = grid_data[row][col][0]
        if r_button['text'] == "X":
            r_button['text'] = ""
        elif r_button['text'] == "":
            r_button['text'] = "X"
    except TypeError:
        print("Error because of this: ", row)


def pop_grid():
    row = 0
    col = 0

    for row in range(grid_size[0]):
        grid_data.append([])
        for col in range(grid_size[1]):
            grid = Frame(main, width=cell_size, height=cell_size,
                         borderwidth=0, relief='solid',
                         background=Style_colors[game_theme.get()]['color3'])
            grid.grid(row=row, column=col, sticky=(N, S, E, W))
            grid.grid_propagate(0)
            label = ttk.Label(grid)
            label.grid(row=0, column=0)
            button = ttk.Button(grid, style='grid.TButton',
                                command=(lambda lamb_row=row, lamb_col=col:
                                         reveal(lamb_row, lamb_col)))
            button.grid(row=0, column=0, sticky=(N, S, E, W))
            button.bind('<Button-3>', (lambda e, lamb_row=row, lamb_col=col:
                                       flag(lamb_row, lamb_col)))
            button.bind('<Button-1>', (lambda e: start_timer()))

            label.bind('<Button-1>', (lambda e, lamb_row=row,
                                      lamb_col=col:
                                      auto_reveal(e, lamb_row,
                                                  lamb_col, 1)))
            label.bind('<Double-Button-1>', (lambda e, lamb_row=row,
                                             lamb_col=col:
                                             auto_reveal(e, lamb_row,
                                                         lamb_col, 2)))
            grid_data[row].append([button, label])
            label.configure(text='')
            grid.columnconfigure(0, weight=1)
            grid.rowconfigure(0, weight=1)
    for i in range(len(grid_data)):
        main.columnconfigure(i, weight=1)
    for i in range(len(grid_data[0])):
        main.rowconfigure(i, weight=1)


def place_bombs(alert=0):
    global n
    global bombs
    global num_bombs
    global difficulty
    global bomb_sprite
    num_bombs = bombs
    g_dim = grid_size[0] * grid_size[1]
    num_bombs = floor(log(g_dim, 20) * difficulty[difficulty['lvl']] * g_dim)
    if alert == 0:
        print("Difficulty level: %s" % difficulty['lvl'])
    while n < num_bombs:
        x = randint(0, grid_size[0] - 1)
        y = randint(0, grid_size[1] - 1)
        place = grid_data[x][y][1]
        if place['text'] == "X":
            place_bombs(alert=1)
        else:
            place['image'] = bomb_sprite
            place['text'] = "X"
            for a in range(-1, 2):
                for b in range(-1, 2):
                    clue_row = a + x
                    clue_col = b + y
                    try:
                        clue_label = grid_data[clue_row][clue_col][1]
                        if(clue_row < 0 or clue_col < 0 or
                           clue_row >= grid_size[0] or
                           clue_col >= grid_size[1]
                           ):
                            pass
                        elif clue_label['text'] == "":
                            clue_label['text'] = "1"
                        elif (clue_label['text'] != "X" and
                              clue_label['text'] != ""):
                            label_num = int(clue_label['text'])
                            label_num += 1
                            clue_label['text'] = label_num
                    except IndexError:
                        pass
            n += 1
    if alert == 0:
        print("Placing {0} bombs.".format(num_bombs))
        n += 1


def reset_game():
    global main
    global grid_data
    global n
    global bombs
    global num_bombs
    global game_over
    global boxes_left
    global g_over
    global grid_size
    global game_timer
    info_timer['text'] = "00:00"
    game_timer = timer_thread()
    game_over.grid_remove()
    try:
        height = int(grid_height.get())
        width = int(grid_width.get())
        if grid_size[0] != height:
            grid_size[0] = height
        if grid_size[1] != width:
            grid_size[1] = width

        if grid_size[0] > 40:
            grid_size[0] = 40
        if grid_size[1] > 40:
            grid_size[1] = 40
        boxes_left = grid_size[0] * grid_size[1]
    except ValueError:
        print("This didn't work: ", grid_height.get())
    g_over = -1
    info_grid['text'] = set_info_var('gs')
    for child in main.winfo_children():
        child.destroy()
    grid_data = []
    pop_grid()
    n = 0
    place_bombs()


def change_grid_size():
    gsdiag = Toplevel(root)
    gsframe = Frame(gsdiag)
    gstext = Label(gsframe, text="Grid size will update "
                   "in the next game")
    gswidth = Scale(gsframe, orient=HORIZONTAL,
                    length=200, variable=grid_width, from_=10, to=40)
    gsheight = Scale(gsframe, orient=HORIZONTAL,
                     length=200, variable=grid_height, from_=10, to=40)
    gsclose = Button(gsframe, text="Close", command=gsdiag.destroy)

    gsdiag.resizable(FALSE, FALSE)
    gsdiag.title("Grid size")
    gsframe.grid(padx=20, pady=(20, 10))
    gstext.grid()
    gswidth.grid()
    gsheight.grid()
    gsclose.grid(pady=10)


def set_info_var(var):
    """Set variables for info bar

    Use 'gs' for grid size. Use 'ar' for auto reveal.
    Use 'd' for difficulty.
    """
    if var == 'gs':
        t = info_vars['gs'].format(grid_size[0], grid_size[1])
        info_grid['text'] = t
    if var == 'ar':
        n = auto_reveal_variable.get()
        if n == '0':
            t = info_vars['ar'].format("Off")
        elif n == '1':
            t = info_vars['ar'].format("Single click")
        elif n == '2':
            t = info_vars['ar'].format("Double click")
        info_reveal['text'] = t
    if var == 'd':
        d = difficulty_var.get()
        difficulty['lvl'] = d


def start_timer():
    global g_over
    global stime
    if g_over == 1 or g_over == 0:
        return
    elif g_over == -1:
        g_over = 0
        stime = int(time())
        if game_timer.started == 0:
            game_timer.start()


class timer_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.started = 0

    def run(self):
        global g_over
        ss = ""
        mm = "00"
        s = 0
        m = 0
        while g_over == 0:
            if s >= 60:
                m += 1
                mm = "0" + str(m)
                mm = mm[-2:]
                s = 0
            ss = "0" + str(s)
            ss = ss[-2:]
            info_timer['text'] = "{0}:{1}".format(mm, ss)
            s += 1
            sleep(1)
        print("Exiting timer.\n==================")


def stop_threads():
    global g_over
    g_over = 1
    try:
        if len(threading.enumerate()) > 1:
            sleep(1)
            stop_threads()
            root.destroy()
            return
        root.destroy()
    except TclError:
        pass


def stylize(style):
    game_theme.set(style)
    s.configure('TFrame', background=Style_colors[style]['color2'])
    s.configure('TLabel', background=Style_colors[style]['color3'],
                foreground=Style_colors[style]['text1'])
    s.configure('timer.TLabel', background=Style_colors[style]['color2'],
                foreground=Style_colors[style]['text2'])
    s.configure('TButton', background=Style_colors[style]['color1'],
                foreground=Style_colors[style]['text1'])
    s.configure('info.TLabel', background=Style_colors[style]['color2'],
                foreground=Style_colors[style]['text2'])
    root.configure(background=Style_colors[style]['color2'])
    info.configure(style='info.TLabel')
    info_timer.configure(style='timer.TLabel')
    info_grid.configure(style='info.TLabel')
    info_reveal.configure(style='info.TLabel')
    root.update()


root = Tk()
root.title("BombSniffer")
main = ttk.Frame(root, borderwidth=3, relief='sunken')
top_bar = ttk.Frame(root)
sizes = ttk.Frame(root, borderwidth=1, relief='sunken')
reset = ttk.Button(top_bar, text="BombSniffer")
h = Entry(sizes, width=4)
w = Entry(sizes, width=4)
game_over = ttk.Label(root)
sep = ttk.Separator(root, orient=HORIZONTAL)
info = ttk.Frame(root)
info_grid = ttk.Label(info)
info_reveal = ttk.Label(info)
info_timer = ttk.Label(top_bar)
info_timer['text'] = "00:00"

main.grid(column=0, row=1, padx=20, pady=(0, 20), sticky=(N, S, E, W))
top_bar.grid(column=0, row=0, pady=20, padx=20, sticky='NSEW')
reset.grid(column=1, row=0)
info_timer.grid(column=1, row=1)
sep.grid(column=0, row=2, sticky='EW')
info.grid(column=0, row=3, sticky='EW')
info_grid.grid(column=0, row=0, sticky='W', padx=(20, 0))
info_reveal.grid(column=1, row=0, sticky='E', padx=(0, 20))

root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
top_bar.columnconfigure(1, weight=1)
top_bar.rowconfigure(0, weight=1)
info.columnconfigure(1, weight=1)
root.resizable(FALSE, FALSE)

# =====
# Menu bar options
# =====
grid_height = StringVar()
grid_width = StringVar()
auto_reveal_variable = StringVar()
difficulty_var = StringVar()
info_vars = {
    'gs': "Grid size: {0} x {1}",
    'ar': "Auto reveal: {0}"
}
game_timer = None       # Placeholder for thread
grid_data = []
boxes_left = 0
n = 0
bombs = 'auto'
num_bombs = 0
cell_size = 20
grid_size = [15, 15]
reset['command'] = reset_game
grid_height.set(grid_size[0])
grid_width.set(grid_size[1])
auto_reveal_variable.set(2)
difficulty_var.set('Normal')
difficulty = {
    'lvl': difficulty_var.get(),
    'Easy': 0.06,
    'Normal': 0.08,
    'Hard': 0.10,
    'Deadly': 0.12
}
game_theme = StringVar()
game_theme.set('light')
Style_colors = {
    'test': {
        'color1': '#f00',   # Buttons
        'color2': '#0f0',   # Root background
        'color3': '#00f',   # Bombfield background
        'text1': '#fff',    # Bombfield text
        'text2': '#000'     # Root text
    },
    'dark_blue': {
        'color1': '#035',   # Buttons
        'color2': '#013',   # Root background
        'color3': '#068',   # Bombfield background
        'text1': '#fff',    # Bombfield text
        'text2': '#fff'     # Root text
    },
    'dark_red': {
        'color1': '#733',   # Buttons
        'color2': '#412',   # Root background
        'color3': '#844',   # Bombfield background
        'text1': '#fff',    # Bombfield text
        'text2': '#fff'     # Root text
    },
    'dark': {
        'color1': '#222',   # Buttons
        'color2': '#001',   # Root background
        'color3': '#333',   # Bombfield background
        'text1': '#fff',    # Bombfield text
        'text2': '#fff'     # Root text
    },
    'light': {
        'color1': '#ccc',   # Buttons
        'color2': '#eef',   # Root background
        'color3': '#fff',   # Bombfield background
        'text1': '#000',    # Bombfield text
        'text2': '#000'     # Root text
    }
}

# =====
# Menu Items
# =====
root.option_add("*tearOff", 0)
options_bar = Menu(root)
root['menu'] = options_bar
options_menu = Menu(options_bar)
options_auto_flag = Menu(options_menu)
options_difficulty = Menu(options_menu)
options_theme = Menu(options_menu)

options_bar.add_cascade(menu=options_menu, label="Options")
options_menu.add_command(label="New Game", command=reset_game,
                         accelerator="Ctrl+N")
options_menu.add_separator()
options_menu.add_cascade(menu=options_theme, label="Theme")
options_menu.add_command(label="Grid size...",
                         command=change_grid_size, accelerator="Ctrl+G")
options_menu.add_cascade(menu=options_auto_flag, label="Auto reveal tiles")
options_menu.add_cascade(menu=options_difficulty, label="Difficulty")
options_auto_flag.add_radiobutton(label="Double click",
                                  variable=auto_reveal_variable, value=2,
                                  command=lambda: set_info_var('ar'))
options_auto_flag.add_radiobutton(label="Single click",
                                  variable=auto_reveal_variable, value=1,
                                  command=lambda: set_info_var('ar'))
options_auto_flag.add_radiobutton(label="Off",
                                  variable=auto_reveal_variable, value=0,
                                  command=lambda: set_info_var('ar'))
options_difficulty.add_radiobutton(label="Easy", variable=difficulty_var,
                                   value="Easy",
                                   command=lambda: set_info_var('d'))
options_difficulty.add_radiobutton(label="Normal", variable=difficulty_var,
                                   value="Normal",
                                   command=lambda: set_info_var('d'))
options_difficulty.add_radiobutton(label="Hard", variable=difficulty_var,
                                   value="Hard",
                                   command=lambda: set_info_var('d'))
options_difficulty.add_radiobutton(label="Deadly", variable=difficulty_var,
                                   value="Deadly",
                                   command=lambda: set_info_var('d'))
options_theme.add_radiobutton(label="Light", variable=game_theme,
                              value='light', command=lambda: stylize('light'))
options_theme.add_radiobutton(label="Dark", variable=game_theme,
                              value='dark', command=lambda: stylize('dark'))
options_theme.add_radiobutton(label="Dark red", variable=game_theme,
                              value='dark_red', command=lambda:
                              stylize('dark_red'))
options_theme.add_radiobutton(label="Dark blue", variable=game_theme,
                              value='dark_blue', command=lambda:
                              stylize('dark_blue'))


root.bind('<Control-n>', lambda e: reset_game())
root.bind('<Control-g>', lambda e: change_grid_size())
top_bar.bind('<3>', lambda e: options_menu.post(e.x_root, e.y_root))
info_grid.bind('<1>', lambda e: change_grid_size())
info_reveal.bind('<1>', lambda e: options_auto_flag.post(e.x_root, e.y_root))
info_reveal.bind('<3>', lambda e: options_auto_flag.post(e.x_root, e.y_root))
h.insert(0, grid_size[0])
w.insert(0, grid_size[1])

s = ttk.Style()
s.theme_use('default')

sprite = Image.open('C:\\Users\\Austin\\Desktop\\sprite.png')
sprite = sprite.resize((cell_size, cell_size))
bomb_sprite = ImageTk.PhotoImage(sprite)

set_info_var('gs')
set_info_var('ar')

stylize('light')
root.protocol('WM_DELETE_WINDOW', stop_threads)
reset_game()
root.mainloop()
