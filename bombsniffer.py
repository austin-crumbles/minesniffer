# =============
# To Learn List:
#   1. Theme
#   2. Package
#   3. Optimize?
# =============

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from random import randint
from math import *


def reveal(row, col):
    global boxes_left
    global game_over
    global g_over
    global num_bombs
    if g_over == 1:
        return
    r_button = grid_data[row][col][0]
    try:
        if r_button['text'] != 'X':
            r_button.grid_remove()
            # print('Removed box at: ', row, ',',
            #      col)
            grid_data[row][col][0] = 0
            r_button.destroy()
            r_lbl = grid_data[row][col][1]
            boxes_left -= 1
            if r_lbl['text'] == '':
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        remove_row = row + x
                        remove_col = col + y
                        try:
                            # grid_data[remove_row][remove_col][0]
                            if(remove_row < 0 or remove_col < 0 or
                               remove_row >= grid_size[0] or
                               remove_col >= grid_size[1]
                               ):
                                pass
                            else:
                                reveal(remove_row, remove_col)
                        except IndexError:
                            print('Could not remove box at: ', remove_row, ',',
                                  remove_col)
                            continue
            elif r_lbl['text'] == 'X':
                for x in range(0, grid_size[0]):
                    for y in range(0, grid_size[1]):
                        if grid_data[x][y][0] != 0:
                            grid_data[x][y][0].destroy()
                print('Game over!')
                game_over['text'] = 'Game Over!'
                game_over.grid(column=0, row=1)
                return
    except TypeError:
        pass
    # print('Checking to see if the game is won...\n',
    #      boxes_left, ' vs. ', num_bombs)
    if boxes_left == num_bombs:
        game_over['text'] = 'Chicken Dinner!'
        game_over.grid(column=0, row=1)
        g_over = 1


def auto_reveal(row, col):
    global grid_data
    label_ar = grid_data[row][col][1]
    num_flags = 0
    try:
        if label_ar.text == '':
            pass
        elif label_ar.text != '' and label_ar.text != 'X':
            for x in range(-1, 2):
                for y in range(-1, 2):
                    remove_row = row + x
                    remove_col = col + y
                    try:
                        if grid_data[remove_row][remove_col][0]['text'] == 'X':
                            num_flags += 1
                    except AttributeError:
                        pass
        if str(num_flags) == label_ar.text:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    remove_row = row + x
                    remove_col = col + y
                    try:
                        flag_b = grid_data[remove_row][remove_col][0]
                        if flag_b.text == '':
                            flag_b.grid_remove()
                            grid_data[remove_row][remove_col][0] = 0
                            flag_b.destroy()
                    except AttributeError:
                        pass
    except AttributeError as e:
        print('Didn\'t work!', e)


def flag(row, col):
    global g_over
    if g_over == 1:
        return
    try:
        r_button = grid_data[row][col][0]
        if r_button['text'] == 'X':
            r_button['text'] = ''
            print('Un-flagged box at: ', row, ',', col)
        elif r_button['text'] == '':
            r_button['text'] = 'X'
            print('Flagged box at: ', row, ',', col)
    except TypeError:
        print('Error because of this: ', row)


def pop_grid():
    row = 0
    col = 0

    for row in range(grid_size[0]):
        grid_data.append([])
        for col in range(grid_size[1]):
            grid = Frame(main, width=cell_size, height=cell_size,
                         borderwidth=0, relief='solid', background=bgcolor)
            grid.grid(row=row, column=col, sticky=(N, S, E, W))
            grid.grid_propagate(0)
            label = Label(grid)
            label.grid(row=0, column=0)
            button = Button(grid,
                            command=(lambda lamb_row=row, lamb_col=col:
                                     reveal(lamb_row, lamb_col)))
            button.grid(row=0, column=0, sticky=(N, S, E, W))
            button.bind('<Button-3>', (lambda e, lamb_row=row, lamb_col=col:
                                       flag(lamb_row, lamb_col)))
            label.bind('<Double-Button-1>', (lambda e, lamb_row=row,
                                             lamb_col=col:
                                             auto_reveal(lamb_row, lamb_col)))
            grid_data[row].append([button, label])
            label.configure(text='', background=bgcolor)
            grid.columnconfigure(0, weight=1)
            grid.rowconfigure(0, weight=1)
    for i in range(len(grid_data)):
        main.columnconfigure(i, weight=1)
    for i in range(len(grid_data[0])):
        main.rowconfigure(i, weight=1)


