"""Go sniff for some bombs"""
from ui.timer import BombTimer

class Gameapp():
    def __init__(self):
        self.window: BombWin = None
        self.settings: BombSettings = None
        self.grid: BombGrid = None
        self.timer: BombTimer = None 

        self.game_over = False

        get_window()
        get_settings()
        get_grid()

        self.new_game()

    def new_game(self):
        self.timer = BombTimer()
        update_settings()
        update_grid()

def main():
    game = Gameapp()
    game.new_game()

if __name__ == "__main__":
    main()
