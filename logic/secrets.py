from .gamestate import GameState
from .coords import CLUE_COORDS

def reveal(gameboard, row, col):
    """
    Reveal tiles, hopefully with significantly less recursion than the first
    iteration of `reveal`
    """
    current_cell = gameboard[row][col]

    if not is_revealable(current_cell):
        return

    current_cell['is_revealed'] = True

    # If the current cell does NOT have an empty clue,
    # then we only want to reveal the current cell. Otherwise,
    # we'd be giving away secrets
    if current_cell['clue'] == 'mine':
        return GameState.LOSE
    elif current_cell['clue'] is not None:
        return GameState.CONTINUE

    recursive_cell_reveal(gameboard, current_cell)

    return GameState.CONTINUE

def recursive_cell_reveal(gameboard, current_cell) -> list:
    """
    Returns a list of cells that need to be revealed, recursively working through
    neighboring cells to `current_cell`
    """

    cells_to_reveal = []

    # Checks the neighboring cells for revealbility
    for neighbor in get_neighbor_cells(gameboard, *current_cell['coords']):
        if neighbor in cells_to_reveal or not is_revealable(neighbor):
            continue
        cells_to_reveal.append(neighbor)

    for cell in cells_to_reveal:
        cell['is_revealed'] = True
    
    # Loops over the neighbors that need to be revealed, adding additional neighbors
    # only if the neighbors of the current cell have empty clues. Everything in this list
    # will inherantly be revealable, and there will not be duplication from previous reveals
    # because of the above line.
    for cell in cells_to_reveal:
        if cell['clue'] is None:
            recursive_cell_reveal(gameboard, cell)

    return cells_to_reveal

def is_revealable(cell) -> bool:
    if cell['is_flagged'] is True or cell['is_revealed'] is True:
        return False
    else:
        return True

def reveal_all(gameboard):
    for row in gameboard:
        for cell in row:
            cell['is_revealed'] = True

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
    if len(unflagged_neighbors) == 0:
        return GameState.CONTINUE

    for neighbor in unflagged_neighbors:
        state = reveal(gameboard, *neighbor['coords'])
        if state == GameState.LOSE:
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
    flag = gameboard[row][col]
    flag['is_flagged'] = not flag['is_flagged']