def place_bombs():
    global n
    global auto_bombs
    global bombs
    global num_bombs
    num_bombs = bombs
    if (bombs == 'auto' or bombs == 0 or
            bombs > (grid_size[0] * grid_size[1])):
        num_bombs = ceil((grid_size[0] * grid_size[1]) * auto_bombs)
        print('Auto set or invalid number of bombs.')
    while n < num_bombs:
        x = randint(0, grid_size[0] - 1)
        y = randint(0, grid_size[1] - 1)
        place = grid_data[x][y][1]
        if place['text'] == 'X':
            place_bombs()
        else:
            place['image'] = bomb_sprite
            place['text'] = 'X'
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
                        elif clue_label['text'] == '':
                            clue_label['text'] = '1'
                        elif (clue_label['text'] != 'X' and
                              clue_label['text'] != ''):
                            label_num = int(clue_label['text'])
                            label_num += 1
                            clue_label['text'] = label_num
                    except IndexError:
                        pass
            n += 1
    if n == num_bombs:
        print('Placing {0} bombs.'.format(num_bombs))
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
    game_over.grid_remove()
    prog.grid()
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
        h.delete(0, 'end')
        w.delete(0, 'end')
        h.insert(0, grid_size[0])
        w.insert(0, grid_size[1])
        boxes_left = grid_size[0] * grid_size[1]
        # grid_size[0] = int(grid_width.get())
        # grid_size[1] = int(grid_height.get())
    except ValueError:
        print('This didn\'t work: ', grid_height.get())
    g_over = 0
    for child in main.winfo_children():
        child.destroy()
    grid_data = []
    pop_grid()
    n = 0
    place_bombs()
    prog.grid_remove()



root = Tk()
root.title('BombSniffer')
main = ttk.Frame(root, borderwidth=3, relief='sunken')
top_bar = ttk.Frame(root)
sizes = ttk.Frame(root, borderwidth=1, relief='sunken')
reset = ttk.Button(top_bar, text='BombSniffer')
h = Entry(sizes, width=4)
w = Entry(sizes, width=4)
game_over = ttk.Label(root)
prog = ttk.Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')

main.grid(column=0, row=1, padx=20, pady=20, sticky=(N, S, E, W))
top_bar.grid(column=0, row=0, pady=20, padx=20, sticky=(E, W))
reset.grid(column=1, row=0)
sizes.grid(column=0, row=0, ipadx=10, ipady=10, padx=20, pady=20, sticky=W)
w.grid(column=0, row=0)
ttk.Label(sizes, text='W').grid(column=1, row=0)
h.grid(column=0, row=1, pady=5)
ttk.Label(sizes, text='H').grid(column=1, row=1)
prog.grid(column=0, row=1)

root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
top_bar.columnconfigure(1, weight=1)
sizes.columnconfigure(0, weight=1)
sizes.columnconfigure(1, weight=1)
sizes.rowconfigure(0, weight=1)
sizes.rowconfigure(1, weight=1)
# main.grid_propagate(0)

grid_data = []
bgcolor = '#ffffff'
boxes_left = 0
n = 0
bombs = 'auto'
num_bombs = 0
cell_size = 20
auto_bombs = .1         # Percentage of grid covered by bombs for auto.
grid_size = [9, 9]
g_over = 0
grid_height = StringVar()
grid_width = StringVar()
reset['command'] = reset_game
h['textvariable'] = grid_height
w['textvariable'] = grid_width
'''main['width'] = cell_size * grid_size[1]
main['height'] = cell_size * grid_size[0]
main['background'] = bgcolor
'''
h.insert(0, grid_size[0])
w.insert(0, grid_size[1])
print(grid_size)

# pixel = PhotoImage()
bomb_sprite = Image.open('C:\\Users\\Austin\\Desktop\\sprite.png')
bomb_sprite = bomb_sprite.resize((cell_size, cell_size))
bomb_sprite = ImageTk.PhotoImage(bomb_sprite)

reset_game()
mainloop()
