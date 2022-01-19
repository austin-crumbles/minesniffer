from tkinter import Menu

def make_options_menu(root, controller):
    """
    Create the options menu list, used for both the top menu bar
    and context menu.
    """
    options_bar = make_menubar(root)

    options_menu = Menu(options_bar)
    options_quick_reveal = Menu(options_menu)
    options_difficulty = Menu(options_menu)
    options_theme = Menu(options_menu)

    options_bar.add_cascade(
        menu=options_menu, 
        label="Options"
    )

    # ===========================================
    # =============TOP LEVEL ITEMS===============
    # ===========================================
    options_menu.add_command(
        label="New Game", 
        command=controller.reset_game, 
        accelerator="Ctrl+N"
    )
    options_menu.add_separator()
    options_menu.add_cascade(
        menu=options_theme, 
        label="Theme"
    )
    options_menu.add_command(
        label="Grid size...", 
        command=controller.change_grid_size, 
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

    # ==========================================
    # =============SUB MENU ITEMS===============
    # ==========================================

    # ==========================================
    # ==============QUICK REVEAL================
    # ==========================================
    options_quick_reveal.add_radiobutton(
        label="Double click", 
        variable=controller.settings['quick_reveal'], 
        value=2, 
        command=lambda: controller.update_infobar()
    )
    options_quick_reveal.add_radiobutton(
        label="Single click", 
        variable=controller.settings['quick_reveal'], 
        value=1, 
        command=lambda: controller.update_infobar()
    )
    options_quick_reveal.add_radiobutton(
        label="Off", 
        variable=controller.settings['quick_reveal'], 
        value=0, 
        command=lambda: controller.update_infobar()
    )

    # ======================================
    # =============DIFFICULTY===============
    # ======================================
    options_difficulty.add_radiobutton(
        label="Easy", 
        variable=controller.settings['difficulty'], 
        value="Easy",  
        command=lambda: controller.update_infobar()
    )
    options_difficulty.add_radiobutton(
        label="Normal", 
        variable=controller.settings['difficulty'], 
        value="Normal", 
        command=lambda: controller.update_infobar()
    )
    options_difficulty.add_radiobutton(
        label="Hard", 
        variable=controller.settings['difficulty'], 
        value="Hard", 
        command=lambda: controller.update_infobar()
    )
    options_difficulty.add_radiobutton(
        label="Deadly", 
        variable=controller.settings['difficulty'], 
        value="Deadly", 
        command=lambda: controller.update_infobar()
    )

    # =================================
    # =============THEME===============
    # =================================
    options_theme.add_radiobutton(
        label="Light", 
        variable=controller.settings['game_theme'], 
        value='light', 
        command=lambda: controller.stylize('light')
    )
    options_theme.add_radiobutton(
        label="Dark", 
        variable=controller.settings['game_theme'], 
        value='dark', 
        command=lambda: controller.stylize('dark')
    )
    options_theme.add_radiobutton(
        label="Dark red", 
        variable=controller.settings['game_theme'], 
        value='dark_red', 
        command=lambda: controller.stylize('dark_red')
    )
    options_theme.add_radiobutton(
        label="Dark blue", 
        variable=controller.settings['game_theme'], 
        value='dark_blue', 
        command=lambda: controller.stylize('dark_blue')
    )
    options_theme.add_radiobutton(
        label="Ugly", 
        variable=controller.settings['game_theme'], 
        value='test', 
        command=lambda: controller.stylize('test')
    )

    return options_menu

def make_menubar(root):
    """
    Create the main top menu bar
    """
    root.option_add("*tearOff", 0)

    options_bar = Menu(root)
    root['menu'] = options_bar

    return options_bar