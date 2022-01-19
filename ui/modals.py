from tkinter import Toplevel, Frame, Label, Scale, Button, HORIZONTAL, FALSE

def make_gridsize_modal(root, controller):
    gsdiag = Toplevel(root)
    gsframe = Frame(gsdiag)
    gstext = Label(
        gsframe,
        text="Grid size will update in the next game"
    )
    gswidth = Scale(
        gsframe,
        orient=HORIZONTAL,
        length=200,
        variable=controller.settings['grid_width'], 
        from_=10, 
        to=40
    )
    gsheight = Scale(
        gsframe, 
        orient=HORIZONTAL,
        length=200, 
        variable=controller.settings['grid_height'], 
        from_=10, 
        to=40
    )
    gsclose = Button(
        gsframe, 
        text="Close", 
        command=gsdiag.destroy
    )

    gsdiag.resizable(FALSE, FALSE)
    gsdiag.title("Grid size")
    gsframe.grid(padx=20, pady=(20, 10))
    gstext.grid()
    gswidth.grid()
    gsheight.grid()
    gsclose.grid(pady=10)

def build_loading_window(root):
    """Loading window"""
    bar_win = Toplevel(root)
    bar_win.withdraw()
    bar_f = Frame(bar_win)
    bar_label = Label(bar_f, text="Loading BombSniffer...")
    bar_f.grid(padx=10, pady=10)
    bar_label.grid(pady=(0, 5))
    bar_win.deiconify()