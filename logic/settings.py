auto_reveal_var = IntVar()
difficulty_var = StringVar()
info_vars = {
    'gs': "Grid size: {0} x {1}",
    'ar': "Auto reveal: {0}"
}

grid_height.set(grid_size[0])
grid_width.set(grid_size[1])
auto_reveal_var.set(1)
difficulty_var.set('Normal')
difficulty = {
    'lvl': difficulty_var.get(),
    'Easy': 0.06,
    'Normal': 0.08,
    'Hard': 0.10,
    'Deadly': 0.12
}