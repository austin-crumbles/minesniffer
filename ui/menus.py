from tkinter import Menu

def make_options_menus(parent):
    """
    Create the options menu list, used for both the top menu bar
    and context menu.
    """
    controller = parent.controller
    menu_bar = make_menubar(parent.root)

    file_menu = Menu(menu_bar)
    options_menu = Menu(menu_bar)
    view_menu = Menu(menu_bar)
    options_quick_reveal = Menu(options_menu)
    options_difficulty = Menu(options_menu)
    options_theme = Menu(view_menu)
    options_animation = Menu(view_menu)

    menu_bar.add_cascade(
        menu=file_menu,
        label="File"
    )
    menu_bar.add_cascade(
        menu=view_menu,
        label="View"
    )
    menu_bar.add_cascade(
        menu=options_menu, 
        label="Options"
    )

    # ===========================================
    # =============TOP LEVEL ITEMS===============
    # ===========================================
    file_menu.add_command(
        label="New Game", 
        command=controller.new_game, 
        accelerator="Ctrl+N"
    )
    file_menu.add_checkbutton(
        label="Save settings on exit",
        variable=controller.settings['save_settings_on_quit'],
        onvalue=True,
        offvalue=False
    )
    # options_menu.add_separator()
    options_menu.add_command(
        label="Grid size...", 
        command=parent.show_gridsize_modal, 
        accelerator="Ctrl+G"
    )
    options_menu.add_cascade(
        menu=options_quick_reveal, 
        label="Quick reveal tiles"
    )
    options_menu.add_cascade(
        menu=options_difficulty, 
        label="Difficulty"
    )
    view_menu.add_cascade(
        menu=options_theme, 
        label="Theme"
    )
    view_menu.add_cascade(
        menu=options_animation,
        label="Grid animation"
    )
    view_menu.add_command(
        label="Zoom in",
        accelerator="Ctrl++",
        command=parent.zoom_in
    )
    view_menu.add_command(
        label="Zoom out",
        accelerator="Ctrl+-",
        command=parent.zoom_out
    )

    # ==========================================
    # =============SUB MENU ITEMS===============
    # ==========================================

    # ==========================================
    # ==============QUICK REVEAL================
    # ==========================================
    options_quick_reveal.add_radiobutton(
        label="Double click", 
        variable=controller.settings['quick_reveal'], 
        value=2
    )
    options_quick_reveal.add_radiobutton(
        label="Single click", 
        variable=controller.settings['quick_reveal'], 
        value=1
    )
    options_quick_reveal.add_radiobutton(
        label="Off", 
        variable=controller.settings['quick_reveal'], 
        value=0
    )

    # ======================================
    # =============DIFFICULTY===============
    # ======================================
    options_difficulty.add_radiobutton(
        label="Easy", 
        variable=controller.settings['difficulty'], 
        value='Easy'
    )
    options_difficulty.add_radiobutton(
        label="Normal", 
        variable=controller.settings['difficulty'], 
        value='Normal'
    )
    options_difficulty.add_radiobutton(
        label="Hard", 
        variable=controller.settings['difficulty'], 
        value='Hard'
    )
    options_difficulty.add_radiobutton(
        label="Deadly", 
        variable=controller.settings['difficulty'], 
        value='Deadly'
    )

    # =================================
    # =============THEME===============
    # =================================
    options_theme.add_radiobutton(
        label="Light", 
        variable=controller.settings['game_theme'], 
        value='light', 
        command=lambda: parent.stylize('light')
    )
    options_theme.add_radiobutton(
        label="Dark", 
        variable=controller.settings['game_theme'], 
        value='dark', 
        command=lambda: parent.stylize('dark')
    )
    options_theme.add_radiobutton(
        label="Mars", 
        variable=controller.settings['game_theme'], 
        value='dark_red', 
        command=lambda: parent.stylize('dark_red')
    )
    options_theme.add_radiobutton(
        label="Ocean", 
        variable=controller.settings['game_theme'], 
        value='dark_blue', 
        command=lambda: parent.stylize('dark_blue')
    )
    options_theme.add_radiobutton(
        label="Ugly", 
        variable=controller.settings['game_theme'], 
        value='test', 
        command=lambda: parent.stylize('test')
    )
    # ==========================================
    # ================Animation=================
    # ==========================================

    options_animation.add_radiobutton(
        label="Off",
        variable=controller.settings['grid_animation'],
        value='none'
    )
    options_animation.add_radiobutton(
        label="Linear",
        variable=controller.settings['grid_animation'],
        value='linear'
    )
    options_animation.add_radiobutton(
        label="Random",
        variable=controller.settings['grid_animation'],
        value='random'
    )
    options_animation.add_radiobutton(
        label="Snake",
        variable=controller.settings['grid_animation'],
        value='snake'
    )

def make_menubar(root):
    """
    Create the main top menu bar
    """
    root.option_add('*tearOff', 0)

    options_bar = Menu(root)
    root['menu'] = options_bar

    return options_bar