from . import gridtools
from .gamestate import GameState


def reveal(gameboard, row, col, tile_updates):
    """
    Reveal tiles, hopefully with significantly less recursion than the first
    iteration of `reveal`
    """
    current_cell = gameboard[row][col]

    if not is_revealable(current_cell):
        return

    current_cell["is_revealed"] = True
    tile_updates.append(current_cell)

    # If the current cell does NOT have an empty clue, then we only want to
    # reveal the current cell. Otherwise, we would be giving away secrets
    if current_cell["hint"] == "M":
        return GameState.LOSE
    elif current_cell["hint"] is not None:
        return GameState.CONTINUE

    recursive_cell_reveal(gameboard, current_cell, tile_updates)

    return GameState.CONTINUE


def recursive_cell_reveal(gameboard, current_cell, tile_updates) -> list:
    """
    Returns a list of cells that need to be revealed, recursively working through
    neighboring cells to `current_cell`
    """

    cells_to_reveal = []

    # Checks the neighboring cells for revealbility
    for neighbor in gridtools.get_neighbor_cells(gameboard, *current_cell["coords"]):
        if neighbor in cells_to_reveal or not is_revealable(neighbor):
            continue
        cells_to_reveal.append(neighbor)

    for cell in cells_to_reveal:
        cell["is_revealed"] = True
        tile_updates.append(cell)
    
    # Loops over the neighbors that need to be revealed, adding additional neighbors
    # only if the neighbors of the current cell have empty clues. Everything in this list
    # will inherantly be revealable, and there will not be duplication from previous reveals
    # because of the above line.
    for cell in cells_to_reveal:
        if cell["hint"] is None:
            recursive_cell_reveal(gameboard, cell, tile_updates)

    return cells_to_reveal


def is_revealable(cell) -> bool:
    if cell["is_flagged"] is True or cell["is_revealed"] is True:
        return False
    else:
        return True


def reveal_all(gameboard, tile_updates):
    for cell in gridtools.flatten_list(gameboard):
        if cell["is_revealed"] is False:
            cell["is_revealed"] = True
            tile_updates.append(cell)


def quick_reveal(gameboard, row, col, tile_updates) -> str:
    """
    Automatically reveal tiles by clicking (or double clicking) on a clue
    if the number of flags has been satisfied. Will cause a game over if one
    of the revealed tiles is a mine.
    """
    cell = gameboard[row][col]
    clue = cell["hint"]

    # Cannot quick-reveal anything if there isn not a clue from which to base the number
    # of surrounding bombs
    if clue is None:
        return

    neighbors = gridtools.get_neighbor_cells(gameboard, row, col)

    # Count the flags among the 8 neighboring cells
    num_flags = len([n for n in neighbors if n["is_flagged"] is True])

    # Player probably does not want to reveal anything if the number of flags
    # does not equal the clue number
    if num_flags != clue:
        return

    # Reveal the neighboring cells if they are not flagged, and return a winning
    # or losing GameState. Otherwise, return CONTINUE
    unflagged_neighbors = [n for n in neighbors if n["is_flagged"] is False]
    if len(unflagged_neighbors) == 0:
        return GameState.CONTINUE

    for neighbor in unflagged_neighbors:
        state = reveal(gameboard, *neighbor["coords"], tile_updates)
        if state == GameState.LOSE:
            return state

    return GameState.CONTINUE


def flag(gameboard, row, col, tile_updates):
    cell = gameboard[row][col]
    cell["is_flagged"] = not cell["is_flagged"]
    tile_updates.append(cell)
