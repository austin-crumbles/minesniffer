from .gamestate import GameState
from .coords import CLUE_COORDS

def reveal(gameboard, row, col, tiles_left=None, mines=None) -> str:
    """
    Recursively reveals tiles and their neighbors.

    Returns a lib.GameState string
    """
    cell = gameboard[row][col]

    # On the Zeroth recursion, calculate number of tiles and mines.
    # On successive recusrions, just return the number back.
    tiles_left, mines = get_tiles_and_mines(gameboard, tiles_left, mines)

    if cell['is_flagged'] is True or cell['is_revealed'] is True:
        return GameState.CONTINUE

    cell['is_revealed'] = True
    tiles_left -= 1

    if cell['clue'] == 'mine':                              # If cell is a mine, end the game
        return GameState.LOSE
    if cell['clue'] is not None:                            # If the clue is not blank, only reveal that clue
        return check_win_condition(tiles_left, mines)

    for c in CLUE_COORDS:
        remove_row = cell['coords'][0] + c[0]              # Clamps lower bound to 0. Upper bound caught by try / except
        remove_col = cell['coords'][1] + c[1]

        if remove_row < 0 or remove_col < 0:
            continue
        
        # Make sure the value does not exceed the grid length
        try:
            state = reveal(gameboard, remove_row, remove_col, tiles_left, mines)
        except IndexError:
            continue
    
        if state in [GameState.LOSE, GameState.WIN]:
            return state

def check_win_condition(tiles_left, mines):
    print(f"[secrets::reveal] Checking win condition... {tiles_left=}, {mines=}")
    if tiles_left == mines:
        return GameState.WIN
    else:
        return GameState.CONTINUE

def reveal_all(gameboard):
    for row in gameboard:
        for cell in row:
            cell['is_revealed'] = True

def get_tiles_and_mines(gameboard, tiles_left, mines) -> int:
    """
    Returns the number of mines and tiles remianing.

    `tiles_left` and `mines` is not None, just return those values.
    Otherwise calculate their values. (This should only calculate values 
    once per reveal cycle.)
    """
    if tiles_left is not None and mines is not None:
        return tiles_left, mines

    calc_tiles_left = tiles_left or 0
    calc_mines = mines or 0

    for row in gameboard:
        for cell in row:
            # Only increment the value if it actually needs to be calculated
            if cell['is_revealed'] is False and tiles_left is None:
                calc_tiles_left += 1
            if cell['clue'] == 'mine' and mines is None:
                calc_mines += 1

    return calc_tiles_left, calc_mines  

def quick_reveal(gameboard, row, col) -> str:
    """
    Automatically reveal tiles by clicking (or double clicking) on a clue
    if the number of flags has been satisfied. Will cause a game over if one
    of the revealed tiles is a mine.
    """
    cell = gameboard[row][col]
    clue = cell['clue']

    # Can't quick-reveal anything if there isn't a clue off which to base the number
    # of surrounding bombs
    if clue is None:
        return

    neighbors = get_neighbor_cells(gameboard, row, col)

    # Count the flags among the 8 neighboring cells
    num_flags = len([n for n in neighbors if n['is_flagged'] is True])

    # Player probably doesn't want to reveal anything if the number of flags
    # doesn't equal the clue number
    if num_flags != clue:
        return

    # Reveal the neighboring cells if they are not flagged, and return a winning
    # or losing GameState. Otherwise, return CONTINUE
    unflagged_neighbors = [n for n in neighbors if n['is_flagged'] is False]
    for neighbor in unflagged_neighbors:
        state = reveal(gameboard, *neighbor['coords'])
        if state in [GameState.LOSE, GameState.WIN]:
            return state

    return GameState.CONTINUE

def get_neighbor_cells(gameboard, row, col):
    cell = gameboard[row][col]
    neighbors = []
    for coords in CLUE_COORDS:
        neighbor_row = coords[0] + cell['coords'][0]
        neighbor_col = coords[1] + cell['coords'][1]

        if neighbor_row < 0 or neighbor_col < 0:
            continue

        try:
            neighbor_cell = gameboard[neighbor_row][neighbor_col]
        except IndexError:
            continue

        neighbors.append(neighbor_cell)

    return neighbors

def flag(gameboard, row, col):
    flag = gameboard[row][col]['is_flagged']
    flag = not flag

# def reveal_old(self, row, col):
#     self.boxes_left
#     self.g_over_alert
#     self.g_over_flag
#     self.num_mines
#     if self.g_over_flag == 1:
#         return
#     r_button = grid_data[row][col][0]
#     try:
#         if r_button['text'] != "X":
#             r_button.grid_remove()
#             grid_data[row][col][0] = 0
#             r_button.destroy()
#             r_lbl = grid_data[row][col][1]
#             self.boxes_left -= 1
#             if r_lbl['text'] == "":
#                 for x in range(-1, 2):
#                     for y in range(-1, 2):
#                         remove_row = row + x
#                         remove_col = col + y
#                         try:
#                             if(remove_row < 0 or remove_col < 0 or
#                             remove_row >= grid_size[0] or
#                             remove_col >= grid_size[1]
#                             ):
#                                 pass
#                             else:
#                                 self.reveal(remove_row, remove_col)
#                         except IndexError:
#                             print("Could not remove box at: {0},{1}"
#                                 .format(remove_row, remove_col))
#                             continue
#             elif r_lbl['text'] == "X":
#                 self.g_over_flag = 1
#                 for x in range(0, grid_size[0]):
#                     for y in range(0, grid_size[1]):
#                         if grid_data[x][y][0] != 0:
#                             grid_data[x][y][0].destroy()
#                 print("Game over!")
#                 self.g_over_alert['text'] = "Game Over!"
#                 self.g_over_alert.grid(column=0, row=1)
#                 return
#     except TypeError:
#         pass
#     if self.boxes_left == self.num_mines:
#         self.g_over_alert['text'] = "Chicken Dinner!"
#         self.g_over_alert.grid(column=0, row=1)
#         self.g_over_flag = 1
#         print('Game won!')
#     return 0