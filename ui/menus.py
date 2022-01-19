from tkinter import Menu

def make_options_menus(parent):
    """
    Create the options menu list, used for both the top menu bar
    and context menu.
    """
    controller = parent.controller
    options_bar = make_menubar(parent.root)

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
        command=controller.new_game, 
        accelerator="Ctrl+N"
    )
    options_menu.add_separator()
    options_menu.add_cascade(
        menu=options_theme, 
        label="Theme"
    )
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
        command=lambda: parent.update_infobar()
    )
    options_quick_reveal.add_radiobutton(
        label="Single click", 
        variable=controller.settings['quick_reveal'], 
        value=1, 
        command=lambda: parent.update_infobar()
    )
    options_quick_reveal.add_radiobutton(
        label="Off", 
        variable=controller.settings['quick_reveal'], 
        value=0, 
        command=lambda: parent.update_infobar()
    )

    # ======================================
    # =============DIFFICULTY===============
    # ======================================
    options_difficulty.add_radiobutton(
        label="Easy", 
        variable=controller.settings['difficulty'], 
        value="Easy",  
        command=lambda: parent.update_infobar()
    )
    options_difficulty.add_radiobutton(
        label="Normal", 
        variable=controller.settings['difficulty'], 
        value="Normal", 
        command=lambda: parent.update_infobar()
    )
    options_difficulty.add_radiobutton(
        label="Hard", 
        variable=controller.settings['difficulty'], 
        value="Hard", 
        command=lambda: parent.update_infobar()
    )
    options_difficulty.add_radiobutton(
        label="Deadly", 
        variable=controller.settings['difficulty'], 
        value="Deadly", 
        command=lambda: parent.update_infobar()
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
        label="Dark red", 
        variable=controller.settings['game_theme'], 
        value='dark_red', 
        command=lambda: parent.stylize('dark_red')
    )
    options_theme.add_radiobutton(
        label="Dark blue", 
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

    return {
        "top": options_menu, 
        "difficulty": options_difficulty, 
        "quick_reveal": options_quick_reveal,
        "theme": options_theme
    }

def make_menubar(root):
    """
    Create the main top menu bar
    """
    root.option_add("*tearOff", 0)

    options_bar = Menu(root)
    root['menu'] = options_bar

    return options_bar