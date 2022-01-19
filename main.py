"""Go sniff for some mines"""
import json
from tkinter import StringVar, IntVar
from ui.window import GameWin
from logic.gamedata import GameData
from logic import secrets, gamestate

class Gameapp():
    def __init__(self):
        self.settings: dict = None
        self.data = GameData()
        self.window = GameWin(self)

        self.read_settings()
        self.new_game()

    def read_settings(self):
        with open("settings.json", "r") as f:
            json_dict = json.load(f)

        settings = {}
        # Need to make some settings a Tk variable so that
        # the information is available to the UI
        for s in json_dict:
            if json_dict[s]['type'] == "tkint":
                settings[s] = IntVar(value=json_dict[s]['value'])
                continue
            elif json_dict[s]['type'] == "tkstr":
                settings[s] = StringVar(value=json_dict[s]['value'])
                continue
            else:
                settings[s] = json_dict[s]

        self.settings = settings

    def get_setting(self, setting):
        if type(self.settings[setting]) in [StringVar, IntVar]:
            return self.settings[setting].get_value()
        else:
            return self.settings[setting]

    def new_game(self):
        self.data.new_game()

    def get_grid_dims(self):
        rows = self.settings['grid_height'].get_value()
        cols = self.settings['grid_width'].get_value()
        return (rows, cols)

    def get_gameboard_data(self):
        return self.data.get_gameboard()

    def quick_reveal(self, row, col, num_clicks):
        if num_clicks != self.settings['quick_reveal'].get_value():
            return

        state = secrets.quick_reveal(self.data.get_gameboard(), row, col)
        self.data.game_state = state
        if state == gamestate.LOSE:
            self.gameover_lose()
        elif state == gamestate.WIN:
            self.gameover_win()

        self.update_window()

    def flag(self, row, col):
        secrets.flag(self.data.get_gameboard(), row, col)
        self.update_window()

    def reveal(self, row, col):
        secrets.reveal(self.data.get_gameboard(), row, col)
        self.update_window()

    def update_infobar(self):
        self.window.update_infobar()

    def quit_game():
        pass

    def change_gridsize():
        pass

    def show_options_menu(e):
        options_menu.post(e.x_root, e.y_root)

    def game_over(e):
        settings.gameover = True

        if e == 0:
            g_over_alert['text'] = "Game Over!"
        elif e == 1:
            g_over_alert['text'] = "Chicken dinner!"

        g_over_alert.grid(column=0, row=1)

    def set_info_display(var):    # Formerly called "set_info_var"
        """Set variables for info bar

        Use 'gs' for grid size. Use 'ar' for auto reveal.
        Use 'd' for difficulty.
        """
        if var == 'gs':
            format_info_gridsize()
        if var == 'ar':
            format_info_quickreveal()
        if var == 'd':
            format_info_difficulty()

    def format_info_gridsize(self):
        info_grid['text'] = info_vars['gs'].format(grid_size[0], grid_size[1])

    def format_info_quickreveal(self):
        n = self.quick_reveal.get()
        if n == 0:
            t = info_vars['ar'].format("Off")
        elif n == 1:
            t = info_vars['ar'].format("Single click")
        elif n == 2:
            t = info_vars['ar'].format("Double click")
        info_reveal['text'] = t

    def format_info_difficulty(self):
        difficulty['lvl'] = difficulty_var.get()

    def run(self):
        self.window.root.mainloop()

def main():
    game = Gameapp()
    game.new_game()

    game.run()

if __name__ == "__main__":
    main()
