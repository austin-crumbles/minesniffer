"""Go sniff for some mines"""
import json
import random
import logging
from typing import Union
from tkinter import BooleanVar, StringVar, IntVar, Tk
from ui.mainview import GameView
from ui.attributes import FuncAttributes, VarAttributes
from logic.mainmodel import GameData
from logic import GameState, secrets

SETTINGS_PATH = "./lib/settings.json"
MAX_DIM_SIZE = 70
logging.basicConfig()


class Gameapp():
    """
    Main game controller
    """
    def __init__(self):
        self.root = Tk()

        # Must load settings first, becuase model and view depend on them
        self.settings = load_settings()
        self.model = GameData(timer_callback=self.update_timer)

        functions = self.get_callback_funcs()
        settings = self.get_setting_vars()
        self.view = GameView(functions, settings, self.root)

        self.tile_updates = []

        self.new_game()

    def get_setting(self, setting):
        """
        Returns the raw value of a setting.
        """
        if type(self.settings[setting]) in [StringVar, IntVar, BooleanVar]:
            return self.settings[setting].get()
        else:
            return self.settings[setting]

    def new_game(self) -> None:
        """
        Reset the app to a beginning-of-game state.
        """
        # Clear out remnants of any active game
        self.model.stop_timer()
        self.tile_updates = []

        # If the timer was paused, tell the view to start
        # accepting timer updates again.
        self.view.interrupt_timer_update = False
        self.view.update_timer_display("00:00")
        self.view.hide_gameover_alert()
        self.view.hide_gridsize_modal()

        logging.info(f"Starting new game")
        self.validate_dims()
        rows, cols = self.get_new_grid_dims()
        difficulty = self.get_setting("difficulty")
        self.model.new_game(rows, cols, difficulty)

        self.view.make_gameboard()

    def validate_dims(self):
        """
        Validate the user-defined dimensions of the playing field.
        Dimensions may not be 0 units, nor exceed 70 units.
        """
        validate = True

        widthvar = self.settings["grid_width"]
        heightvar = self.settings["grid_height"]
        try:
            width_units = int(widthvar.get())
        except ValueError:
            validate = False
            widthvar.set(10)
            width_units = int(widthvar.get())

        try:
            height_units = int(heightvar.get())
        except ValueError:
            validate = False
            heightvar.set(10)
            height_units = int(heightvar.get())

        if width_units > MAX_DIM_SIZE:
            widthvar.set(MAX_DIM_SIZE)
            validate = False
        if height_units > MAX_DIM_SIZE:
            heightvar.set(MAX_DIM_SIZE)
            validate = False
        if width_units == "" or width_units <= 0:
            widthvar.set(10)
            validate = False
        if height_units == "" or height_units <= 0:
            heightvar.set(10)
            validate = False

        return validate

    def get_new_grid_dims(self):
        """
        Return the current values of the grid_height and grid_width setting.
        (These values are potentially different than the actual dimensions of
        the current grid, for instance, if the user has changed the grid dimensions
        but has not yet asked for a new game.)
        """
        rows = int(self.get_setting("grid_height"))
        cols = int(self.get_setting("grid_width"))
        return (rows, cols)

    def get_num_remaining_cells(self):
        """
        Get the number of cells whose `is_revealed` property is False
        """
        return self.model.get_num_remaining_cells()

    def get_num_mines(self):
        """
        Get the number of mines in the current game.
        """
        return self.model.get_num_mines()

    def get_gameboard(self):
        """
        Get the gameboard data of the current game.
        """
        return self.model.get_gameboard()

    def is_revealed(self, row, col) -> bool:
        """
        Return the value of the `is_revealed` key of the cell located at `(row, col)`
        """
        cell = self.get_gameboard()[row][col]
        return cell["is_revealed"]

    def flag(self, row, col):
        """
        Toggle the `is_flagged` key for the cell located at `(row, col)`

        Ignore if the game is over.
        """
        if self.model.game_state in [GameState.LOSE, GameState.WIN]:
            return
        if self.is_revealed(row, col) is True:
            return
        secrets.flag(self.get_gameboard(), row, col, self.tile_updates)
        self.update_grid()

    def reveal(self, row, col):
        """
        Set the `is_revealed` key for the cell located at `(row, col)`, and
        do the same for its neighbors and extended neighbors. This action also
        triggers the timer to start (which is ignored by the model if the timer
        has already been started.)

        Ignore if the game is over.
        """
        if self.model.game_state in [GameState.LOSE, GameState.WIN]:
            return
        elif self.model.game_state is GameState.IDLE:
            self.model.check_first_move(row, col)
            self.model.start_timer()

        state = secrets.reveal(self.get_gameboard(), row, col, self.tile_updates)
        self.update_gamestate(state)

    def quick_reveal(self, row, col, num_clicks):
        """
        Perform a quick reveal at the cell hint located at `(row, col)`
        """
        if self.model.game_state in [GameState.LOSE, GameState.WIN]:
            return
        if self.is_revealed(row, col) is False:
            return
        if num_clicks != self.get_setting("quick_reveal"):
            return

        state = secrets.quick_reveal(self.get_gameboard(), row, col, self.tile_updates)
        self.update_gamestate(state)

    def update_gamestate(self, state):
        """
        Update the current state of the game. If the game is not over, check to see if
        a win condition has been met.
        """
        # Update the grid before doing anything else to make sure that all the
        # user's inputs go through, in the event that we need to block them during
        # a gameover condition
        self.update_grid()
        if state == GameState.CONTINUE:
            state = self.model.check_win_condition()
        self.model.game_state = state

        if state in [GameState.WIN, GameState.LOSE]:
            self.gameover()

    def update_timer(self, timestr):
        """
        Update the timer display. Used as the callback for the timer module, so
        this function typically runs on a separate thread.
        """
        self.view.update_timer_display(timestr)

    def update_grid(self):
        """
        Update the grid display, using the `self.tile_updates` list
        """
        self.view.update_grid(self.tile_updates)
        
    def pause_timer(self):
        """
        Pause the timer, if it is running.
        """
        return self.model.pause_timer()

    def resume_timer(self):
        """
        Resume the timer, if it is paused.
        """
        self.model.resume_timer()

    def gameover(self):
        """
        End the game if either a WIN or LOSE condition is met
        """
        # Clean up the view
        self.view.interrupt_timer_update = True
        self.model.stop_timer()

        # No need to reveal all the times if the player has won, because
        # all the tiles are already revealed!
        if self.model.game_state == GameState.LOSE:
            secrets.reveal_all(self.get_gameboard(), self.tile_updates)
            self.update_grid()

        # Tease or congratulate the player
        text = get_random_text(self.model.game_state)
        self.view.show_gameover_alert(text)
        logging.info("Game over!", text)

    def quit_game(self):
        save_settings(self.settings, self.get_setting("save_settings_on_quit"))
        self.model.stop_timer()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def get_callback_funcs(self):
        funcs = {
            "flag": self.flag,
            "get_gameboard": self.get_gameboard,
            "get_num_mines": self.get_num_mines,
            "get_num_remaining_cells": self.get_num_remaining_cells,
            "new_game": self.new_game,
            "pause_timer": self.pause_timer,
            "quick_reveal": self.quick_reveal,
            "quit_game": self.quit_game,
            "resume_timer": self.resume_timer,
            "reveal": self.reveal,
            "validate_dims": self.validate_dims
        }
        return FuncAttributes(funcs)

    def get_setting_vars(self):
        return VarAttributes(self.settings)


