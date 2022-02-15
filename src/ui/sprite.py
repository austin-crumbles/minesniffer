from PIL import Image, ImageTk
import os

def get_mine_sprite(cell_size):
    path = os.path.abspath("./lib/minesprite.png")
    return load_sprite(path, cell_size)

def get_flag_sprite(cell_size):
    path = os.path.abspath("./lib/flagsprite.png")
    return load_sprite(path, cell_size)

def load_sprite(path, cell_size):
    """
    Load the sprite from the given path using the given cell_size.
    """
    sprite = Image.open(path)
    sprite = sprite.resize((cell_size, cell_size))
    sprite = ImageTk.PhotoImage(sprite)

    return sprite