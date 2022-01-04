def reveal(self, row, col):
    self.boxes_left
    self.g_over_alert
    self.g_over_flag
    self.num_bombs
    if self.g_over_flag == 1:
        return
    r_button = grid_data[row][col][0]
    try:
        if r_button['text'] != "X":
            r_button.grid_remove()
            grid_data[row][col][0] = 0
            r_button.destroy()
            r_lbl = grid_data[row][col][1]
            self.boxes_left -= 1
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
                                self.reveal(remove_row, remove_col)
                        except IndexError:
                            print("Could not remove box at: {0},{1}"
                                .format(remove_row, remove_col))
                            continue
            elif r_lbl['text'] == "X":
                self.g_over_flag = 1
                for x in range(0, grid_size[0]):
                    for y in range(0, grid_size[1]):
                        if grid_data[x][y][0] != 0:
                            grid_data[x][y][0].destroy()
                print("Game over!")
                self.g_over_alert['text'] = "Game Over!"
                self.g_over_alert.grid(column=0, row=1)
                return
    except TypeError:
        pass
    if self.boxes_left == self.num_bombs:
        self.g_over_alert['text'] = "Chicken Dinner!"
        self.g_over_alert.grid(column=0, row=1)
        self.g_over_flag = 1
        print('Game won!')
    return 0


def auto_reveal(e, row, col, num_clicks):
    if num_clicks != auto_reveal_var.get():
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
                        re = reveal(remove_row, remove_col)
                        if re == 1:
                            return
                except (TypeError, AttributeError, IndexError) as err:
                    continue

def flag(self, row, col):
    self.g_over_flag
    if self.g_over_flag == 1:
        return
    try:
        r_button = grid_data[row][col][0]
        if r_button['text'] == "X":
            r_button['text'] = ""
        elif r_button['text'] == "":
            r_button['text'] = "X"
    except TypeError:
        print("Error because of this: ", row)

def get_num_bombs():
    gs = grid_height.get() * grid_width.get()
    self.num_bombs = floor(log(gs, 20) * difficulty[difficulty['lvl']] * gs)

self.num_bombs
self.boxes_left