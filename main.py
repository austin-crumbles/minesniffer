"""Go sniff for some mines"""
import json
import random
from os import stat
from tkinter import StringVar, IntVar
from ui.window import GameWin
from logic.gamedata import GameData
from logic import secrets, GameState

class Gameapp():
    def __init__(self):
        self.settings: dict = None
        self.data: GameData = None
        self.window: GameWin = None

        self.window = GameWin(self)     # Have to get the Tk root element started before we can load the settings
        self.read_settings()
        self.data = GameData(self)
        self.window.make_window()       # Have to wait for settings to load before we can finish making
                                        # the rest of the window
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
                settings[s] = json_dict[s]['value']

        self.settings = settings

    def get_setting(self, setting):
        if type(self.settings[setting]) in [StringVar, IntVar]:
            return self.settings[setting].get()
        else:
            return self.settings[setting]

    def new_game(self):
        print(f"[main::new_game] Starting new game")
        self.data.new_game()
        self.window.make_gameboard()

    def get_grid_dims(self):
        rows = self.get_setting('grid_height')
        cols = self.get_setting('grid_width')
        return (rows, cols)

    def get_num_mines(self):
        return self.data.get_num_mines()

    def get_gameboard(self):
        return self.data.get_gameboard()

    def quick_reveal(self, row, col, num_clicks):
        if self.data.game_state in [GameState.LOSE, GameState.WIN]:
            return
    
        if num_clicks != self.settings['quick_reveal'].get_value():
            return

        state = secrets.quick_reveal(self.data.get_gameboard(), row, col)

        self.update_state(state)
        self.window.update_grid()

    def flag(self, row, col):
        if self.data.game_state in [GameState.LOSE, GameState.WIN]:
            return
        secrets.flag(self.data.get_gameboard(), row, col)
        self.window.update_grid()

    def reveal(self, row, col):
        if self.data.game_state in [GameState.LOSE, GameState.WIN]:
            return
        state = secrets.reveal(self.data.get_gameboard(), row, col)
        self.update_state(state)
        self.window.update_grid()

    def update_state(self, state):
        # self.text_board()
        self.data.game_state = state
        if state in [GameState.WIN, GameState.LOSE]:
            self.gameover()

    def text_board(self):
        b = []
        for row in self.get_gameboard():
            r = []
            for cell in row:
                r.append(cell['clue'])
            b.append(r)
        for r in b:
            print(r)

    def update_infobar(self):
        self.window.update_infobar()

    def gameover(self):
        text = self.get_random_text(self.data.game_state)
        self.window.show_gameover_alert(text)
        print("Game over!", text)
        # if self.data.game_state == GameState.LOSE:
        #     secrets.reveal_all(self.get_gameboard())

    @staticmethod
    def get_random_text(section):
        with open('phrases.json', 'r') as f:
            phrases = json.load(f)

        return random.choice(phrases[section])

    def quit_game(self):
        self.window.root.destroy()

    def run(self):
        self.window.root.mainloop()

def main():
    game = Gameapp()
    # print([m for row in game.get_gameboard() for m in row if m['clue'] is not None])

    game.run()

if __name__ == "__main__":
    main()
