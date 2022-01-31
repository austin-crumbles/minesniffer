from tkinter import Menu, Tk, Variable

def make_options_menus(root: Tk, setting_vars: dict, functions: dict):
    """
    Create the options menu list, used for both the top menu bar
    and context menu.
    """
    setting_vars = MenuVars(setting_vars)
    functions = MenuFuncs(functions)
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
        command=functions.new_game, 
        accelerator="Ctrl+N"
    )
    file_menu.add_checkbutton(
        label="Save settings on exit",
        variable=setting_vars.save_settings_on_quit,
        onvalue=True,
        offvalue=False
    )
    # options_menu.add_separator()
    options_menu.add_command(
        label="Grid size...", 
        command=functions.show_gridsize_modal, 
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
        command=functions.zoom_in
    )
    view_menu.add_command(
        label="Zoom out",
        accelerator="Ctrl+-",
        command=functions.zoom_out
    )

    # ==========================================
    # =============SUB MENU ITEMS===============
    # ==========================================

    # ==========================================
    # ==============QUICK REVEAL================
    # ==========================================
    options_quick_reveal.add_radiobutton(
        label="Double click", 
        variable=setting_vars.quick_reveal, 
        value=2
    )
    options_quick_reveal.add_radiobutton(
        label="Single click", 
        variable=setting_vars.quick_reveal, 
        value=1
    )
    options_quick_reveal.add_radiobutton(
        label="Off", 
        variable=setting_vars.quick_reveal, 
        value=0
    )

    # ======================================
    # =============DIFFICULTY===============
    # ======================================
    options_difficulty.add_radiobutton(
        label="Easy", 
        variable=setting_vars.difficulty, 
        value='Easy'
    )
    options_difficulty.add_radiobutton(
        label="Normal", 
        variable=setting_vars.difficulty, 
        value='Normal'
    )
    options_difficulty.add_radiobutton(
        label="Hard", 
        variable=setting_vars.difficulty, 
        value='Hard'
    )
    options_difficulty.add_radiobutton(
        label="Deadly", 
        variable=setting_vars.difficulty, 
        value='Deadly'
    )

    # =================================
    # =============THEME===============
    # =================================
    options_theme.add_radiobutton(
        label="Light", 
        variable=setting_vars.game_theme, 
        value='light', 
        command=lambda: functions.stylize
    )
    options_theme.add_radiobutton(
        label="Dark", 
        variable=setting_vars.game_theme, 
        value='dark', 
        command=lambda: functions.stylize
    )
    options_theme.add_radiobutton(
        label="Mars", 
        variable=setting_vars.game_theme, 
        value='dark_red', 
        command=lambda: functions.stylize
    )
    options_theme.add_radiobutton(
        label="Ocean", 
        variable=setting_vars.game_theme, 
        value='dark_blue', 
        command=lambda: functions.stylize
    )
    options_theme.add_radiobutton(
        label="Ugly", 
        variable=setting_vars.game_theme, 
        value='test', 
        command=lambda: functions.stylize
    )
    # ==========================================
    # ================Animation=================
    # ==========================================

    options_animation.add_radiobutton(
        label="Off",
        variable=setting_vars.grid_animation,
        value='none'
    )
    options_animation.add_radiobutton(
        label="Linear",
        variable=setting_vars.grid_animation,
        value='linear'
    )
    options_animation.add_radiobutton(
        label="Random",
        variable=setting_vars.grid_animation,
        value='random'
    )
    options_animation.add_radiobutton(
        label="Snake",
        variable=setting_vars.grid_animation,
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


class MenuFuncs:
    def __init__(self, funcs: dict = None):
        if funcs is None:
            funcs = {}

        self.funcs_dict = funcs
        self.funcs_list = [
            'new_game',
            'show_gridsize_modal',
            'zoom_in',
            'zoom_out',
            'stylize'
        ]
        self.new_game = None
        self.show_gridsize_modal = None
        self.zoom_in = None
        self.zoom_out = None
        self.stylize = None

        self.set_funcs()

    def set_funcs(self):
        for f in self.funcs_list:
            if f not in self.funcs_dict:
                def no_func(*args, **kwargs):
                    raise NotImplementedError(f"{f} is not defined")
                self.funcs_dict[f] = no_func

        self.new_game = self.funcs_dict['new_game']
        self.show_gridsize_modal = self.funcs_dict['show_gridsize_modal']
        self.zoom_in = self.funcs_dict['zoom_in']
        self.zoom_out = self.funcs_dict['zoom_out']
        self.stylize = self.funcs_dict['stylize']


class MenuVars:
    def __init__(self, vars: dict = None):
        if vars is None:
            vars = {}

        self.vars_dict = vars
        self.vars_list = [
            'save_settings_on_quit',
            'quick_reveal',
            'difficulty',
            'setting_vars',
            'grid_animation',
            'game_theme'
        ]
        self.save_settings_on_quit = None
        self.quick_reveal = None
        self.difficulty = None
        self.setting_vars = None
        self.grid_animation = None
        self.game_theme = None

        self.default_var = Variable()

        self.set_vars()

    def set_vars(self):
        for f in self.vars_list:
            if f not in self.vars_dict:
                self.vars_dict[f] = self.default_var

        self.save_settings_on_quit = self.vars_dict['save_settings_on_quit']
        self.quick_reveal = self.vars_dict['quick_reveal']
        self.difficulty = self.vars_dict['difficulty']
        self.setting_vars = self.vars_dict['setting_vars']
        self.grid_animation = self.vars_dict['grid_animation']
        self.game_theme = self.vars_dict['game_theme']