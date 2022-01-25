from tkinter import ttk, Toplevel, Scale, HORIZONTAL, FALSE

def make_gridsize_modal(parent, controller):
    # gsdiag = Toplevel(root)
    root = parent.root

    widthvar = controller.settings['grid_width']
    heightvar = controller.settings['grid_height']
    gsframe = ttk.Frame(root, style='modal.TFrame')
    gstext = ttk.Label(
        gsframe,
        text="Grid size will update in the next game"
    )
    gswidth_label = ttk.Label(
        gsframe,
        text="Width:"
    )
    gswidth = ttk.Entry(
        gsframe,
        width=2,
        textvariable=widthvar,
        validate='all',
        validatecommand=controller.validate_dims,
        invalidcommand=invalid
    )
    gsheight_label = ttk.Label(
        gsframe,
        text="Height:"
    )
    gsheight = ttk.Entry(
        gsframe,
        width=2,
        textvariable=heightvar,
        validate='all',
        validatecommand=controller.validate_dims,
        invalidcommand=invalid
    )
    gsclose = ttk.Button(
        gsframe, 
        text="Close", 
        command=parent.hide_gridsize_modal
    )

    # gsdiag.resizable(FALSE, FALSE)
    # gsdiag.title("Grid size")
    gsframe.columnconfigure(0, weight=1)
    gsframe.columnconfigure(1, weight=1)
    gsframe.rowconfigure(0, weight=1)
    gsframe.rowconfigure(1, weight=1)
    gsframe.rowconfigure(2, weight=1)
    gsframe.rowconfigure(3, weight=1)


    gstext.grid(row=0, column=0, columnspan=2)
    gswidth_label.grid(row=1, column=0, pady=5)
    gswidth.grid(row=2, column=0, pady=5)
    gsheight_label.grid(row=1, column=1, pady=5)
    gsheight.grid(row=2, column=1, pady=5)
    gsclose.grid(row=3, column=0, pady=10, columnspan=2)

    return gsframe

def invalid():
    print("Invalid dimensions")


# def build_loading_window(root):
#     """Loading window"""
#     bar_win = Toplevel(root)
#     bar_win.withdraw()
#     bar_f = ttk.Frame(bar_win)
#     bar_label = ttk.Label(bar_f, text="Loading BombSniffer...")
#     bar_f.grid(padx=10, pady=10)
#     bar_label.grid(pady=(0, 5))
#     bar_win.deiconify()