import math
from random import randint
from re import L
from tkinter.constants import N
from .gamestate import GameState
from .coords import CLUE_COORDS
from .timer import GameTimer, TimerState

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
        self.set_num_mines()
        self.set_gameboard()
        self.timer = GameTimer(self.controller)
        self.game_state = GameState.IDLE

    def get_num_mines(self):
        return self.num_mines

    def set_num_mines(self, n=None):
        """
        Calculate number of mines based on the grid size and mine distribution percentage
        """
        if n is not None:
            self.num_mines = n

        rows, cols = self.controller.get_grid_dims()
        gridsize = rows * cols
        dist = MINE_DISTRIBUTION[self.controller.get_setting('difficulty')]
        num_mines = math.floor(dist * gridsize)

        self.num_mines = num_mines

    def get_num_remaining_cells(self) -> int:
        cells = [cell for row in self.gameboard for cell in row if cell['is_revealed'] is False]
        return len(cells)

    def get_gameboard(self):
        return self.gameboard

    def set_gameboard(self):
        gameboard = []
        grid_rows, grid_cols = self.controller.get_grid_dims()

        # Loop over every cell and make a new container, tile, and clue based
        # on the given grid size
        for row in range(grid_rows):
            gameboard.append([])
            for col in range(grid_cols):
                gameboard[row].append({
                    'hint': None,   # Value is one of None, int, or 'M'
                    'is_revealed': False, 
                    'is_flagged': False,
                    'coords': [row, col]
                })

        self.gameboard = gameboard
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
                if self.gameboard[row][col]['hint'] == 'M':
                    continue
                new_mine = self.gameboard[row][col]
                new_mine['hint'] = 'M'

    def place_clues(self):
        """
        Calculates mine hints arround mines. Modifies `grid_data` in place.
        """

        for row in self.gameboard:
            for cell in row:
                if cell['hint'] == 'M':
                    self.calc_clues(cell)

    def calc_clues(self, mine):
        for coord in CLUE_COORDS:
            clue_row = mine['coords'][0] + coord[0]
            clue_col = mine['coords'][1] + coord[1]

            if clue_row < 0 or clue_col < 0:
                continue
            try:
                neighbor_clue = self.gameboard[clue_row][clue_col]
            except IndexError:  # If the above goes out of row or col range (i.e. -1 or > length)
                continue

            if neighbor_clue['hint'] is None:
                neighbor_clue['hint'] = 1
            elif neighbor_clue['hint'] != 'M':
                neighbor_clue['hint'] += 1

    def check_win_condition(self):
        remaining_cells = self.get_num_remaining_cells()

        if remaining_cells == self.get_num_mines():
            return GameState.WIN
        else:
            return GameState.CONTINUE

    def start_timer(self):
        if self.timer is None:
            return
        if self.timer.running == TimerState.IDLE:
            self.timer.start()

    def pause_timer(self):
        if self.timer is None:
            return
        if self.timer.running == TimerState.RUNNING:
            self.timer.pause()

    def resume_timer(self):
        if self.timer is None:
            return
        if self.timer.running == TimerState.PAUSED:
            self.timer.resume()

    def stop_timer(self):
        if self.timer is None:
            return
        if self.timer.running == TimerState.RUNNING:
            self.timer.stop()
    
    def get_timer_state(self):
        return self.timer.running
