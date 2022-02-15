from tkinter import Menu, Tk
from .attributes import VarAttributes, FuncAttributes

def make_options_menus(root: Tk, settings: VarAttributes, functions: FuncAttributes):
    """
    Create the options menu list, used for both the top menu bar
    and context menu.
    """
    menu_bar = make_menubar(root)

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
        command=functions.get_func_obj("new_game"), 
        accelerator="Ctrl+N"
    )
    file_menu.add_checkbutton(
        label="Save settings on exit",
        variable=settings.get_var_obj("save_settings_on_quit"),
        onvalue=True,
        offvalue=False
    )
    # options_menu.add_separator()
    options_menu.add_command(
        label="Grid size...", 
        command=functions.get_func_obj("show_gridsize_modal"), 
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
        command=functions.get_func_obj("zoom_in")
    )
    view_menu.add_command(
        label="Zoom out",
        accelerator="Ctrl+-",
        command=functions.get_func_obj("zoom_out")
    )

    # ==========================================
    # =============SUB MENU ITEMS===============
    # ==========================================

    # ==========================================
    # ==============QUICK REVEAL================
    # ==========================================
    options_quick_reveal.add_radiobutton(
        label="Double click", 
        variable=settings.get_var_obj("quick_reveal"), 
        value=2
    )
    options_quick_reveal.add_radiobutton(
        label="Single click", 
        variable=settings.get_var_obj("quick_reveal"), 
        value=1
    )
    options_quick_reveal.add_radiobutton(
        label="Off", 
        variable=settings.get_var_obj("quick_reveal"), 
        value=0
    )

    # ======================================
    # =============DIFFICULTY===============
    # ======================================
    options_difficulty.add_radiobutton(
        label="Easy", 
        variable=settings.get_var_obj("difficulty"), 
        value="Easy"
    )
    options_difficulty.add_radiobutton(
        label="Normal", 
        variable=settings.get_var_obj("difficulty"), 
        value="Normal"
    )
    options_difficulty.add_radiobutton(
        label="Hard", 
        variable=settings.get_var_obj("difficulty"), 
        value="Hard"
    )
    options_difficulty.add_radiobutton(
        label="Deadly", 
        variable=settings.get_var_obj("difficulty"), 
        value="Deadly"
    )

    # =================================
    # =============THEME===============
    # =================================
    options_theme.add_radiobutton(
        label="Light", 
        variable=settings.get_var_obj("game_theme"), 
        value="light", 
        command=functions.get_func_obj("stylize")
    )
    options_theme.add_radiobutton(
        label="Dark", 
        variable=settings.get_var_obj("game_theme"), 
        value="dark", 
        command=functions.get_func_obj("stylize")
    )
    options_theme.add_radiobutton(
        label="Mars", 
        variable=settings.get_var_obj("game_theme"), 
        value="dark_red", 
        command=functions.get_func_obj("stylize")
    )
    options_theme.add_radiobutton(
        label="Ocean", 
        variable=settings.get_var_obj("game_theme"), 
        value="dark_blue", 
        command=functions.get_func_obj("stylize")
    )
    options_theme.add_radiobutton(
        label="Ugly", 
        variable=settings.get_var_obj("game_theme"), 
        value="test", 
        command=functions.get_func_obj("stylize")
    )
    # ==========================================
    # ================Animation=================
    # ==========================================

    options_animation.add_radiobutton(
        label="Off",
        variable=settings.get_var_obj("grid_animation"),
        value="none"
    )
    options_animation.add_radiobutton(
        label="Linear",
        variable=settings.get_var_obj("grid_animation"),
        value="linear"
    )
    options_animation.add_radiobutton(
        label="Random",
        variable=settings.get_var_obj("grid_animation"),
        value="random"
    )
    options_animation.add_radiobutton(
        label="Snake",
        variable=settings.get_var_obj("grid_animation"),
        value="snake"
    )


def make_menubar(root):
    """
    Create the main top menu bar
    """
    root.option_add("*tearOff", 0)

    options_bar = Menu(root)
    root["menu"] = options_bar

    return options_bar
