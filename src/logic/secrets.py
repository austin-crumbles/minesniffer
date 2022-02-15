"""
The revealing logic.
"""

from . import gridtools
from .gamestate import GameState


def reveal(gameboard, row, col, tile_updates):
    """
    Reveal tiles!
    """
    current_cell = gameboard[row][col]

    # If the cell is flagged, or already revealed, for instance.
    if not is_revealable(current_cell):
        return GameState.CONTINUE

    # Tag the revealed cell, and store it to send back to the controller.
    # The list will eventually be passed to the mainview as a reference
    # for which tiles have corresponding cells that have been updated.
    current_cell["is_revealed"] = True
    tile_updates.append(current_cell)

    # If the current cell is a mine ("M"), then the game has been lost.
    # 
    # Otherwise, if the current cell is NOT an empty clue, then we 
    # only want to reveal the current cell. Otherwise, we would be giving
    # away secrets
    if current_cell["hint"] == "M":
        return GameState.LOSE
    elif current_cell["hint"] is not None:
        return GameState.CONTINUE

    # If the cell is an empty clue, continue to the recursive reveal.
    recursive_cell_reveal(gameboard, current_cell, tile_updates)

    # If we've made it this far, then the game is still on!
    return GameState.CONTINUE


def recursive_cell_reveal(gameboard, current_cell, tile_updates) -> list:
    """
    Returns a list of cells that need to be revealed, recursively working through
    cells that neighbor `current_cell`.
    """

    cells_to_reveal = []

    # Check if the neighbor cell can be revealed, and if we aren't already tracking it
    for neighbor in gridtools.get_neighbor_cells(gameboard, *current_cell["coords"]):
        if neighbor not in cells_to_reveal and is_revealable(neighbor):
            cells_to_reveal.append(neighbor)

    for cell in cells_to_reveal:
        cell["is_revealed"] = True
        tile_updates.append(cell)
    
    # Loop over the neighbors that need to be revealed, adding additional neighbors
    # only if the neighbors of the current cell have empty clues. Everything in this 
    # list will inherantly be revealable, and there will not be duplication from 
    # previous cycles.
    for cell in cells_to_reveal:
        if cell["hint"] is None:
            recursive_cell_reveal(gameboard, cell, tile_updates)

    return cells_to_reveal


def is_revealable(cell) -> bool:
    """
    Check if `cell` is either flagged or already revealed. If not,
    the cell can be revealed (returns True). 
    """
    if cell["is_flagged"] is True or cell["is_revealed"] is True:
        return False
    else:
        return True


def reveal_all(gameboard, tile_updates) -> None:
    """
    Mark all cells on the board as revealed. Typically used during a lose
    condition.
    """
    for cell in gridtools.flatten_list(gameboard):
        # Limit the number of cells we need to deal with instead of telling
        # the mainview to "just update everything."
        if cell["is_revealed"] is False:
            cell["is_revealed"] = True
            tile_updates.append(cell)


def quick_reveal(gameboard, row, col, tile_updates) -> str:
    """
    Automatically reveal tiles by clicking (or double clicking) on a clue
    if the number of flags has been satisfied. Will cause a game over if one
    of the revealed tiles is a mine (due to a misplaced flag).
    """
    cell = gameboard[row][col]
    clue = cell["hint"]

    # Cannot quick-reveal anything if there isn't a clue from which to base the number
    # of surrounding bombs
    if clue is None:
        return GameState.CONTINUE

    neighbors = gridtools.get_neighbor_cells(gameboard, row, col)

    # Count the flags among the 8 neighboring cells
    num_flags = len([n for n in neighbors if n["is_flagged"] is True])

    # Player probably does not want to reveal anything if the number of flags
    # does not equal the clue number
    if num_flags != clue:
        return GameState.CONTINUE

    # Check for any unflagged neighbors that need to be revealed
    unflagged_neighbors = [n for n in neighbors if n["is_flagged"] is False]
    if len(unflagged_neighbors) == 0:
        return GameState.CONTINUE
    for neighbor in unflagged_neighbors:
        state = reveal(gameboard, *neighbor["coords"], tile_updates)
        if state == GameState.LOSE:
            return state

    return GameState.CONTINUE


def flag(gameboard, row, col, tile_updates):
    """
    Mark a cell as flagged. This inhibits the game from revealing a flagged cell,
    either through directly clicking on and revealing a tile, or through
    quick-revealing via a neighboring tile.
    """
    cell = gameboard[row][col]
    # Toggle `is_flagged`
    cell["is_flagged"] = not cell["is_flagged"]
    tile_updates.append(cell)
