import math
import random
from . import gridtools
from .gamestate import GameState
from .timer import GameTimer, TimerState


MINE_DISTRIBUTION = {
    "Easy": 0.10,
    "Normal": 0.12,
    "Hard": 0.16,
    "Deadly": 0.2
}

class GameData:
    def __init__(self, timer_callback=None):
        self.timer_callback = timer_callback
        self.gameboard = None
        self.num_mines = None
        self.timer = None
        self.game_state = None
    
    def new_game(self, rows, cols, difficulty):
        """
        Reset all values to beginning-of-game state
        """
        self.set_num_mines(rows, cols, difficulty)
        self.set_gameboard(rows, cols)
        self.timer = GameTimer(self.timer_callback)
        self.game_state = GameState.IDLE

    def get_num_mines(self) -> int:
        return self.num_mines

    def set_num_mines(self, rows, cols, difficulty, n=None):
        """
        Calculate number of mines based on the grid size and mine distribution percentage
        """
        if n is not None:
            self.num_mines = n

        gridsize = rows * cols
        dist = MINE_DISTRIBUTION[difficulty]
        tuner = 98000

        # Quadratic formula, where `tuner` is 20x the max gridsize
        num_mines = math.floor(gridsize * (dist + (gridsize / tuner)))
        self.num_mines = num_mines

    def get_num_remaining_cells(self) -> int:
        """
        Count the number of data cells that have not been revealed.
        """
        cells = [cell for row in self.gameboard for cell in row if cell["is_revealed"] is False]
        return len(cells)

    def get_gameboard(self):
        """
        Returns the current gameboard.
        """
        return self.gameboard

    def set_gameboard(self, num_rows, num_cols):
        """
        Creates a new gameboard with the size `num_rows` x `num_cols`
        """
        gameboard = []

        # Loop over every cell and make a new container, tile, and clue based
        # on the given grid size
        for row in range(num_rows):
            gameboard.append([])
            for col in range(num_cols):
                gameboard[row].append({
                    "hint": None,   # Value is one of None, int, or "M"
                    "is_revealed": False, 
                    "is_flagged": False,
                    "coords": [row, col]
                })

        self.gameboard = gameboard
        self.place_mines(num_rows, num_cols)
        self.place_clues()

    def place_mines(self, num_rows, num_cols):
        """
        Places mines in random coordinates. Modifies `grid_data` in place.
        """
        for _ in range(self.get_num_mines()):
            # Place a new mine only if one isn't already placed in that cell
            new_mine = None
            while new_mine is None:
                row = random.randint(0, num_rows - 1)
                col = random.randint(0, num_cols - 1)
                if self.gameboard[row][col]["hint"] == "M":
                    continue
                new_mine = self.gameboard[row][col]
                new_mine["hint"] = "M"

    def place_clues(self):
        """
        Calculates mine hints arround mines. Modifies `grid_data` in place.
        """

        for cell in gridtools.flatten_list(self.gameboard):
            if cell["hint"] == "M":
                self.calc_clues(*cell["coords"])

    def calc_clues(self, row, col, operation="add"):
        """
        Calculate the number of surrounding mines, and set the data cell located at
        `(row, col)` to that number.

        `operation` is "add" for normal gameboard creation, but can be "subtract" when
        a mine needs to be removed (such as when replacing a mine on the user's first
        move.)
        """
        neighbors = gridtools.get_neighbor_cells(self.gameboard, row, col)
        for cell in neighbors:
            if operation == "add":
                if cell["hint"] is None:
                    cell["hint"] = 1
                elif cell["hint"] != "M":
                    cell["hint"] += 1
            elif operation == "subtract":
                if cell["hint"] == 1:
                    cell["hint"] = None
                elif cell["hint"] != "M":
                    cell["hint"] -= 1

        return neighbors

    def check_win_condition(self):
        remaining_cells = self.get_num_remaining_cells()

        if remaining_cells == self.get_num_mines():
            return GameState.WIN
        else:
            return GameState.CONTINUE

    def start_timer(self):
        if self.timer is None:
            return None
        
        # `timer.start` is used to start the actual thread that the timer is 
        # attatched to, so we have to hide it behind a failsafe, otherwise the 
        # Thread will throw an error whenever this function is called.
        if self.timer.state == TimerState.IDLE:
            self.timer.start()
            return self.get_timer_state()

    def pause_timer(self):
        if self.timer is None:
            return None
        self.timer.pause()
        return self.get_timer_state()

    def resume_timer(self):
        if self.timer is None:
            return None
        self.timer.resume()
        return self.get_timer_state()

    def stop_timer(self):
        if self.timer is None:
            return None
        self.timer.stop()
        return self.get_timer_state()
    
    def get_timer_state(self):
        return self.timer.state

    def check_first_move(self, row, col):
        """
        Check whether the tile about to be revealed is a mine or not. If it is, move the
        mine to a different location on the grid, and recalculate hints that surround both
        the old location and the new location.
        """
        cell = self.gameboard[row][col]
        if cell["hint"] != "M":
            return
        old_neighbors = self.calc_clues(*cell["coords"], operation="subtract")

        # Recalculate the hint based on the number of mines that surrounded the previous
        # location of the mine.
        surrounding_mines = len([m for m in old_neighbors if m["hint"] == "M"])
        if surrounding_mines == 0:
            surrounding_mines = None

        # Wait until after calculating clues to change the hint becuase clues are calculated
        # based on whether the provided cell is a mine or not
        cell["hint"] = surrounding_mines

        # Grab a random cell that doesn't already contain a mine, and isn't at the same
        # coords as the previous mine
        other_cells = []
        for c in gridtools.flatten_list(self.gameboard):
            if c["hint"] != "M" and c["coords"] != cell["coords"]:
                other_cells.append(c)
        new_mine = random.choice(other_cells)

        # Need to change the hint before calculating clues, for the inverse reason as above
        new_mine["hint"] = "M"

        # Calculate the clues of the tiles that surround the new mine location
        self.calc_clues(*new_mine["coords"])
