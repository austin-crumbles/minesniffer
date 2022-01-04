from tkinter import IntVar

grid_height = IntVar()
grid_width = IntVar()
cell_size = 20
grid_size = [15, 15]

def pop_grid():
    row = 0
    col = 0

    for row in range(grid_size[0]):
        grid_data.append([])
        for col in range(grid_size[1]):
            grid = Grid_Frame(main, row, col)
            label = Grid_Label(grid, row, col)
            button = Grid_Button(grid, row, col)
            grid_data[row].append([button, label])
    for i in range(len(grid_data)):
        main.columnconfigure(i, weight=1)
    for i in range(len(grid_data[0])):
        main.rowconfigure(i, weight=1)


def place_bombs(alert=0):
    global n
    if alert == 0:
        print("Difficulty level: %s" % difficulty['lvl'])
    while n < self.num_bombs:
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
        print("Placing {0} bombs.".format(self.num_bombs))
        n += 1

def change_grid_size(self):
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

def set_info_var(self, var):
        """Set variables for info bar

        Use 'gs' for grid size. Use 'ar' for auto reveal.
        Use 'd' for difficulty.
        """
        if var == 'gs':
            info_grid['text'] = info_vars['gs'].format(grid_size[0], grid_size[1])
        if var == 'ar':
            n = auto_reveal_var.get()
            if n == 0:
                t = info_vars['ar'].format("Off")
            elif n == 1:
                t = info_vars['ar'].format("Single click")
            elif n == 2:
                t = info_vars['ar'].format("Double click")
            info_reveal['text'] = t
        if var == 'd':
            difficulty['lvl'] = difficulty_var.get()

def get_grid_dimms():
    height = grid_height.get()
    width = grid_width.get()
    if grid_size[0] != height:
        grid_size[0] = height
    if grid_size[1] != width:
        grid_size[1] = width

    if grid_size[0] > 40:
        grid_size[0] = 40
    if grid_size[1] > 40:
        grid_size[1] = 40
    self.boxes_left = grid_size[0] * grid_size[1]

    info_grid['text'] = set_info_var('gs')