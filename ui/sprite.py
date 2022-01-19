from PIL import Image, ImageTk
from os.path import normpath

def get_sprite(controller):
    cell_size = controller.get_setting('cell_size')
    sprite = Image.open(normpath('../lib/sprite.png'))
    sprite = sprite.resize((cell_size, cell_size))
    mine_sprite = ImageTk.PhotoImage(sprite)

    return mine_sprite