def load_settings():
    """
    Load the settings json file
    """
    with open(SETTINGS_PATH, "r") as f:
        json_dict = json.load(f)

    game_settings = {}
    # Need to make some settings a Tk variable so that
    # the information is available to the UI
    for s in json_dict["user"]:
        setting = json_dict["user"][s]
        if setting["type"] == "tkint":
            game_settings[s] = IntVar(value=setting["value"])
            continue
        elif setting["type"] == "tkstr":
            game_settings[s] = StringVar(value=setting["value"])
            continue
        elif setting["type"] == "tkbool":
            game_settings[s] = BooleanVar(value=setting["value"])
            continue
        else:
            game_settings[s] = setting["value"]

    return game_settings


def save_settings(settings, save_default=False):
    """
    Copy the current settings into the user settings section of the settings json file.
    If the user is not using the `save_settings_on_quit` option, overwrite the user
    settings with the default settings.
    """
    if save_default is False:
        save_default_settings()
        return

    json_dict = {}

    # Make all the tkinter variables serializable
    for key in settings:
        val = settings[key]
        if type(val) == StringVar:
            stype = "tkstr"
            val = val.get()
        elif type(val) == IntVar:
            stype = "tkint"
            val = val.get()
        elif type(val) == BooleanVar:
            stype = "tkbool"
            val = val.get()
        elif type(val) == int:
            stype = "int"

        json_dict[key] = {
            "value": val,
            "type": stype
        }

    # If something goes awry, abort before writing to file to avoid
    # corrupting the settings file.
    try:
        json.dumps(json_dict)
    except TypeError:
        logging.error("Couldn't save settings. Sorry!")
    else:
        with open(SETTINGS_PATH, "r+") as fp:
            data = json.load(fp)
            data["user"] = json_dict
            fp.seek(0)
            fp.truncate()
            json.dump(data, fp, indent=4)


def save_default_settings():
    """
    Copy the default settings into the user settings segment of the
    settings json file.
    """
    with open(SETTINGS_PATH, "r+") as fp:
        json_dict = json.load(fp)
        json_dict["user"] = json_dict["default"]
        fp.seek(0)
        fp.truncate()
        json.dump(json_dict, fp, indent=4)


def get_random_text(section) -> str:
    """
    Return a random phrase from the `section` of the phrases document.
    """
    with open("./lib/phrases.json", "r") as f:
        phrases = json.load(f)

    return random.choice(phrases[section])


def main():
    game = Gameapp()
    game.run()


if __name__ == "__main__":
    main()
