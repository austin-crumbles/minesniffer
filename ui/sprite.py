from PIL import Image, ImageTk
import os

def get_sprite(cell_size):
    path = os.path.abspath('./ui/minesprite.png')
    sprite = Image.open(path)
    sprite = sprite.resize((cell_size, cell_size))
    mine_sprite = ImageTk.PhotoImage(sprite)

    return mine_sprite