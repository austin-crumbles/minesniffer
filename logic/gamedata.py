import numpy as np
from random import randint
from . import gamestate, CLUE_COORDS
from .timer import GameTimer

MINE_DISTRIBUTION = {
    'Easy': 0.06,
    'Normal': 0.08,
    'Hard': 0.10,
    'Deadly': 0.12
}

class GameData:
    def __init__(self, controller):
        self.controller = controller
        self.gameboard = None
        self.num_mines = None
        self.timer = None
        self.game_state = None
    
    def new_game(self):
        """
        Reset all values to beginning-of-game state
        """
        self.set_gameboard()
        self.set_num_mines()
        self.timer = GameTimer()
        self.game_state = gamestate.IDLE

    def get_num_mines(self):
        if self.num_mines is None:
            self.set_num_mines()
        
        return self.num_mines

    def set_num_mines(self):
        """
        Calculate number of mines based on the grid size and mine distribution percentage
        """
        rows, cols = self.controller.get_grid_dims()
        gridsize = rows * cols
        dist = MINE_DISTRIBUTION[self.controller.get_setting('difficulty')]
        num_mines = np.floor(dist * gridsize)

        self.num_mines = num_mines

    def get_gameboard(self):
        if self.board is None:
            self.set_gameboard()

        return self.board

    def set_gameboard(self):
        board = []
        grid_rows, grid_cols = self.controller.get_grid_dims()

        # Loop over every cell and make a new container, tile, and clue based
        # on the given grid size
        for row in range(grid_rows):
            board.append([])
            for col in range(grid_cols):
                board[row].append({
                    'clue': None,   # Value is one of None, int, or 'mine'
                    'is_revealed': False, 
                    'is_flagged': False,
                    'coords': [row, col]
                })

        self.board = board
        self.place_mines()
        self.place_clues()

    def place_mines(self):
        """
        Places mines in random coordinates. Modifies `grid_data` in place.
        """
        for _ in range(self.get_num_mines()):
            # Place a new mine only if one isn't already placed in that cell
            new_mine = None
            rows, cols = self.controller.get_grid_dims()
            while new_mine is None:
                row = randint(0, rows - 1)
                col = randint(0, cols - 1)
                if self.gameboard[row][col]['clue'] == 'mine':
                    continue
                new_mine = self.gameboard[row][col]
                new_mine['clue'] = 'mine'

    def place_clues(self):
        """
        Calculates mine hints arround mines. Modifies `grid_data` in place.
        """

        mines = [cell for row in self.gameboard for cell in row if cell['clue'] == 'mine']
        for m in mines:
            self.calc_clues(m)

    def calc_clues(self, mine):
        for coord in CLUE_COORDS:
            clue_row = mine['coord'][0] + coord[0]
            clue_col = mine['coord'][1] + coord[1]

            try:
                neighbor_clue = self.gameboard[clue_row][clue_col]['clue']
            except IndexError:  # If the above goes out of row or col range (i.e. -1 or > length)
                continue

            if neighbor_clue is None:
                neighbor_clue['clue'] = 1
            elif neighbor_clue != 'mine':
                neighbor_clue += 1

