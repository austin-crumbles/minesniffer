"""Go sniff for some mines"""
import json
import random
import logging
from tkinter import BooleanVar, StringVar, IntVar, Tk
from ui.mainview import GameView
from logic.mainmodel import GameData
from logic import secrets, GameState

SETTINGS_PATH = './lib/settings.json'
logging.basicConfig()


class Gameapp():
    def __init__(self):
        self.root = Tk()

        self.settings = load_settings()
        self.model = GameData(self)
        self.view = GameView(self, self.root)

        self.new_game()
        
    def get_setting(self, setting):
        if type(self.settings[setting]) in [StringVar, IntVar, BooleanVar]:
            return self.settings[setting].get()
        else:
            return self.settings[setting]

    def new_game(self):
        # Clear out remnants of any active game
        self.view.interrupt_timer = False
        self.model.stop_timer()
        self.view.update_timer_display("00:00")
        self.view.hide_gameover_alert()

        logging.info(f"Starting new game")
        self.validate_dims('focusout')
        rows, cols = self.get_grid_dims()
        difficulty = self.get_setting('difficulty')
        self.model.new_game(rows, cols, difficulty)

        self.view.make_gameboard()

    def validate_dims(self, value):
        validate = True
        widthvar = self.settings['grid_width']
        heightvar = self.settings['grid_height']
        width = int(widthvar.get() or 0)
        height = int(heightvar.get() or 0)
        if width > 40:
            widthvar.set("40")
            validate = False
        if height > 40:
            heightvar.set("40")
            validate = False
        if value in ['focusout', 'focusin']:
            if widthvar.get() == '' or  widthvar.get() == 0:
                widthvar.set(10)
                return False
            if heightvar.get() == '' or  heightvar.get() == 0:
                heightvar.set(10)
                return False
        
        return validate

    def get_grid_dims(self):
        rows = int(self.get_setting('grid_height'))
        cols = int(self.get_setting('grid_width'))
        return (rows, cols)

    def get_num_remaining_cells(self):
        return self.model.get_num_remaining_cells()

    def get_num_mines(self):
        return self.model.get_num_mines()

    def get_gameboard(self):
        return self.model.get_gameboard()

    def is_revealed(self, row, col):
        cell = self.get_gameboard()[row][col]
        return cell['is_revealed']

    def flag(self, row, col):
        if self.model.game_state in [GameState.LOSE, GameState.WIN]:
            return
        if self.is_revealed(row, col) is True:
            return
        secrets.flag(self.get_gameboard(), row, col)
        self.view.update_grid()

    def reveal(self, row, col):
        if self.model.game_state in [GameState.LOSE, GameState.WIN]:
            return
        
        self.model.start_timer()

        state = secrets.reveal(self.get_gameboard(), row, col)
        self.update_gamestate(state)

    def quick_reveal(self, row, col, num_clicks):
        if self.model.game_state in [GameState.LOSE, GameState.WIN]:
            return
        if self.is_revealed(row, col) is False:
            return
        if num_clicks != self.get_setting('quick_reveal'):
            return

        state = secrets.quick_reveal(self.get_gameboard(), row, col)
        self.update_gamestate(state)

    def update_gamestate(self, state):
        self.view.update_grid()
        if state == GameState.CONTINUE:
            state = self.model.check_win_condition()
        self.model.game_state = state

        if state in [GameState.WIN, GameState.LOSE]:
            self.gameover()

    def update_timer(self, timestr):
        self.view.update_timer_display(timestr)

    def pause_timer(self):
        return self.model.pause_timer()

    def resume_timer(self):
        self.model.resume_timer()

    def gameover(self):
        self.view.interrupt_timer = True
        self.model.stop_timer()
        if self.model.game_state == GameState.LOSE:
            secrets.reveal_all(self.get_gameboard())
            self.view.update_grid()
        text = get_random_text(self.model.game_state)
        self.view.show_gameover_alert(text)
        logging.info("Game over!", text)

    def quit_game(self):
        save_settings(self.settings, self.get_setting('save_settings_on_quit'))
        self.model.stop_timer()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

def load_settings():
    with open(SETTINGS_PATH, 'r') as f:
        json_dict = json.load(f)

    game_settings = {}
    # Need to make some settings a Tk variable so that
    # the information is available to the UI
    for s in json_dict['user']:
        setting = json_dict['user'][s]
        if setting['type'] == 'tkint':
            game_settings[s] = IntVar(value=setting['value'])
            continue
        elif setting['type'] == 'tkstr':
            game_settings[s] = StringVar(value=setting['value'])
            continue
        elif setting['type'] == 'tkbool':
            game_settings[s] = BooleanVar(value=setting['value'])
            continue            
        else:
            game_settings[s] = setting['value']

    return game_settings

def save_settings(settings, save_default=False):
    if save_default is False:
        save_default_settings()
        return

    json_dict = {}

    for key in settings:
        val = settings[key]
        if type(val) == StringVar:
            stype = 'tkstr'
            val = val.get()
        elif type(val) == IntVar:
            stype = 'tkint'
            val = val.get()
        elif type(val) == BooleanVar:
            stype = 'tkbool'
            val = val.get()
        elif type(val) == int:
            stype = 'int'

        json_dict[key] = {
            'value': val,
            'type': stype
        }
    
    with open(SETTINGS_PATH, 'r+') as fp:
        data = json.load(fp)
        data['user'] = json_dict
        fp.seek(0)
        fp.truncate()
        json.dump(data, fp, indent=4)

def save_default_settings():
    with open(SETTINGS_PATH, 'r+') as fp:
        json_dict = json.load(fp)
        json_dict['user'] = json_dict['default']
        fp.seek(0)
        fp.truncate()
        json.dump(json_dict, fp, indent=4)

def get_random_text(section):
    with open('./lib/phrases.json', 'r') as f:
        phrases = json.load(f)

    return random.choice(phrases[section])

def main():
    game = Gameapp()
    game.run()

if __name__ == '__main__':
    main()
