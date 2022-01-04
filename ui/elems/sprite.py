from PIL import Image, ImageTk

sprite = Image.open('sprite.png')
sprite = sprite.resize((cell_size, cell_size))
bomb_sprite = ImageTk.PhotoImage(sprite)